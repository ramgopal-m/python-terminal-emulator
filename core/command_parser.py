"""
Command parser - handles parsing of command line input into command and arguments.
"""
import shlex
from typing import List, Tuple, Optional


class CommandParser:
    """Parses command line input into command and arguments."""
    
    @staticmethod
    def parse(command_line: str) -> Tuple[Optional[str], List[str]]:
        """
        Parse command line input into command and arguments.
        
        Args:
            command_line: Raw command line input
            
        Returns:
            Tuple of (command, arguments_list)
        """
        if not command_line.strip():
            return None, []
        
        try:
            # Use shlex to properly handle quoted arguments
            tokens = shlex.split(command_line)
            if not tokens:
                return None, []
            
            command = tokens[0]
            args = tokens[1:] if len(tokens) > 1 else []
            
            return command, args
        except ValueError as e:
            # Handle cases like unclosed quotes
            raise ValueError(f"Invalid command syntax: {e}")
    
    @staticmethod
    def split_pipes(command_line: str) -> List[str]:
        """
        Split command line by pipes for future pipe support.
        Currently just returns the command as a single item.
        """
        # For now, return as single command
        # TODO: Implement proper pipe parsing
        return [command_line.strip()]
    
    @staticmethod
    def parse_redirections(args: List[str]) -> Tuple[List[str], dict]:
        """
        Parse output redirections from arguments.
        
        Args:
            args: List of arguments
            
        Returns:
            Tuple of (cleaned_args, redirections_dict)
        """
        cleaned_args = []
        redirections = {}
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg == '>':
                # Output redirection
                if i + 1 < len(args):
                    redirections['stdout'] = args[i + 1]
                    i += 2
                else:
                    raise ValueError("Missing filename for output redirection")
            elif arg == '>>':
                # Append redirection
                if i + 1 < len(args):
                    redirections['stdout_append'] = args[i + 1]
                    i += 2
                else:
                    raise ValueError("Missing filename for append redirection")
            elif arg == '<':
                # Input redirection
                if i + 1 < len(args):
                    redirections['stdin'] = args[i + 1]
                    i += 2
                else:
                    raise ValueError("Missing filename for input redirection")
            elif arg.startswith('>'):
                # Handle >filename format
                redirections['stdout'] = arg[1:]
                i += 1
            elif arg.startswith('>>'):
                # Handle >>filename format
                redirections['stdout_append'] = arg[2:]
                i += 1
            else:
                cleaned_args.append(arg)
                i += 1
        
        return cleaned_args, redirections