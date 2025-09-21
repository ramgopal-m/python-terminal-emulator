"""
Demo script to showcase Python Terminal functionality.
"""
import sys
import os
import time

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.terminal import TerminalEngine


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demo_command(terminal, command, description=""):
    """Execute and display a command with description."""
    if description:
        print(f"\n💡 {description}")
    
    print(f"\n{terminal.get_prompt()}{command}")
    
    result = terminal.execute_command(command)
    if result:
        print(result)
    
    time.sleep(1)  # Pause for readability


def main():
    """Run the terminal demo."""
    print("🚀 Python Terminal Emulator Demo")
    print("This demo showcases the various features of the terminal.")
    print("\nPress Enter to continue...")
    input()
    
    # Initialize terminal
    terminal = TerminalEngine()
    
    # File Operations Demo
    print_header("FILE OPERATIONS DEMO")
    
    demo_command(terminal, "pwd", "Show current working directory")
    demo_command(terminal, "ls", "List current directory contents")
    demo_command(terminal, "mkdir demo_folder", "Create a new directory")
    demo_command(terminal, "cd demo_folder", "Change to the new directory")
    demo_command(terminal, "pwd", "Verify we're in the new directory")
    demo_command(terminal, "touch demo_file.txt", "Create an empty file")
    demo_command(terminal, "echo 'Hello, World!' > hello.txt", "Create file with content using redirection")
    demo_command(terminal, "ls -l", "List files with detailed information")
    demo_command(terminal, "cat hello.txt", "Display file contents")
    demo_command(terminal, "cp hello.txt backup.txt", "Copy file")
    demo_command(terminal, "mv backup.txt renamed.txt", "Rename/move file")
    demo_command(terminal, "ls", "Show updated directory contents")
    
    # System Information Demo
    print_header("SYSTEM INFORMATION DEMO")
    
    demo_command(terminal, "whoami", "Show current user")
    demo_command(terminal, "free -h", "Show memory usage in human-readable format")
    demo_command(terminal, "df -h", "Show disk usage")
    demo_command(terminal, "ps", "Show running processes (limited view)")
    demo_command(terminal, "top", "Show system resource usage")
    
    # Environment and Built-in Commands Demo
    print_header("ENVIRONMENT & BUILT-IN COMMANDS DEMO")
    
    demo_command(terminal, "set DEMO_VAR hello_world", "Set an environment variable")
    demo_command(terminal, "echo $DEMO_VAR", "Note: Variable expansion not implemented in echo")
    demo_command(terminal, "env | grep DEMO", "Note: Pipe operations not implemented")
    demo_command(terminal, "history", "Show command history")
    demo_command(terminal, "help", "Show available commands")
    
    # AI Commands Demo (if available)
    print_header("BASIC COMMAND DEMONSTRATIONS")
    
    demo_command(terminal, "help", "Show all available commands")
    demo_command(terminal, "echo 'This is a basic terminal implementation'", "Echo a message")
    demo_command(terminal, "set DEMO_VAR=basic_terminal", "Set environment variable")
    demo_command(terminal, "env | findstr DEMO", "Note: Advanced piping not implemented")
    
    # Cleanup Demo
    print_header("CLEANUP DEMO")
    
    demo_command(terminal, "cd ..", "Go back to parent directory")
    demo_command(terminal, "rm -r demo_folder", "Remove demo directory and contents")
    demo_command(terminal, "ls", "Verify cleanup")
    
    # Conclusion
    print_header("DEMO COMPLETE")
    print("\n✅ Demo completed successfully!")
    print("\nKey Features Demonstrated:")
    print("• Complete file and directory operations")
    print("• System monitoring and information")
    print("• Command history and environment variables")
    print("• Error handling and user-friendly output")
    print("• Cross-platform compatibility")
    
    print("\nTo use the terminal interactively:")
    print("• CLI Mode: python main.py")
    print("• Run Tests: python tests/test_terminal.py")
    
    print("\nThank you for trying the Python Terminal Emulator! 🎉")


if __name__ == "__main__":
    main()