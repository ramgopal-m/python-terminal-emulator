# 🚀 Vercel Deployment Guide - Python Terminal Emulator

## 📋 Quick Deployment Steps

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Login to Vercel

```bash
vercel login
```

### 3. Deploy from Project Directory

```bash
cd python_terminal
vercel
```

### 4. Production Deployment

```bash
vercel --prod
```

## 🌐 Live URLs

After deployment, you'll get URLs like:

- **Development**: `https://python-terminal-emulator-username.vercel.app/`
- **Production**: `https://python-terminal-emulator.vercel.app/`

## 📁 Project Structure for Vercel

```
python_terminal/
├── index.html              # Frontend web terminal
├── api/
│   └── terminal.py         # Python backend API
├── vercel.json            # Vercel configuration
├── package.json           # NPM configuration
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## 🔧 Configuration Files

### vercel.json

- Configures Python runtime for API routes
- Sets up static file serving for frontend
- Defines routing rules

### package.json

- NPM configuration for Vercel CLI
- Project metadata and scripts

### requirements.txt

- Python dependencies (psutil for system monitoring)

## 🎯 Features

### Frontend (index.html)

- Interactive web-based terminal interface
- Real terminal look and feel
- Command history and navigation
- Responsive design

### Backend (api/terminal.py)

- Python serverless functions
- Real system monitoring with psutil
- Process listing, memory usage, disk info
- Cross-platform compatibility

## 🧪 Testing Locally

```bash
# Install Vercel CLI
npm install -g vercel

# Start development server
vercel dev

# Open browser to http://localhost:3000
```

## 🎮 Available Commands

### Web Terminal Commands:

- `help` - Show all commands
- `ls`, `dir` - List files
- `cd` - Change directory
- `pwd` - Current directory
- `mkdir` - Create directory
- `touch` - Create file
- `cat` - Read file
- `echo` - Display text
- `history` - Command history
- `clear` - Clear screen

### System Commands (via API):

- `ps` - List processes
- `top` - System information
- `df` - Disk usage
- `free` - Memory information
- `whoami` - Current user
- `date` - Current date/time

## 🔒 Security Notes

- API endpoints are sandboxed in Vercel serverless environment
- No file system persistence between requests
- Safe execution environment for system commands

## 🏆 Competition Features

- ✅ **Live Hosted URL** - Perfect for CodeMate submission
- ✅ **Interactive Demo** - Judges can test commands
- ✅ **Professional Interface** - Clean, modern design
- ✅ **Real System Data** - Actual process and memory info
- ✅ **Cross-platform** - Works on any device with browser

## 📱 Mobile Responsive

The terminal interface is fully responsive and works on:

- Desktop computers
- Tablets
- Mobile devices
- Any device with a modern web browser

## 🎯 Submission Ready

This Vercel deployment provides:

1. **Live working URL** ✅
2. **Interactive demonstration** ✅
3. **Professional presentation** ✅
4. **Easy judge access** ✅
5. **No installation required** ✅

Perfect for SRM Hacks with CodeMate submission requirements!
