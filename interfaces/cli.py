"""
Simple command-line interface for the terminal.
"""
import os
import sys

# Handle both relative and absolute imports
try:
    from ..core.terminal import TerminalEngine
except ImportError:
    # Fallback for absolute imports when running directly
    from core.terminal import TerminalEngine


class CLIInterface:
    """Simple command-line interface for the Python terminal."""
    
    def __init__(self):
        self.terminal = TerminalEngine()
    
    def run(self):
        """Run the CLI terminal."""
        self._print_welcome()
        
        while self.terminal.is_running():
            try:
                # Get command input
                prompt_text = self.terminal.get_prompt()
                command_line = input(prompt_text)
                
                if command_line.strip():
                    output = self.terminal.execute_command(command_line)
                    
                    if output == "__CLEAR_SCREEN__":
                        self._clear_screen()
                    elif output:
                        print(output)
            
            except KeyboardInterrupt:
                # Handle Ctrl+C
                print("^C")
                continue
            except EOFError:
                # Handle Ctrl+D
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
        
        self._print_goodbye()
    
    def _print_welcome(self):
        """Print welcome message."""
        print("Welcome to Python Terminal Emulator")
        print("Type 'help' for available commands or 'exit' to quit.")
        print()
    
    def _print_goodbye(self):
        """Print goodbye message."""
        print("Goodbye!")
    
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Main entry point for CLI interface."""
    try:
        cli = CLIInterface()
        cli.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()