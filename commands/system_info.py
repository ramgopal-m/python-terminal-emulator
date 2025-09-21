"""
System information and monitoring commands.
"""
import os
import platform
import psutil
import time
from typing import List
from datetime import datetime

# Handle both relative and absolute imports
try:
    from .base import BaseCommand
except ImportError:
    # Fallback for absolute imports when running directly
    from commands.base import BaseCommand


class SystemInfo:
    """Handles system information and monitoring commands."""
    
    def ps(self, args: List[str]) -> str:
        """Show running processes."""
        try:
            # Parse arguments
            show_all = False
            show_full = False
            
            for arg in args:
                if arg in ['-a', '-A']:
                    show_all = True
                elif arg in ['-f', '--full']:
                    show_full = True
                elif arg.startswith('-'):
                    return f"ps: invalid option: {arg}"
            
            # Get processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status', 'cmdline']):
                try:
                    pinfo = proc.info
                    
                    # Filter out system processes if not showing all
                    if not show_all and pinfo['username'] != psutil.Process().username():
                        continue
                    
                    processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # Format output
            if show_full:
                header = f"{'PID':<8} {'USER':<12} {'CPU%':<6} {'MEM%':<6} {'STAT':<8} {'COMMAND'}"
                lines = [header]
                lines.append("-" * 80)
                
                for proc in processes:
                    pid = proc['pid']
                    user = proc['username'] or '?'
                    cpu = f"{proc['cpu_percent']:.1f}" if proc['cpu_percent'] else "0.0"
                    mem = f"{proc['memory_percent']:.1f}" if proc['memory_percent'] else "0.0"
                    status = proc['status'] or '?'
                    
                    if proc['cmdline']:
                        cmd = ' '.join(proc['cmdline'])
                    else:
                        cmd = proc['name'] or '?'
                    
                    # Truncate command if too long
                    if len(cmd) > 40:
                        cmd = cmd[:37] + "..."
                    
                    lines.append(f"{pid:<8} {user:<12} {cpu:<6} {mem:<6} {status:<8} {cmd}")
            else:
                header = f"{'PID':<8} {'NAME':<20} {'STATUS':<10}"
                lines = [header]
                lines.append("-" * 40)
                
                for proc in processes:
                    pid = proc['pid']
                    name = proc['name'] or '?'
                    status = proc['status'] or '?'
                    
                    # Truncate name if too long
                    if len(name) > 18:
                        name = name[:15] + "..."
                    
                    lines.append(f"{pid:<8} {name:<20} {status:<10}")
            
            return "\n".join(lines)
        except Exception as e:
            return f"ps: {str(e)}"
    
    def top(self, args: List[str]) -> str:
        """Show system resource usage."""
        try:
            # Get system information
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            # Get load averages (Unix-like systems)
            try:
                load_avg = os.getloadavg()
                load_str = f"Load average: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
            except (OSError, AttributeError):
                # Windows doesn't have load averages
                load_str = "Load average: N/A (Windows)"
            
            # Format uptime
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            uptime_str = f"{days} days, {hours:02d}:{minutes:02d}"
            
            # System summary
            output = []
            output.append(f"System: {platform.system()} {platform.release()}")
            output.append(f"Uptime: {uptime_str}")
            output.append(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            output.append("")
            output.append(f"CPU Usage: {cpu_percent}%")
            output.append(f"Memory Usage: {memory.percent}% ({self._format_bytes(memory.used)}/{self._format_bytes(memory.total)})")
            output.append(f"Disk Usage: {disk.percent}% ({self._format_bytes(disk.used)}/{self._format_bytes(disk.total)})")
            output.append(load_str)
            output.append("")
            
            # Top processes by CPU
            output.append("Top Processes by CPU:")
            output.append(f"{'PID':<8} {'NAME':<20} {'CPU%':<8} {'MEM%':<8}")
            output.append("-" * 50)
            
            # Get top processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    pinfo['cpu_percent'] = proc.cpu_percent()
                    if pinfo['cpu_percent'] is not None:
                        processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            # Show top 10
            for proc in processes[:10]:
                pid = proc['pid']
                name = proc['name'][:18] if proc['name'] else '?'
                cpu = f"{proc['cpu_percent']:.1f}" if proc['cpu_percent'] else "0.0"
                mem = f"{proc['memory_percent']:.1f}" if proc['memory_percent'] else "0.0"
                
                output.append(f"{pid:<8} {name:<20} {cpu:<8} {mem:<8}")
            
            return "\n".join(output)
        except Exception as e:
            return f"top: {str(e)}"
    
    def df(self, args: List[str]) -> str:
        """Show disk space usage."""
        try:
            # Parse arguments
            human_readable = False
            
            for arg in args:
                if arg in ['-h', '--human-readable']:
                    human_readable = True
                elif arg.startswith('-'):
                    return f"df: invalid option: {arg}"
            
            # Get disk usage information
            output = []
            if human_readable:
                header = f"{'Filesystem':<20} {'Size':<8} {'Used':<8} {'Avail':<8} {'Use%':<6} {'Mounted on'}"
            else:
                header = f"{'Filesystem':<20} {'1K-blocks':<12} {'Used':<12} {'Available':<12} {'Use%':<6} {'Mounted on'}"
            
            output.append(header)
            output.append("-" * 80)
            
            # Get all disk partitions
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    filesystem = partition.device
                    if len(filesystem) > 18:
                        filesystem = filesystem[:15] + "..."
                    
                    if human_readable:
                        size = self._format_bytes(usage.total)
                        used = self._format_bytes(usage.used)
                        avail = self._format_bytes(usage.free)
                    else:
                        size = str(usage.total // 1024)
                        used = str(usage.used // 1024)
                        avail = str(usage.free // 1024)
                    
                    percent = f"{usage.percent:.0f}%"
                    mountpoint = partition.mountpoint
                    
                    if human_readable:
                        output.append(f"{filesystem:<20} {size:<8} {used:<8} {avail:<8} {percent:<6} {mountpoint}")
                    else:
                        output.append(f"{filesystem:<20} {size:<12} {used:<12} {avail:<12} {percent:<6} {mountpoint}")
                
                except (PermissionError, OSError):
                    # Skip inaccessible partitions
                    continue
            
            return "\n".join(output)
        except Exception as e:
            return f"df: {str(e)}"
    
    def free(self, args: List[str]) -> str:
        """Show memory usage."""
        try:
            # Parse arguments
            human_readable = False
            
            for arg in args:
                if arg in ['-h', '--human-readable']:
                    human_readable = True
                elif arg.startswith('-'):
                    return f"free: invalid option: {arg}"
            
            # Get memory information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            if human_readable:
                # Human readable format
                output = []
                output.append(f"{'':>15} {'total':<10} {'used':<10} {'free':<10} {'shared':<10} {'buff/cache':<12} {'available':<10}")
                
                mem_total = self._format_bytes(memory.total)
                mem_used = self._format_bytes(memory.used)
                mem_free = self._format_bytes(memory.available)
                mem_shared = self._format_bytes(getattr(memory, 'shared', 0))
                mem_buff = self._format_bytes(getattr(memory, 'buffers', 0) + getattr(memory, 'cached', 0))
                mem_avail = self._format_bytes(memory.available)
                
                output.append(f"{'Mem:':<15} {mem_total:<10} {mem_used:<10} {mem_free:<10} {mem_shared:<10} {mem_buff:<12} {mem_avail:<10}")
                
                swap_total = self._format_bytes(swap.total)
                swap_used = self._format_bytes(swap.used)
                swap_free = self._format_bytes(swap.free)
                
                output.append(f"{'Swap:':<15} {swap_total:<10} {swap_used:<10} {swap_free:<10} {'0':<10} {'0':<12} {'0':<10}")
            else:
                # Kilobytes format
                output = []
                output.append(f"{'':>15} {'total':<12} {'used':<12} {'free':<12} {'shared':<12} {'buff/cache':<12} {'available':<12}")
                
                mem_total = memory.total // 1024
                mem_used = memory.used // 1024
                mem_free = memory.available // 1024
                mem_shared = getattr(memory, 'shared', 0) // 1024
                mem_buff = (getattr(memory, 'buffers', 0) + getattr(memory, 'cached', 0)) // 1024
                mem_avail = memory.available // 1024
                
                output.append(f"{'Mem:':<15} {mem_total:<12} {mem_used:<12} {mem_free:<12} {mem_shared:<12} {mem_buff:<12} {mem_avail:<12}")
                
                swap_total = swap.total // 1024
                swap_used = swap.used // 1024
                swap_free = swap.free // 1024
                
                output.append(f"{'Swap:':<15} {swap_total:<12} {swap_used:<12} {swap_free:<12} {'0':<12} {'0':<12} {'0':<12}")
            
            return "\n".join(output)
        except Exception as e:
            return f"free: {str(e)}"
    
    def whoami(self, args: List[str]) -> str:
        """Show current user."""
        try:
            import getpass
            return getpass.getuser()
        except Exception:
            # Fallback to environment variables
            return os.getenv('USERNAME', os.getenv('USER', 'unknown'))
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes in human readable format."""
        for unit in ['B', 'K', 'M', 'G', 'T']:
            if bytes_value < 1024.0:
                if unit == 'B':
                    return f"{bytes_value:.0f}{unit}"
                else:
                    return f"{bytes_value:.1f}{unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f}P"