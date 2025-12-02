@echo off
REM Weight Loss Challenge - Development Commands for Windows
REM Usage: dev.bat [command]
REM
REM Commands:
REM   help        - Show this help message
REM   install     - Install development dependencies
REM   format      - Format code with Black and isort
REM   lint        - Run Flake8 linting checks
REM   type-check  - Run MyPy type checking
REM   check       - Run all checks (format, lint, type-check)
REM   run         - Run the application
REM   clean       - Remove cache and build artifacts

setlocal enabledelayedexpansion

if "%1"=="" goto help
if /i "%1"=="help" goto help
if /i "%1"=="install" goto install
if /i "%1"=="format" goto format
if /i "%1"=="lint" goto lint
if /i "%1"=="type-check" goto type_check
if /i "%1"=="check" goto check
if /i "%1"=="run" goto run
if /i "%1"=="clean" goto clean

echo Unknown command: %1
goto help

:help
echo.
echo Weight Loss Challenge - Python Development Commands
echo.
echo Available commands:
echo   dev install        - Install development dependencies
echo   dev format         - Format code with Black and isort
echo   dev lint           - Run Flake8 linting checks
echo   dev type-check     - Run MyPy type checking
echo   dev check          - Run all checks (format, lint, type-check)
echo   dev run            - Run the application
echo   dev clean          - Remove cache and build artifacts
echo   dev help           - Show this help message
echo.
goto end

:install
echo [*] Installing development dependencies...
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
goto end

:format
echo [*] Formatting code with Black...
.\venv\Scripts\black.exe frontend/ backend/
echo [*] Sorting imports with isort...
.\venv\Scripts\isort.exe frontend/ backend/
echo [+] Code formatting complete!
goto end

:lint
echo [*] Running Flake8 linting checks...
.\venv\Scripts\flake8.exe frontend/ backend/
if %errorlevel% equ 0 (
    echo [+] All linting checks passed!
) else (
    echo [!] Linting issues found
)
goto end

:type_check
echo [*] Running MyPy type checking...
.\venv\Scripts\mypy.exe frontend/ backend/
if %errorlevel% equ 0 (
    echo [+] All type checks passed!
) else (
    echo [!] Type checking issues found
)
goto end

:check
echo [*] Running all checks...
echo.
echo [1/3] Formatting code...
.\venv\Scripts\black.exe frontend/ backend/ >nul 2>&1
.\venv\Scripts\isort.exe frontend/ backend/ >nul 2>&1
echo [+] Formatting complete
echo.
echo [2/3] Running Flake8 linting...
.\venv\Scripts\flake8.exe frontend/ backend/ >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Linting checks passed
) else (
    echo [!] Linting issues found
    .\venv\Scripts\flake8.exe frontend/ backend/
)
echo.
echo [3/3] Running MyPy type checking...
.\venv\Scripts\mypy.exe frontend/ backend/ >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Type checks passed
) else (
    echo [!] Type checking issues found
    .\venv\Scripts\mypy.exe frontend/ backend/
)
echo.
echo [✓] All checks complete!
goto end

:run
echo [*] Starting Weight Loss Challenge application...
.\venv\Scripts\python.exe .\frontend\main.py
goto end

:clean
echo [*] Cleaning Python cache directories...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
for /d /r . %%d in (.mypy_cache) do @if exist "%%d" rmdir /s /q "%%d"
for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rmdir /s /q "%%d"
for /d /r . %%d in (.ruff_cache) do @if exist "%%d" rmdir /s /q "%%d"
echo [+] Cleanup complete!
goto end

:end
endlocal
