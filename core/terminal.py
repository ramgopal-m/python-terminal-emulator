"""
Main terminal engine - orchestrates command execution and terminal state.
"""
import os
import sys
from typing import Dict, Any, Optional, List

# Handle both relative and absolute imports
try:
    from .state import TerminalState
    from .command_parser import CommandParser
    from ..utils.history import CommandHistory
except ImportError:
    # Fallback for absolute imports when running directly
    from core.state import TerminalState
    from core.command_parser import CommandParser
    from utils.history import CommandHistory


class TerminalEngine:
    """Main terminal engine that coordinates all terminal operations."""
    
    def __init__(self):
        self.state = TerminalState()
        self.parser = CommandParser()
        self.history = CommandHistory()
        self.commands = {}
        self.running = True
        
        # Register built-in commands
        self._register_builtin_commands()
    
    def _register_builtin_commands(self):
        """Register built-in terminal commands."""
        try:
            from ..commands.file_ops import FileOperations
            from ..commands.system_info import SystemInfo
        except ImportError:
            # Fallback for absolute imports
            try:
                from commands.file_ops import FileOperations
                from commands.system_info import SystemInfo
            except ImportError:
                # Final fallback - add parent directory to path
                import sys
                import os
                parent_dir = os.path.dirname(os.path.dirname(__file__))
                if parent_dir not in sys.path:
                    sys.path.insert(0, parent_dir)
                from commands.file_ops import FileOperations
                from commands.system_info import SystemInfo
        
        # File operations
        file_ops = FileOperations(self.state)
        self.commands.update({
            'ls': file_ops.ls,
            'dir': file_ops.ls,  # Windows alias
            'cd': file_ops.cd,
            'pwd': file_ops.pwd,
            'mkdir': file_ops.mkdir,
            'md': file_ops.mkdir,  # Windows alias
            'rmdir': file_ops.rmdir,
            'rd': file_ops.rmdir,  # Windows alias
            'rm': file_ops.rm,
            'del': file_ops.rm,  # Windows alias
            'cp': file_ops.cp,
            'copy': file_ops.cp,  # Windows alias
            'mv': file_ops.mv,
            'move': file_ops.mv,  # Windows alias
            'touch': file_ops.touch,
            'cat': file_ops.cat,
            'type': file_ops.cat,  # Windows alias
        })
        
        # System information
        sys_info = SystemInfo()
        self.commands.update({
            'ps': sys_info.ps,
            'top': sys_info.top,
            'df': sys_info.df,
            'free': sys_info.free,
            'whoami': sys_info.whoami,
        })
        
        # Built-in commands
        self.commands.update({
            'help': self._help,
            'history': self._history,
            'clear': self._clear,
            'cls': self._clear,  # Windows alias
            'exit': self._exit,
            'quit': self._exit,
            'echo': self._echo,
            'set': self._set,
            'env': self._env,
        })
    
    def execute_command(self, command_line: str) -> str:
        """
        Execute a command and return the output.
        
        Args:
            command_line: The complete command line to execute
            
        Returns:
            String output of the command
        """
        if not command_line.strip():
            return ""
        
        try:
            # Add to history
            self.history.add(command_line)
            
            # Parse command
            command, args = self.parser.parse(command_line)
            
            if command is None:
                return ""
            
            # Parse redirections
            args, redirections = self.parser.parse_redirections(args)
            
            # Execute command
            if command in self.commands:
                try:
                    output = self.commands[command](args)
                    
                    # Handle output redirections
                    if 'stdout' in redirections:
                        self._write_to_file(output, redirections['stdout'], 'w')
                        return f"Output redirected to {redirections['stdout']}"
                    elif 'stdout_append' in redirections:
                        self._write_to_file(output, redirections['stdout_append'], 'a')
                        return f"Output appended to {redirections['stdout_append']}"
                    
                    return output
                except Exception as e:
                    return f"Error executing command '{command}': {str(e)}"
            else:
                return f"Command not found: {command}"
                
        except ValueError as e:
            return f"Parse error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def _write_to_file(self, content: str, filename: str, mode: str):
        """Write content to file."""
        filepath = self.state.get_full_path(filename)
        try:
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(content)
                if not content.endswith('\n'):
                    f.write('\n')
        except Exception as e:
            raise Exception(f"Cannot write to file '{filename}': {str(e)}")
    
    def get_prompt(self) -> str:
        """Get the current terminal prompt."""
        return self.state.get_prompt()
    
    def is_running(self) -> bool:
        """Check if terminal is still running."""
        return self.running
    
    # Built-in command implementations
    def _help(self, args: List[str]) -> str:
        """Show help information."""
        if args:
            command = args[0]
            if command in self.commands:
                # Try to get docstring
                func = self.commands[command]
                doc = func.__doc__ or "No documentation available."
                return f"{command}: {doc}"
            else:
                return f"Unknown command: {command}"
        
        help_text = "Available commands:\n\n"
        help_text += "File Operations:\n"
        help_text += "  ls/dir        - List directory contents\n"
        help_text += "  cd            - Change directory\n"
        help_text += "  pwd           - Print working directory\n"
        help_text += "  mkdir/md      - Create directory\n"
        help_text += "  rmdir/rd      - Remove directory\n"
        help_text += "  rm/del        - Remove files\n"
        help_text += "  cp/copy       - Copy files\n"
        help_text += "  mv/move       - Move/rename files\n"
        help_text += "  touch         - Create empty file\n"
        help_text += "  cat/type      - Display file contents\n\n"
        help_text += "System Information:\n"
        help_text += "  ps            - Show processes\n"
        help_text += "  top           - Show system resources\n"
        help_text += "  df            - Show disk usage\n"
        help_text += "  free          - Show memory usage\n"
        help_text += "  whoami        - Show current user\n\n"
        help_text += "Built-in:\n"
        help_text += "  help          - Show this help\n"
        help_text += "  history       - Show command history\n"
        help_text += "  clear/cls     - Clear screen\n"
        help_text += "  exit/quit     - Exit terminal\n"
        help_text += "  echo          - Echo text\n"
        help_text += "  set           - Set environment variable\n"
        help_text += "  env           - Show environment variables\n"
        
        return help_text
    
    def _history(self, args: List[str]) -> str:
        """Show command history."""
        history_list = self.history.get_history()
        if not history_list:
            return "No commands in history."
        
        output = []
        for i, cmd in enumerate(history_list, 1):
            output.append(f"{i:4d}  {cmd}")
        
        return "\n".join(output)
    
    def _clear(self, args: List[str]) -> str:
        """Clear terminal screen."""
        # Return special marker for interface to handle
        return "__CLEAR_SCREEN__"
    
    def _exit(self, args: List[str]) -> str:
        """Exit the terminal."""
        self.running = False
        return "Goodbye!"
    
    def _echo(self, args: List[str]) -> str:
        """Echo the provided arguments."""
        return " ".join(args)
    
    def _set(self, args: List[str]) -> str:
        """Set environment variable."""
        if not args:
            # Show all environment variables
            return self._env(args)
        
        if len(args) == 1 and '=' in args[0]:
            # Handle SET VAR=VALUE format
            var, value = args[0].split('=', 1)
            self.state.set_env_var(var, value)
            return f"Set {var}={value}"
        elif len(args) >= 2:
            # Handle SET VAR VALUE format
            var = args[0]
            value = " ".join(args[1:])
            self.state.set_env_var(var, value)
            return f"Set {var}={value}"
        else:
            return "Usage: set VARIABLE=VALUE or set VARIABLE VALUE"
    
    def _env(self, args: List[str]) -> str:
        """Show environment variables."""
        env_vars = []
        for key, value in sorted(self.state.environment_vars.items()):
            env_vars.append(f"{key}={value}")
        return "\n".join(env_vars)