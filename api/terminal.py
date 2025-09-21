from http.server import BaseHTTPRequestHandler
import json
import subprocess
import psutil
import os
import platform
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()

            # Parse request
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            command = data.get('command', '').lower()
            args = data.get('args', [])
            current_dir = data.get('currentDir', '/tmp')

            # Process command
            result = self.execute_command(command, args, current_dir)
            
            # Send response
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            error_result = {
                'success': False,
                'error': f'Server error: {str(e)}',
                'output': ''
            }
            self.wfile.write(json.dumps(error_result).encode('utf-8'))

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def execute_command(self, command, args, current_dir):
        try:
            if command == 'ps':
                return self.get_processes()
            elif command == 'top':
                return self.get_system_info()
            elif command == 'df':
                return self.get_disk_usage()
            elif command == 'free':
                return self.get_memory_info()
            elif command == 'whoami':
                return {'success': True, 'output': 'web-user@python-terminal', 'currentDir': current_dir}
            elif command == 'uname':
                return {'success': True, 'output': f'{platform.system()} {platform.release()}', 'currentDir': current_dir}
            elif command == 'date':
                return {'success': True, 'output': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'currentDir': current_dir}
            elif command == 'pwd':
                return {'success': True, 'output': current_dir, 'currentDir': current_dir}
            else:
                return {'success': False, 'error': f'Command "{command}" not supported in web environment', 'output': ''}
                
        except Exception as e:
            return {'success': False, 'error': str(e), 'output': ''}

    def get_processes(self):
        try:
            output = "PID     PPID    NAME                     CPU%    MEM%    STATUS\n"
            output += "-" * 70 + "\n"
            
            # Get top 10 processes by CPU usage
            processes = []
            for proc in psutil.process_iter(['pid', 'ppid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    proc_info = proc.info
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            for proc in processes[:15]:  # Top 15 processes
                pid = str(proc.get('pid', 0)).ljust(8)
                ppid = str(proc.get('ppid', 0)).ljust(8)
                name = str(proc.get('name', 'unknown'))[:20].ljust(20)
                cpu = f"{proc.get('cpu_percent', 0):.1f}%".ljust(8)
                mem = f"{proc.get('memory_percent', 0):.1f}%".ljust(8)
                status = str(proc.get('status', 'unknown'))
                
                output += f"{pid}{ppid}{name} {cpu}{mem}{status}\n"
            
            return {'success': True, 'output': output, 'currentDir': '/tmp'}
            
        except Exception as e:
            return {'success': False, 'error': f'Error getting processes: {str(e)}', 'output': ''}

    def get_system_info(self):
        try:
            # CPU Info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory Info
            memory = psutil.virtual_memory()
            
            # Disk Info
            disk = psutil.disk_usage('/')
            
            # Load average (Unix-like systems)
            try:
                load_avg = os.getloadavg()
                load_str = f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}"
            except (AttributeError, OSError):
                load_str = "Not available"
            
            output = f"""
🖥️  SYSTEM INFORMATION - Python Terminal Emulator
{'='*60}

💻 CPU Information:
   Usage: {cpu_percent}%
   Cores: {cpu_count}
   Load Average: {load_str}

🧠 Memory Information:
   Total: {self.format_bytes(memory.total)}
   Used: {self.format_bytes(memory.used)} ({memory.percent}%)
   Available: {self.format_bytes(memory.available)}

💾 Disk Information:
   Total: {self.format_bytes(disk.total)}
   Used: {self.format_bytes(disk.used)} ({disk.used/disk.total*100:.1f}%)
   Free: {self.format_bytes(disk.free)}

🌐 Platform: {platform.system()} {platform.release()}
📅 Uptime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🏆 Built for SRM Hacks with CodeMate Competition
            """
            
            return {'success': True, 'output': output.strip(), 'currentDir': '/tmp'}
            
        except Exception as e:
            return {'success': False, 'error': f'Error getting system info: {str(e)}', 'output': ''}

    def get_disk_usage(self):
        try:
            output = "Filesystem      Size    Used   Avail  Use%  Mounted on\n"
            output += "-" * 60 + "\n"
            
            # Get disk usage for root partition
            disk = psutil.disk_usage('/')
            
            size = self.format_bytes(disk.total)
            used = self.format_bytes(disk.used)
            avail = self.format_bytes(disk.free)
            use_percent = f"{disk.used/disk.total*100:.1f}%"
            
            output += f"{'/':<15} {size:<7} {used:<7} {avail:<7} {use_percent:<5} /\n"
            
            # Add info about web environment
            output += "\n💻 Running in Vercel serverless environment"
            output += "\n🚀 Python Terminal Emulator - Web Edition"
            
            return {'success': True, 'output': output, 'currentDir': '/tmp'}
            
        except Exception as e:
            return {'success': False, 'error': f'Error getting disk usage: {str(e)}', 'output': ''}

    def get_memory_info(self):
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            output = f"""
🧠 MEMORY INFORMATION
{'='*40}

Physical Memory:
  Total:     {self.format_bytes(memory.total)}
  Used:      {self.format_bytes(memory.used)} ({memory.percent:.1f}%)
  Available: {self.format_bytes(memory.available)}
  Free:      {self.format_bytes(memory.free)}
  Buffers:   {self.format_bytes(getattr(memory, 'buffers', 0))}
  Cached:    {self.format_bytes(getattr(memory, 'cached', 0))}

Swap Memory:
  Total:     {self.format_bytes(swap.total)}
  Used:      {self.format_bytes(swap.used)} ({swap.percent:.1f}%)
  Free:      {self.format_bytes(swap.free)}

🌐 Platform: {platform.system()} {platform.machine()}
🚀 Python Terminal Emulator - Live Demo
            """
            
            return {'success': True, 'output': output.strip(), 'currentDir': '/tmp'}
            
        except Exception as e:
            return {'success': False, 'error': f'Error getting memory info: {str(e)}', 'output': ''}

    def format_bytes(self, bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024.0
        return f"{bytes:.1f}PB"