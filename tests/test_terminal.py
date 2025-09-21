"""
Basic tests for the Python Terminal system.
"""
import unittest
import tempfile
import os
import shutil
from unittest.mock import Mock, patch

# Add parent directory to path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.terminal import TerminalEngine
from core.state import TerminalState
from core.command_parser import CommandParser
from commands.file_ops import FileOperations
from utils.history import CommandHistory


class TestTerminalState(unittest.TestCase):
    """Test terminal state management."""
    
    def setUp(self):
        self.state = TerminalState()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_current_directory(self):
        """Test current directory management."""
        initial_dir = self.state.get_current_directory()
        self.assertTrue(os.path.isdir(initial_dir))
        
        # Test changing to test directory
        success = self.state.set_current_directory(self.test_dir)
        self.assertTrue(success)
        self.assertEqual(self.state.get_current_directory(), self.test_dir)
        
        # Test changing to non-existent directory
        success = self.state.set_current_directory("/non/existent/path")
        self.assertFalse(success)
        self.assertEqual(self.state.get_current_directory(), self.test_dir)
    
    def test_environment_variables(self):
        """Test environment variable management."""
        self.state.set_env_var("TEST_VAR", "test_value")
        self.assertEqual(self.state.get_env_var("TEST_VAR"), "test_value")
        
        # Check that it's also set in os.environ
        self.assertEqual(os.environ.get("TEST_VAR"), "test_value")
    
    def test_prompt_generation(self):
        """Test prompt string generation."""
        prompt = self.state.get_prompt()
        self.assertIn("@", prompt)
        self.assertIn("$", prompt)
        self.assertIsInstance(prompt, str)


class TestCommandParser(unittest.TestCase):
    """Test command parsing functionality."""
    
    def test_basic_parsing(self):
        """Test basic command parsing."""
        command, args = CommandParser.parse("ls -la /tmp")
        self.assertEqual(command, "ls")
        self.assertEqual(args, ["-la", "/tmp"])
    
    def test_quoted_arguments(self):
        """Test parsing with quoted arguments."""
        command, args = CommandParser.parse('cp "file with spaces.txt" destination')
        self.assertEqual(command, "cp")
        self.assertEqual(args, ["file with spaces.txt", "destination"])
    
    def test_empty_command(self):
        """Test parsing empty command."""
        command, args = CommandParser.parse("")
        self.assertIsNone(command)
        self.assertEqual(args, [])
    
    def test_redirections(self):
        """Test redirection parsing."""
        args = ["ls", "-l", ">", "output.txt"]
        cleaned_args, redirections = CommandParser.parse_redirections(args)
        self.assertEqual(cleaned_args, ["ls", "-l"])
        self.assertEqual(redirections, {"stdout": "output.txt"})


class TestFileOperations(unittest.TestCase):
    """Test file operations commands."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.state = TerminalState()
        self.state.set_current_directory(self.test_dir)
        self.file_ops = FileOperations(self.state)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_mkdir(self):
        """Test directory creation."""
        result = self.file_ops.mkdir(["test_folder"])
        self.assertEqual(result, "")
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "test_folder")))
    
    def test_touch(self):
        """Test file creation."""
        result = self.file_ops.touch(["test_file.txt"])
        self.assertEqual(result, "")
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "test_file.txt")))
    
    def test_ls(self):
        """Test directory listing."""
        # Create test files
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        result = self.file_ops.ls([])
        self.assertIn("test.txt", result)
    
    def test_cd(self):
        """Test directory changing."""
        # Create subdirectory
        sub_dir = os.path.join(self.test_dir, "subdir")
        os.mkdir(sub_dir)
        
        result = self.file_ops.cd(["subdir"])
        self.assertEqual(result, "")
        self.assertEqual(self.state.get_current_directory(), sub_dir)
    
    def test_rm(self):
        """Test file removal."""
        # Create test file
        test_file = os.path.join(self.test_dir, "to_delete.txt")
        with open(test_file, 'w') as f:
            f.write("delete me")
        
        result = self.file_ops.rm(["to_delete.txt"])
        self.assertEqual(result, "")
        self.assertFalse(os.path.exists(test_file))


class TestCommandHistory(unittest.TestCase):
    """Test command history functionality."""
    
    def setUp(self):
        self.history_file = tempfile.mktemp()
        self.history = CommandHistory(history_file=self.history_file)
    
    def tearDown(self):
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
    
    def test_add_command(self):
        """Test adding commands to history."""
        self.history.add("ls -la")
        self.history.add("cd /tmp")
        
        history_list = self.history.get_history()
        self.assertEqual(len(history_list), 2)
        self.assertEqual(history_list[0], "ls -la")
        self.assertEqual(history_list[1], "cd /tmp")
    
    def test_duplicate_commands(self):
        """Test that duplicate consecutive commands are not added."""
        self.history.add("ls")
        self.history.add("ls")
        
        history_list = self.history.get_history()
        self.assertEqual(len(history_list), 1)
    
    def test_search_history(self):
        """Test searching command history."""
        self.history.add("ls -la")
        self.history.add("cd /tmp")
        self.history.add("ls /home")
        
        results = self.history.search("ls")
        self.assertEqual(len(results), 2)
        self.assertIn("ls -la", results)
        self.assertIn("ls /home", results)


class TestTerminalEngine(unittest.TestCase):
    """Test the main terminal engine."""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.terminal = TerminalEngine()
        self.terminal.state.set_current_directory(self.test_dir)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_execute_basic_command(self):
        """Test executing basic commands."""
        result = self.terminal.execute_command("pwd")
        self.assertEqual(result.strip(), self.test_dir)
    
    def test_execute_help_command(self):
        """Test help command."""
        result = self.terminal.execute_command("help")
        self.assertIn("Available commands", result)
        self.assertIn("File Operations", result)
    
    def test_execute_invalid_command(self):
        """Test executing invalid command."""
        result = self.terminal.execute_command("invalid_command")
        self.assertIn("Command not found", result)
    
    def test_command_history(self):
        """Test that commands are added to history."""
        self.terminal.execute_command("pwd")
        self.terminal.execute_command("ls")
        
        history = self.terminal.history.get_history()
        self.assertIn("pwd", history)
        self.assertIn("ls", history)
    
    def test_empty_command(self):
        """Test executing empty command."""
        result = self.terminal.execute_command("")
        self.assertEqual(result, "")
    
    def test_echo_command(self):
        """Test echo command."""
        result = self.terminal.execute_command("echo hello world")
        self.assertEqual(result, "hello world")


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)