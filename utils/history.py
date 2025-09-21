"""
Command history management.
"""
import os
import json
from typing import List
from datetime import datetime


class CommandHistory:
    """Manages command history storage and retrieval."""
    
    def __init__(self, max_history: int = 1000, history_file: str = None):
        self.max_history = max_history
        self.history = []
        
        # Default history file location
        if history_file is None:
            home_dir = os.path.expanduser("~")
            self.history_file = os.path.join(home_dir, ".python_terminal_history")
        else:
            self.history_file = history_file
        
        self._load_history()
    
    def add(self, command: str):
        """Add a command to history."""
        if command.strip() and (not self.history or self.history[-1] != command):
            self.history.append(command)
            
            # Trim history if it exceeds max size
            if len(self.history) > self.max_history:
                self.history = self.history[-self.max_history:]
            
            self._save_history()
    
    def get_history(self) -> List[str]:
        """Get the complete command history."""
        return self.history.copy()
    
    def get_recent(self, count: int = 10) -> List[str]:
        """Get the most recent commands."""
        return self.history[-count:] if count <= len(self.history) else self.history.copy()
    
    def search(self, pattern: str) -> List[str]:
        """Search for commands containing the pattern."""
        return [cmd for cmd in self.history if pattern.lower() in cmd.lower()]
    
    def clear(self):
        """Clear the command history."""
        self.history = []
        self._save_history()
    
    def _load_history(self):
        """Load history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.history = data.get('commands', [])
        except (IOError, json.JSONDecodeError):
            # If file doesn't exist or is corrupted, start with empty history
            self.history = []
    
    def _save_history(self):
        """Save history to file."""
        try:
            data = {
                'commands': self.history,
                'last_saved': datetime.now().isoformat()
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError:
            # Silently fail if we can't write to history file
            pass