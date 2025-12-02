# Weight Tracker Calculator - C Implementation Specification

## Overview

Create a lightweight C calculator program that performs age and weight loss calculations. The program receives commands via command-line arguments and outputs results to stdout.

**Key Principle**: This is a **pure calculator** - no JSON parsing, no file I/O, no data management. Just math.

## Requirements

### Language & Standards
- Standard C (C11 or later)
- Only use standard C library (`stdio.h`, `stdlib.h`, `string.h`, `time.h`)
- No external dependencies
- Cross-platform compatible (Windows/Linux/Mac)

### Compilation
Must compile with:
```bash
gcc -Wall -Wextra -std=c11 -o data-manipulator.exe data-manipulator.c
```

No warnings, no errors, no external libraries needed.

## Program Interface

### Command-Line Format
```
data-manipulator.exe <command> <arg1> [arg2] [arg3]
```

### Three Commands to Implement

---

#### 1. `age` - Calculate Age from Date of Birth

**Usage:**
```bash
data-manipulator.exe age <YYYY-MM-DD>
```

**Input:**
- Date of birth in YYYY-MM-DD format (e.g., "1990-05-15")

**Output:**
- Age as integer (e.g., "35")
- Print to stdout with newline

**Validation:**
- Must validate date format (YYYY-MM-DD)
- Must validate month is 1-12
- Must validate day is 1-31
- Must reject future dates (date after today)
- Current date should be December 1, 2025 (or use system time)

**Return Codes:**
- `0` = Success (valid age calculated)
- `1` = Error (invalid format or future date)

**Error Output:**
- Print error message to stderr: `"ERROR: <message>"`
- Examples:
  - `"ERROR: Missing date of birth"`
  - `"ERROR: Invalid date of birth"`

**Examples:**
```bash
$ data-manipulator.exe age 1990-05-15
35

$ data-manipulator.exe age 2030-01-01
ERROR: Invalid date of birth
(exit code 1)

$ data-manipulator.exe age invalid
ERROR: Invalid date of birth
(exit code 1)
```

**Age Calculation Rules:**
- Age = current_year - birth_year
- If current month/day is before birth month/day, subtract 1 from age
- Example: Born 1990-05-15, today is 2025-05-10 → age is 34 (not 35 yet)

---

#### 2. `weight_lost` - Calculate Weight Lost

**Usage:**
```bash
data-manipulator.exe weight_lost <starting_weight> <current_weight>
```

**Input:**
- Starting weight (float/double, e.g., "200.0")
- Current weight (float/double, e.g., "190.0")

**Output:**
- Weight lost formatted as "%.2f" (e.g., "10.00")
- Print to stdout with newline

**Calculation:**
```
weight_lost = starting_weight - current_weight
```

**Validation:**
- Both weights must be valid numbers
- No validation for negative results (can lose or gain weight)

**Return Codes:**
- `0` = Always succeeds with valid numbers

**Error Output:**
- Print to stderr if arguments missing: `"ERROR: Missing starting or current weight"`

**Examples:**
```bash
$ data-manipulator.exe weight_lost 200.0 190.0
10.00

$ data-manipulator.exe weight_lost 200 195.5
4.50

$ data-manipulator.exe weight_lost 190.0 200.0
-10.00
(gained weight - negative is OK)

$ data-manipulator.exe weight_lost 200.0
ERROR: Missing starting or current weight
(exit code 1)
```

---

#### 3. `percentage_lost` - Calculate Weight Loss Percentage

**Usage:**
```bash
data-manipulator.exe percentage_lost <weight_lost> <starting_weight>
```

**Input:**
- Weight lost (float/double, e.g., "10.0")
- Starting weight (float/double, e.g., "200.0")

**Output:**
- Percentage formatted as "%.2f" (e.g., "5.00")
- Print to stdout with newline

**Calculation:**
```
if starting_weight <= 0:
    percentage = 0.0
else:
    percentage = (weight_lost / starting_weight) * 100.0
```

