# Weight-Loss-Challenge
A highly user friendly experience provided by the GUI that can be used for gathering contestant data for an annual Weight Loss Challenge.

## Project Structure

```
Weight-Loss-Challenge/
├── frontend/              # Python GUI (tkinter)
│   ├── main.py           # Main application
│   ├── backend_api.py    # Backend communication layer
│   ├── contestant_manager.py  # Business logic
│   ├── ui_components.py  # UI components
│   └── docs/             # Frontend documentation
│       ├── README.md     # Documentation index
│       ├── DEVELOPMENT.md    # Development setup
│       └── ARCHITECTURE.md   # Code architecture
├── backend/              # C backend
│   ├── weight_tracker.c  # C backend implementation
│   └── mock_backend.py   # Python mock for testing
├── shared/               # Shared resources
│   └── spec.md           # API specification
├── .vscode/              # VS Code settings
├── pyproject.toml        # Python tool config
├── .flake8               # Flake8 config
├── requirements-dev.txt  # Development dependencies
├── dev.bat               # Development commands (Windows)
└── README.md             # This file
```

## Setup Instructions

### Backend (C) - Samuel H.

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Compile the C program:
   ```bash
   gcc -Wall -Wextra -std=c11 -o weight_tracker.exe weight_tracker.c
   ```

3. Test the backend:
   ```bash
   .\weight_tracker.exe add "{\"name\":\"Test\",\"weight\":200.0}"
   .\weight_tracker.exe rankings
   ```

### Frontend (Python) - Johnathan H.

1. Ensure Python 3.11+ is installed (tkinter comes built-in)

2. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

3. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. Install development dependencies:
   ```bash
   pip install -r ../requirements-dev.txt
   ```

5. Run the application:
   ```bash
   python main.py
   ```

**For detailed setup and development information**, see [`frontend/docs/DEVELOPMENT.md`](./frontend/docs/DEVELOPMENT.md)

**For architecture and code structure**, see [`frontend/docs/ARCHITECTURE.md`](./frontend/docs/ARCHITECTURE.md)

## Quick Commands (Windows)

Use the `dev.bat` script for development tasks:

```batch
dev help           # Show all available commands
dev install        # Install development dependencies
dev run            # Run the application
dev format         # Format code with Black and isort
dev lint           # Check code style with Flake8
dev type-check     # Run MyPy type checking
dev check          # Run all checks (format + lint + type-check)
dev clean          # Clean cache directories
```

## How It Works

1. **Frontend (Python)**: 
   - Provides a user-friendly GUI using tkinter
   - Collects contestant data (name, weight)
   - Calls the C backend executable with commands
   - Displays results and rankings

2. **Backend (C)**:
   - Handles all data storage and calculations
   - Stores contestant data in binary file
   - Processes commands from frontend
   - Returns JSON responses

3. **Communication**:
   - Frontend calls backend via subprocess
   - Data exchanged in JSON format

## Features

- 

## Development Workflow

### For Frontend Development (Python)
- Work in the `frontend/` directory
- Modify `main.py` for GUI changes
- Test with the compiled backend

### For Backend Development (C)
- 

## Git Workflow

```bash
# Pull latest changes
git pull

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin feature/your-feature-name

# Create pull request on GitHub
```
