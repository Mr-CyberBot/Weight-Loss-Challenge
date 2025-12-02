"""
Backend API - Handles communication with C backend
"""

import subprocess
import json
import os
import sys


class BackendAPI:
    """Interface for communicating with the C backend executable"""

    def __init__(self, backend_path="../backend/weight_tracker.exe", use_mock=False):
        self.backend_exe = backend_path
        self.use_mock = use_mock

        # Try to use mock backend if C executable doesn't exist
        if use_mock or not os.path.exists(self.backend_exe):
            self.backend_exe = os.path.join(
                os.path.dirname(__file__), "..", "backend", "mock_backend.py"
            )
            self.backend_exe = os.path.normpath(os.path.abspath(self.backend_exe))
            self.is_python = True
        else:
            self.is_python = False

    def is_available(self):
        """Check if backend executable exists"""
        return os.path.exists(self.backend_exe)

    def _execute_command(self, command, data=None):
        """
        Execute a command on the backend

        :param command: The command to execute
        :type command: str
        :param data: Optional data to pass to backend
        :type data: dict
        :return: Response from backend (parsed JSON)
        :rtype: dict
        """
        try:
            if not self.is_available():
                return {"error": "Backend executable not found. Please compile the C backend."}

            # Prepare command with data
            if self.is_python:
                # Use the venv's python executable for consistency
                cmd = [sys.executable, self.backend_exe, command]
            else:
                cmd = [self.backend_exe, command]

            if data:
                cmd.append(json.dumps(data))

            # Execute backend
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": result.stderr}

        except json.JSONDecodeError:
            return {"error": "Invalid response from backend"}
        except subprocess.TimeoutExpired:
            return {"error": "Backend timeout"}
        except Exception as e:
            return {"error": str(e)}

    def add_contestant(self, name, weight, dob):
        """
        Add a new contestant

        :param name: Contestant name
        :type name: str
        :param weight: Contestant starting weight
        :type weight: float
        :param dob: Date of birth (YYYY-MM-DD format)
        :type dob: str
        :return: Response from backend
        :rtype: dict
        """
        data = {"name": name, "weight": weight, "dob": dob}
        return self._execute_command("add", data)

    def update_weight(self, name, weight):
        """
        Update contestant's weight

        :param name: Contestant name
        :type name: str
        :param weight: New weight value
        :type weight: float
        :return: Response from backend
        :rtype: dict
        """
        data = {"name": name, "weight": weight}
        return self._execute_command("update", data)

    def get_rankings(self):
        """Get current rankings"""
        return self._execute_command("rankings")

    def delete_contestant(self, name):
        """
        Delete a contestant

        :param name: Contestant name
        :type name: str
        :return: Response from backend
        :rtype: dict
        """
        data = {"name": name}
        return self._execute_command("delete", data)

    def get_contestants(self):
        """
        Get list of all contestants

        :return: List of contestant names
        :rtype: dict
        """
        return self._execute_command("list")

    def get_contestant_info(self, name):
        """
        Get information for a specific contestant

        :param name: Contestant name
        :type name: str
        :return: Contestant information
        :rtype: dict
        """
        try:
            if not self.is_available():
                return {"error": "Backend executable not found. Please compile the C backend."}

            # Prepare command with contestant name
            if self.is_python:
                cmd = [sys.executable, self.backend_exe, "info", name]
            else:
                cmd = [self.backend_exe, "info", name]

            # Execute backend
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"error": result.stderr}

        except json.JSONDecodeError:
            return {"error": "Invalid response from backend"}
        except subprocess.TimeoutExpired:
            return {"error": "Backend timeout"}
        except Exception as e:
            return {"error": str(e)}

    def edit_contestant(self, name, dob=None, starting_weight=None):
        """
        Edit a contestant's information

        :param name: Contestant name
        :type name: str
        :param dob: Date of birth (YYYY-MM-DD format)
        :type dob: str
        :param starting_weight: Starting weight
        :type starting_weight: float
        :return: Response from backend
        :rtype: dict
        """
        data = {"name": name}
        if dob is not None:
            data["dob"] = dob
        if starting_weight is not None:
            data["starting_weight"] = starting_weight
        return self._execute_command("edit", data)
