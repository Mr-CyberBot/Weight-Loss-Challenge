# Weight-Loss-Challenge
A highly user friendly experience provided by the GUI that can be used for gathering contestant data for an annual Weight Loss Challenge.

## Project Structure

```
Weight-Loss-Challenge/
├── frontend/           # Python GUI (tkinter)
│   ├── main.py        # Main application
│   └── requirements.txt
├── backend/           # C backend
│   ├── weight_tracker.c
│   ├── Makefile
│   └── contestants.dat (generated)
├── shared/            # Shared documentation
│   └── spec.md    # API specification
└── README.md
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
   Or use the Makefile:
   ```bash
   make
   ```

3. Test the backend:
   ```bash
   .\weight_tracker.exe add "{\"name\":\"Test\",\"weight\":200.0}"
   .\weight_tracker.exe rankings
   ```

### Frontend (Python) - Johnathan H.

1. Ensure Python 3.x is installed (tkinter comes built-in)

2. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

3. Run the application:
   ```bash
   python main.py
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
