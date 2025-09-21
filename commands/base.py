"""
Base command class for all terminal commands.
"""
from abc import ABC, abstractmethod
from typing import List, Any


class BaseCommand(ABC):
    """Base class for all terminal commands."""
    
    def __init__(self, terminal_state=None):
        self.terminal_state = terminal_state
    
    @abstractmethod
    def execute(self, args: List[str]) -> str:
        """
        Execute the command with given arguments.
        
        Args:
            args: List of command arguments
            
        Returns:
            String output of the command
        """
        pass
    
    def validate_args(self, args: List[str], min_args: int = 0, max_args: int = None) -> bool:
        """
        Validate command arguments.
        
        Args:
            args: Command arguments
            min_args: Minimum required arguments
            max_args: Maximum allowed arguments (None for unlimited)
            
        Returns:
            True if arguments are valid
            
        Raises:
            ValueError: If arguments are invalid
        """
        if len(args) < min_args:
            raise ValueError(f"Not enough arguments. Expected at least {min_args}, got {len(args)}")
        
        if max_args is not None and len(args) > max_args:
            raise ValueError(f"Too many arguments. Expected at most {max_args}, got {len(args)}")
        
        return True
    
    def format_error(self, message: str) -> str:
        """Format error message."""
        return f"Error: {message}"
    
    def format_success(self, message: str) -> str:
        """Format success message."""
        return message


class CommandRegistry:
    """Registry for managing available commands."""
    
    def __init__(self):
        self.commands = {}
    
    def register(self, name: str, command_func):
        """Register a command function."""
        self.commands[name] = command_func
    
    def unregister(self, name: str):
        """Unregister a command."""
        if name in self.commands:
            del self.commands[name]
    
    def get_command(self, name: str):
        """Get a command function by name."""
        return self.commands.get(name)
    
    def list_commands(self) -> List[str]:
        """List all registered command names."""
        return list(self.commands.keys())
    
    def command_exists(self, name: str) -> bool:
        """Check if a command exists."""
        return name in self.commands