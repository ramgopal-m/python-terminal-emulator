"""
Terminal state management - handles current directory, environment variables, etc.
"""
import os
from typing import Dict, Any


class TerminalState:
    """Manages the current state of the terminal session."""
    
    def __init__(self):
        self.current_directory = os.getcwd()
        self.environment_vars = dict(os.environ)
        self.user = os.getenv('USERNAME', os.getenv('USER', 'user'))
        self.hostname = os.getenv('COMPUTERNAME', os.getenv('HOSTNAME', 'localhost'))
    
    def get_current_directory(self) -> str:
        """Get the current working directory."""
        return self.current_directory
    
    def set_current_directory(self, path: str) -> bool:
        """
        Set the current working directory.
        Returns True if successful, False otherwise.
        """
        try:
            # Resolve path relative to current directory
            if not os.path.isabs(path):
                new_path = os.path.join(self.current_directory, path)
            else:
                new_path = path
            
            # Normalize the path
            new_path = os.path.normpath(new_path)
            
            # Check if directory exists
            if os.path.isdir(new_path):
                self.current_directory = new_path
                return True
            else:
                return False
        except (OSError, IOError):
            return False
    
    def get_env_var(self, name: str) -> str:
        """Get environment variable value."""
        return self.environment_vars.get(name, '')
    
    def set_env_var(self, name: str, value: str):
        """Set environment variable."""
        self.environment_vars[name] = value
        os.environ[name] = value
    
    def get_prompt(self) -> str:
        """Generate terminal prompt string."""
        # Get current directory name (last part of path)
        current_dir = os.path.basename(self.current_directory) or self.current_directory
        return f"{self.user}@{self.hostname}:{current_dir}$ "
    
    def get_full_path(self, path: str) -> str:
        """Convert relative path to absolute path based on current directory."""
        if os.path.isabs(path):
            return os.path.normpath(path)
        else:
            return os.path.normpath(os.path.join(self.current_directory, path))