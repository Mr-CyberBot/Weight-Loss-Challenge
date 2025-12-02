# Weight-Loss-Challenge

A user-friendly GUI application for managing an annual Weight Loss Challenge. Track contestants, monitor progress, and view rankings.

## Project Structure

```
Weight-Loss-Challenge/
├── frontend/                 # Python GUI & data management
│   ├── main.py               # Main application entry point
│   ├── backend_api.py        # Data management & C backend calls
│   ├── contestant_manager.py # Business logic
│   ├── ui_components.py      # Reusable UI components
│   ├── contestants.json      # Data storage (JSON)
│   └── requirements.txt      # Python dependencies
├── backend/                  # C calculator backend
│   ├── data-manipulator.c      # C source code (age & weight calculations)
│   ├── data-manipulator.exe    # Compiled executable
│   └── Makefile              # Build configuration
├── shared/                   # Shared resources
│   └── spec.md               # API specification
└── .vscode/                  # VS Code configuration
    └── settings.json         # Auto-format & linting on save
```

## Quick Start

### 1. Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies (including linting tools)
pip install -r frontend\requirements.txt
```

### 2. Compile C Backend (Optional)

The C backend provides faster calculations. If not compiled, Python fallback is used.

```powershell
cd backend
gcc -Wall -Wextra -std=c11 -o data-manipulator.exe data-manipulator.c

# Or use Make
make
```

Test it:
```powershell
.\data-manipulator.exe age 1990-05-15
.\data-manipulator.exe weight_lost 200.0 190.0
```

### 3. Run Application

```powershell
python frontend\main.py
```

## VS Code Setup (Auto-Linting)

**The project is already configured!** When you open Python files in VS Code:

✅ **Auto-format on save** (Black formatter, 100 char line length)  
✅ **Auto-organize imports** (isort)  
✅ **Flake8 linting** (shows errors/warnings in editor)  
✅ **MyPy type checking** (optional static typing)

**Required VS Code Extensions:**
- Python (ms-python.python)
- Black Formatter (ms-python.black-formatter)
- Flake8 (ms-python.flake8)

Install dependencies to enable linting:
```powershell
pip install -r frontend\requirements.txt
```

All settings are in `.vscode/settings.json` - no additional configuration needed!

## Architecture

**Separation of Concerns:**
- **Python Frontend**: Handles all data (JSON), UI, business logic
- **C Backend**: Pure calculator (age, weight loss, percentages)
- **Communication**: Python calls C backend via subprocess for calculations

**Data Flow:**
```
User Input → Python GUI → Save to contestants.json
                ↓
         Call C backend for calculations (if available)
                ↓
         Python fallback if C not compiled
                ↓
         Display results in GUI
```

## Features

- ✅ Add contestants (name, date of birth, starting weight)
- ✅ Update current weight
- ✅ Automatic age calculation
- ✅ Weight loss statistics (pounds lost, percentage)
- ✅ Rankings sorted by percentage lost
- ✅ Edit contestant information
- ✅ Delete contestants
- ✅ Persistent JSON storage
- ✅ Auto-populate fields on selection

## Development

**Python Development:**
- Work in `frontend/` directory
- Code is auto-formatted on save (Black, isort)
- Linting shows issues in real-time (Flake8)
- All data operations are in `backend_api.py`

**C Development:**
- Work in `backend/` directory
- Only handles calculations (no JSON, no file I/O)
- Compile with `gcc` or `make`
- Test with command-line arguments

**Code Quality:**
```powershell
# Format code
black frontend --line-length=100

# Check linting
flake8 frontend --max-line-length=100

# Type check
mypy frontend
```

## Git Workflow

```powershell
# Pull latest changes
git pull

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, auto-format on save

# Commit
git add .
git commit -m "feat: description of changes"

# Push
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Data Storage

- **File**: `frontend/contestants.json`
- **Format**: JSON (human-readable)
- **Contents**: All contestant data (name, DOB, age, weights, statistics)
- **Managed by**: Python frontend (`backend_api.py`)
- **Ignored by Git**: Listed in `.gitignore` to prevent committing user data

## Troubleshooting

**Application won't start:**
- Ensure virtual environment is activated
- Install dependencies: `pip install -r frontend\requirements.txt`

**C backend not working:**
- Check if `data-manipulator.exe` exists in `backend/` folder
- If missing, app will use Python fallback (slightly slower)
- Recompile: `gcc -Wall -Wextra -std=c11 -o data-manipulator.exe data-manipulator.c`

**Linting not working in VS Code:**
- Install required VS Code extensions (Python, Black, Flake8)
- Install tools: `pip install -r frontend\requirements.txt`
- Restart VS Code
