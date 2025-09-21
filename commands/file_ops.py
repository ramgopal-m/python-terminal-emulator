"""
File and directory operations commands.
"""
import os
import shutil
import stat
import glob
from typing import List
from datetime import datetime

# Handle both relative and absolute imports
try:
    from .base import BaseCommand
except ImportError:
    # Fallback for absolute imports when running directly
    from commands.base import BaseCommand


class FileOperations:
    """Handles file and directory operations."""
    
    def __init__(self, terminal_state):
        self.state = terminal_state
    
    def ls(self, args: List[str]) -> str:
        """List directory contents."""
        try:
            # Parse arguments
            show_hidden = False
            show_long = False
            paths = []
            
            for arg in args:
                if arg.startswith('-'):
                    if 'a' in arg:
                        show_hidden = True
                    if 'l' in arg:
                        show_long = True
                else:
                    paths.append(arg)
            
            # Default to current directory if no paths specified
            if not paths:
                paths = [self.state.current_directory]
            
            output = []
            for path in paths:
                full_path = self.state.get_full_path(path)
                
                if not os.path.exists(full_path):
                    output.append(f"ls: cannot access '{path}': No such file or directory")
                    continue
                
                if os.path.isfile(full_path):
                    # Single file
                    if show_long:
                        output.append(self._format_long_listing([full_path]))
                    else:
                        output.append(os.path.basename(full_path))
                else:
                    # Directory
                    try:
                        items = os.listdir(full_path)
                        if not show_hidden:
                            items = [item for item in items if not item.startswith('.')]
                        
                        items.sort()
                        
                        if show_long:
                            item_paths = [os.path.join(full_path, item) for item in items]
                            output.append(self._format_long_listing(item_paths))
                        else:
                            # Format in columns
                            if items:
                                # Simple column formatting
                                max_width = max(len(item) for item in items) if items else 0
                                cols = max(1, 80 // (max_width + 2))
                                
                                formatted_items = []
                                for i, item in enumerate(items):
                                    if os.path.isdir(os.path.join(full_path, item)):
                                        item += "/"
                                    formatted_items.append(item.ljust(max_width + 2))
                                    
                                    if (i + 1) % cols == 0:
                                        formatted_items.append("\n")
                                
                                output.append("".join(formatted_items).rstrip())
                            else:
                                output.append("")
                    except PermissionError:
                        output.append(f"ls: cannot open directory '{path}': Permission denied")
            
            return "\n".join(output)
        except Exception as e:
            return f"ls: {str(e)}"
    
    def _format_long_listing(self, paths: List[str]) -> str:
        """Format files in long listing format."""
        lines = []
        for path in paths:
            try:
                stat_info = os.stat(path)
                
                # File type and permissions
                mode = stat_info.st_mode
                if stat.S_ISDIR(mode):
                    file_type = 'd'
                elif stat.S_ISLNK(mode):
                    file_type = 'l'
                else:
                    file_type = '-'
                
                # Permissions (simplified)
                perms = file_type
                perms += 'r' if mode & stat.S_IRUSR else '-'
                perms += 'w' if mode & stat.S_IWUSR else '-'
                perms += 'x' if mode & stat.S_IXUSR else '-'
                perms += 'r' if mode & stat.S_IRGRP else '-'
                perms += 'w' if mode & stat.S_IWGRP else '-'
                perms += 'x' if mode & stat.S_IXGRP else '-'
                perms += 'r' if mode & stat.S_IROTH else '-'
                perms += 'w' if mode & stat.S_IWOTH else '-'
                perms += 'x' if mode & stat.S_IXOTH else '-'
                
                # Size
                size = stat_info.st_size
                
                # Modification time
                mtime = datetime.fromtimestamp(stat_info.st_mtime)
                time_str = mtime.strftime("%b %d %H:%M")
                
                # File name
                name = os.path.basename(path)
                
                lines.append(f"{perms} {size:>8} {time_str} {name}")
            except (OSError, IOError):
                lines.append(f"????????? ? ? ? {os.path.basename(path)}")
        
        return "\n".join(lines)
    
    def cd(self, args: List[str]) -> str:
        """Change directory."""
        if not args:
            # Go to home directory
            home = os.path.expanduser("~")
            if self.state.set_current_directory(home):
                return ""
            else:
                return "cd: cannot change to home directory"
        
        path = args[0]
        
        if path == "-":
            # TODO: Implement previous directory functionality
            return "cd: OLDPWD not set"
        
        if self.state.set_current_directory(path):
            return ""
        else:
            return f"cd: no such file or directory: {path}"
    
    def pwd(self, args: List[str]) -> str:
        """Print working directory."""
        return self.state.current_directory
    
    def mkdir(self, args: List[str]) -> str:
        """Create directory."""
        if not args:
            return "mkdir: missing operand"
        
        create_parents = False
        dirs_to_create = []
        
        for arg in args:
            if arg == '-p':
                create_parents = True
            elif arg.startswith('-'):
                return f"mkdir: invalid option: {arg}"
            else:
                dirs_to_create.append(arg)
        
        if not dirs_to_create:
            return "mkdir: missing operand"
        
        results = []
        for dir_name in dirs_to_create:
            full_path = self.state.get_full_path(dir_name)
            try:
                if create_parents:
                    os.makedirs(full_path, exist_ok=True)
                else:
                    os.mkdir(full_path)
            except FileExistsError:
                results.append(f"mkdir: cannot create directory '{dir_name}': File exists")
            except OSError as e:
                results.append(f"mkdir: cannot create directory '{dir_name}': {str(e)}")
        
        return "\n".join(results) if results else ""
    
    def rmdir(self, args: List[str]) -> str:
        """Remove empty directory."""
        if not args:
            return "rmdir: missing operand"
        
        results = []
        for dir_name in args:
            if dir_name.startswith('-'):
                results.append(f"rmdir: invalid option: {dir_name}")
                continue
                
            full_path = self.state.get_full_path(dir_name)
            try:
                os.rmdir(full_path)
            except OSError as e:
                results.append(f"rmdir: failed to remove '{dir_name}': {str(e)}")
        
        return "\n".join(results) if results else ""
    
    def rm(self, args: List[str]) -> str:
        """Remove files and directories."""
        if not args:
            return "rm: missing operand"
        
        recursive = False
        force = False
        files_to_remove = []
        
        for arg in args:
            if arg == '-r' or arg == '-R':
                recursive = True
            elif arg == '-f':
                force = True
            elif arg == '-rf' or arg == '-fr':
                recursive = True
                force = True
            elif arg.startswith('-'):
                return f"rm: invalid option: {arg}"
            else:
                files_to_remove.append(arg)
        
        if not files_to_remove:
            return "rm: missing operand"
        
        results = []
        for file_name in files_to_remove:
            full_path = self.state.get_full_path(file_name)
            try:
                if os.path.isdir(full_path):
                    if recursive:
                        shutil.rmtree(full_path)
                    else:
                        results.append(f"rm: cannot remove '{file_name}': Is a directory")
                else:
                    os.remove(full_path)
            except FileNotFoundError:
                if not force:
                    results.append(f"rm: cannot remove '{file_name}': No such file or directory")
            except OSError as e:
                if not force:
                    results.append(f"rm: cannot remove '{file_name}': {str(e)}")
        
        return "\n".join(results) if results else ""
    
    def cp(self, args: List[str]) -> str:
        """Copy files and directories."""
        if len(args) < 2:
            return "cp: missing file operand"
        
        recursive = False
        source_files = []
        
        for arg in args[:-1]:
            if arg == '-r' or arg == '-R':
                recursive = True
            elif arg.startswith('-'):
                return f"cp: invalid option: {arg}"
            else:
                source_files.append(arg)
        
        if not source_files:
            return "cp: missing file operand"
        
        destination = args[-1]
        dest_path = self.state.get_full_path(destination)
        
        results = []
        for source in source_files:
            source_path = self.state.get_full_path(source)
            
            try:
                if not os.path.exists(source_path):
                    results.append(f"cp: cannot stat '{source}': No such file or directory")
                    continue
                
                if os.path.isdir(source_path):
                    if not recursive:
                        results.append(f"cp: -r not specified; omitting directory '{source}'")
                        continue
                    
                    # Directory copy
                    if os.path.isdir(dest_path):
                        final_dest = os.path.join(dest_path, os.path.basename(source_path))
                    else:
                        final_dest = dest_path
                    
                    shutil.copytree(source_path, final_dest)
                else:
                    # File copy
                    if os.path.isdir(dest_path):
                        final_dest = os.path.join(dest_path, os.path.basename(source_path))
                    else:
                        final_dest = dest_path
                    
                    shutil.copy2(source_path, final_dest)
            except OSError as e:
                results.append(f"cp: cannot copy '{source}': {str(e)}")
        
        return "\n".join(results) if results else ""
    
    def mv(self, args: List[str]) -> str:
        """Move/rename files and directories."""
        if len(args) < 2:
            return "mv: missing file operand"
        
        source_files = args[:-1]
        destination = args[-1]
        dest_path = self.state.get_full_path(destination)
        
        results = []
        for source in source_files:
            source_path = self.state.get_full_path(source)
            
            try:
                if not os.path.exists(source_path):
                    results.append(f"mv: cannot stat '{source}': No such file or directory")
                    continue
                
                if os.path.isdir(dest_path) and len(source_files) > 1:
                    final_dest = os.path.join(dest_path, os.path.basename(source_path))
                else:
                    final_dest = dest_path
                
                shutil.move(source_path, final_dest)
            except OSError as e:
                results.append(f"mv: cannot move '{source}': {str(e)}")
        
        return "\n".join(results) if results else ""
    
    def touch(self, args: List[str]) -> str:
        """Create empty file or update timestamp."""
        if not args:
            return "touch: missing file operand"
        
        results = []
        for filename in args:
            if filename.startswith('-'):
                results.append(f"touch: invalid option: {filename}")
                continue
            
            full_path = self.state.get_full_path(filename)
            try:
                if os.path.exists(full_path):
                    # Update timestamp
                    os.utime(full_path, None)
                else:
                    # Create empty file
                    with open(full_path, 'w'):
                        pass
            except OSError as e:
                results.append(f"touch: cannot touch '{filename}': {str(e)}")
        
        return "\n".join(results) if results else ""
    
    def cat(self, args: List[str]) -> str:
        """Display file contents."""
        if not args:
            return "cat: missing file operand"
        
        output = []
        for filename in args:
            if filename.startswith('-'):
                output.append(f"cat: invalid option: {filename}")
                continue
            
            full_path = self.state.get_full_path(filename)
            try:
                if os.path.isdir(full_path):
                    output.append(f"cat: {filename}: Is a directory")
                else:
                    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                        output.append(content.rstrip('\n'))  # Remove trailing newline
            except FileNotFoundError:
                output.append(f"cat: {filename}: No such file or directory")
            except PermissionError:
                output.append(f"cat: {filename}: Permission denied")
            except Exception as e:
                output.append(f"cat: {filename}: {str(e)}")
        
        return "\n".join(output)