**Validation:**
- Must handle division by zero (return 0.00 if starting weight is 0 or negative)
- No validation for negative percentages (can be negative if gained weight)

**Return Codes:**
- `0` = Always succeeds with valid numbers

**Error Output:**
- Print to stderr if arguments missing: `"ERROR: Missing weight lost or starting weight"`

**Examples:**
```bash
$ data-manipulator.exe percentage_lost 10.0 200.0
5.00

$ data-manipulator.exe percentage_lost 15.5 200.0
7.75

$ data-manipulator.exe percentage_lost 10.0 0
0.00
(avoid division by zero)

$ data-manipulator.exe percentage_lost -10.0 200.0
-5.00
(gained weight - negative is OK)
```

---

## General Requirements

### Command Validation
If no command is provided or unknown command:
```bash
$ data-manipulator.exe
ERROR: No command specified
(exit code 1)

$ data-manipulator.exe unknown
ERROR: Unknown command: unknown
(exit code 1)
```

### Main Function Structure
```c
int main(int argc, char *argv[]) {
    // Check if command provided
    // Parse command
    // Execute appropriate function
    // Return appropriate exit code
}
```

### Suggested Function Signatures
```c
int calculate_age(const char *dob_str);
double calculate_weight_lost(double starting_weight, double current_weight);
double calculate_percentage_lost(double weight_lost, double starting_weight);
```

## Testing Your Implementation

### Test Suite
Run these tests to verify your implementation:

```bash
# Age calculation tests
data-manipulator.exe age 1990-05-15     # Should output: 35
data-manipulator.exe age 2000-01-01     # Should output: 25
data-manipulator.exe age 2030-01-01     # Should error (future date)
data-manipulator.exe age invalid        # Should error

# Weight lost tests
data-manipulator.exe weight_lost 200.0 190.0   # Should output: 10.00
data-manipulator.exe weight_lost 200 195.5     # Should output: 4.50
data-manipulator.exe weight_lost 190.0 200.0   # Should output: -10.00

# Percentage tests
data-manipulator.exe percentage_lost 10.0 200.0   # Should output: 5.00
data-manipulator.exe percentage_lost 15.5 200.0   # Should output: 7.75
data-manipulator.exe percentage_lost 10.0 0       # Should output: 0.00
```

### Exit Code Testing
```bash
# PowerShell
data-manipulator.exe age 1990-05-15
echo $LASTEXITCODE    # Should be 0

data-manipulator.exe age 2030-01-01
echo $LASTEXITCODE    # Should be 1
```

## Integration with Python Frontend

The Python frontend will call your program like this:

```python
import subprocess

# Age calculation
result = subprocess.run(
    ["data-manipulator.exe", "age", "1990-05-15"],
    capture_output=True,
    text=True
)
if result.returncode == 0:
    age = int(result.stdout.strip())  # "35"

# Weight calculations
result = subprocess.run(
    ["data-manipulator.exe", "weight_lost", "200.0", "190.0"],
    capture_output=True,
    text=True
)
weight_lost = float(result.stdout.strip())  # "10.00"
```

## Performance Requirements

- Each calculation should complete in < 1ms
- No memory leaks
- No buffer overflows
- Handle edge cases gracefully

## Code Quality

- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small
- Validate all inputs
- Handle errors gracefully

## What NOT to Include

❌ JSON parsing (no json-c library needed)  
❌ File I/O (no reading/writing files)  
❌ Data structures for contestants  
❌ Sorting or ranking logic  
❌ String formatting beyond printf  
❌ Network communication  
❌ Configuration files  

This is a **pure calculator** - the Python frontend handles everything else!

## Success Criteria

✅ Compiles with no warnings  
✅ All three commands work correctly  
✅ Validates inputs properly  
✅ Returns correct exit codes  
✅ Handles edge cases (division by zero, future dates, etc.)  
✅ No external dependencies  
✅ Output matches specification exactly  

## File to Create

Create a single file: `data-manipulator.c`

That's it! Keep it simple and focused.
