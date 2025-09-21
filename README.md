### 🚀 Python Terminal Emulator [Demo Link](https://python-terminal-emulator.vercel.app/)


A fully functioning command terminal emulator built in Python that mimics real system terminal behavior with cross-platform compatibility.

## ✨ Features

### Core Functionality

- 🗂️ **Complete File Operations**: `ls`, `cd`, `pwd`, `mkdir`, `rm`, `cp`, `mv`, `touch`, `cat`
- 🖥️ **System Monitoring**: `ps`, `top`, `df`, `free`, `whoami` with real-time data
- 🔧 **Built-in Commands**: `help`, `history`, `clear`, `exit`, `echo`, `set`, `env`
- 🌐 **Cross-platform**: Works on Windows, Linux, and macOS
- 🎯 **Windows Aliases**: `dir`, `copy`, `del`, `type`, `cls` for Windows users
- 📝 **Command History**: Session-based command tracking
- 🔀 **Output Redirection**: Basic file redirection support
- ⚡ **Error Handling**: Comprehensive error handling for invalid commands
- 🎨 **Clean CLI Interface**: Simple and intuitive command-line interface

## 🎮 Quick Start

### Prerequisites

- Python 3.7+
- psutil library (auto-installed)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ramgopal-m/python-terminal-emulator.git
   cd python-terminal-emulator
   ```

2. Run the terminal:
   ```bash
   python main.py
   ```

## 🎯 Demo & Usage

Run the included demo script to see all features in action:

```bash
python demo.py
```

### Example Commands

```bash
# File operations
ls -la                   # List files with details
mkdir test_folder        # Create directory
cd test_folder          # Change directory
touch example.txt       # Create file
echo "Hello World" > example.txt   # Write to file
cat example.txt         # Read file content

# System monitoring
ps                      # List running processes
top                     # System resource usage
df                      # Disk space information
free                    # Memory usage

# Utilities
history                 # Command history
help                    # Available commands
clear                   # Clear screen
```

## Usage

### CLI Terminal

```bash
python main.py
```

## 🏗️ Architecture

```
python_terminal/
├── main.py                    # Entry point
├── core/
│   └── terminal.py           # Main terminal engine
├── commands/
│   ├── file_ops.py          # File operations
│   └── system_info.py       # System monitoring
├── interfaces/
│   └── cli.py               # Command-line interface
├── utils/
│   ├── state.py             # Terminal state management
│   ├── command_parser.py    # Command parsing logic
│   └── history.py           # Command history
└── requirements.txt         # Dependencies
```

## 🔧 Supported Commands

### File Operations

| Command        | Description              | Examples                         |
| -------------- | ------------------------ | -------------------------------- |
| `ls` / `dir`   | List directory contents  | `ls`, `ls -la`, `dir`            |
| `cd`           | Change directory         | `cd folder`, `cd ..`, `cd /home` |
| `pwd`          | Print working directory  | `pwd`                            |
| `mkdir`        | Create directory         | `mkdir newfolder`                |
| `rm` / `del`   | Remove files/directories | `rm file.txt`, `del folder`      |
| `cp` / `copy`  | Copy files               | `cp source.txt dest.txt`         |
| `mv`           | Move/rename files        | `mv old.txt new.txt`             |
| `touch`        | Create empty file        | `touch newfile.txt`              |
| `cat` / `type` | Display file contents    | `cat file.txt`, `type file.txt`  |

### System Commands

| Command  | Description              |
| -------- | ------------------------ |
| `ps`     | List running processes   |
| `top`    | Display system resources |
| `df`     | Show disk space usage    |
| `free`   | Display memory usage     |
| `whoami` | Current user information |

### Built-in Commands

| Command         | Description                   |
| --------------- | ----------------------------- |
| `help`          | Show available commands       |
| `history`       | Display command history       |
| `clear` / `cls` | Clear terminal screen         |
| `exit` / `quit` | Exit terminal                 |
| `echo`          | Print text to output          |
| `set`           | Set environment variables     |
| `env`           | Display environment variables |

## 🚀 Deployment Options

### Web Deployment

- **Live Demo**: Download the executable from our [web interface](web/index.html)
- **Cloud Sharing**: Easy deployment to cloud platforms (see CLOUD_SHARING.md)

### Local Distribution

- **Standalone Executable**: Run without Python installation
- **Cross-platform**: Windows, Linux, and macOS support

## 🎮 SRM Hacks with CodeMate

This project was developed for the **SRM Hacks with CodeMate** competition, showcasing:

- **Innovation**: Complete terminal emulator built from scratch
- **Technical Excellence**: Modular architecture with comprehensive error handling
- **Cross-platform Compatibility**: Works seamlessly across operating systems
- **Real-world Utility**: Practical tool for developers and system administrators

### Competition Highlights

- ✅ Fully functional terminal with 20+ commands
- ✅ Real-time system monitoring capabilities
- ✅ Professional code architecture and documentation
- ✅ Comprehensive testing and demo scripts
- ✅ Web deployment interface for easy distribution

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🎯 Development Team

Developed by **Ramgopal M** for SRM Hacks with CodeMateai

---

_🏆 Built for SRM Hacks with CodeMate - Empowering developers with powerful terminal solutions_

- `ps` - Show running processes
- `top` - Show system resource usage
- `df` - Show disk usage
- `free` - Show memory usage
- `whoami` - Show current user

### Built-in Commands

- `help` - Show available commands
- `history` - Show command history
- `clear` - Clear terminal screen
- `exit` - Exit terminal

