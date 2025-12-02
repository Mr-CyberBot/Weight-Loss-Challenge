"""
Backend API - Handles all data operations with C calculator backend
"""

import subprocess
import json
import os
import sys
from pathlib import Path
from datetime import datetime


DATA_FILE = os.path.join(os.path.dirname(__file__), "contestants.json")


def load_contestants():
    """
    Load contestants from file

    :return: Dictionary of contestants
    :rtype: dict
    """
    if Path(DATA_FILE).exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_contestants(data):
    """
    Save contestants to file

    :param data: Contestant data to save
    :type data: dict
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def call_c_backend(command, *args):
    """
    Call the C calculator backend

    :param command: Command to execute (age, weight_lost, percentage_lost)
    :type command: str
    :param args: Arguments for the command
    :return: Result from C backend
    :rtype: str or None
    """
    backend_exe = os.path.join(
        os.path.dirname(__file__), "..", "backend", "data-manipulator.exe"
    )

    if not os.path.exists(backend_exe):
        return None

    try:
        cmd = [backend_exe, command] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None


class BackendAPI:
    """Interface for communicating with the data backend"""

    def __init__(self):
        pass

    def _calculate_age(self, dob_str):
        """
        Calculate age using C backend if available, otherwise use Python fallback

        :param dob_str: Date of birth in YYYY-MM-DD format
        :type dob_str: str
        :return: Age in years or None if invalid
        :rtype: int or None
        """
        result = call_c_backend("age", dob_str)
        if result is not None:
            try:
                age = int(result)
                return age if age >= 0 else None
            except ValueError:
                pass

        # Fallback to Python calculation
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 0:
                return None
            return age
        except ValueError:
            return None

    def _calculate_weight_lost(self, starting_weight, current_weight):
        """
        Calculate weight lost using C backend if available

        :param starting_weight: Starting weight
        :type starting_weight: float
        :param current_weight: Current weight
        :type current_weight: float
        :return: Weight lost
        :rtype: float
        """
        result = call_c_backend("weight_lost", str(starting_weight), str(current_weight))
        if result is not None:
            try:
                return float(result)
            except ValueError:
                pass

        return starting_weight - current_weight

    def _calculate_percentage_lost(self, weight_lost, starting_weight):
        """
        Calculate percentage lost using C backend if available

        :param weight_lost: Weight lost in pounds
        :type weight_lost: float
        :param starting_weight: Starting weight
        :type starting_weight: float
        :return: Percentage lost
        :rtype: float
        """
        result = call_c_backend("percentage_lost", str(weight_lost), str(starting_weight))
        if result is not None:
            try:
                return float(result)
            except ValueError:
                pass

        if starting_weight <= 0:
            return 0.0
        return (weight_lost / starting_weight) * 100.0

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
        contestants_db = load_contestants()

        if name in contestants_db:
            return {"error": "Contestant already exists"}

        age = self._calculate_age(dob)
        if age is None:
            return {"error": "Invalid date of birth. Use YYYY-MM-DD format or date cannot be in future"}

        contestants_db[name] = {
            "date_of_birth": dob,
            "age": age,
            "starting_weight": weight,
            "current_weight": weight,
            "weight_lost": 0.0,
            "percentage_lost": 0.0,
        }
        save_contestants(contestants_db)
        return {"status": "ok"}

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
        contestants_db = load_contestants()

        if name not in contestants_db:
            return {"error": "Contestant not found"}

        contestant = contestants_db[name]
        contestant["current_weight"] = weight
        contestant["weight_lost"] = self._calculate_weight_lost(
            contestant["starting_weight"], weight
        )
        contestant["percentage_lost"] = self._calculate_percentage_lost(
            contestant["weight_lost"], contestant["starting_weight"]
        )

        save_contestants(contestants_db)
        return {"status": "ok"}

    def get_rankings(self):
        """Get current rankings"""
        contestants_db = load_contestants()

        if not contestants_db:
            return {"rankings": "No contestants found"}

        # Sort by percentage lost (descending)
        sorted_contestants = sorted(
            contestants_db.items(), key=lambda x: x[1]["percentage_lost"], reverse=True
        )

        rankings_text = ""
        for i, (name, data) in enumerate(sorted_contestants, 1):
            age = data.get("age", "N/A")
            rankings_text += f"{i}. {name}\n"
            rankings_text += (
                f"   Starting: {data['starting_weight']:.1f} lbs | "
                f"Current: {data['current_weight']:.1f} lbs\n"
            )
            rankings_text += (
                f"   Lost: {data['weight_lost']:.1f} lbs "
                f"({data['percentage_lost']:.1f}%)\n"
            )
            rankings_text += f"   Age: {age}\n\n"

        return {"rankings": rankings_text}

    def delete_contestant(self, name):
        """
        Delete a contestant

        :param name: Contestant name
        :type name: str
        :return: Response from backend
        :rtype: dict
        """
        contestants_db = load_contestants()

        if name not in contestants_db:
            return {"error": "Contestant not found"}

        del contestants_db[name]
        save_contestants(contestants_db)
        return {"status": "ok"}

    def get_contestants(self):
        """
        Get list of all contestants

        :return: List of contestant names
        :rtype: dict
        """
        contestants_db = load_contestants()
        names = list(contestants_db.keys())
        return {"contestants": names}

    def get_contestant_info(self, name):
        """
        Get information for a specific contestant

        :param name: Contestant name
        :type name: str
        :return: Contestant information
        :rtype: dict
        """
        contestants_db = load_contestants()

        if name not in contestants_db:
            return {"error": "Contestant not found"}

        contestant = contestants_db[name]
        return {
            "name": name,
            "date_of_birth": contestant.get("date_of_birth"),
            "age": contestant.get("age"),
            "starting_weight": contestant.get("starting_weight"),
            "current_weight": contestant.get("current_weight"),
        }

    def edit_contestant(self, name, dob=None, starting_weight=None, current_weight=None):
        """
        Edit a contestant's information

        :param name: Contestant name
        :type name: str
        :param dob: Date of birth (YYYY-MM-DD format)
        :type dob: str
        :param starting_weight: Starting weight
        :type starting_weight: float
        :param current_weight: Current weight
        :type current_weight: float
        :return: Response from backend
        :rtype: dict
        """
        contestants_db = load_contestants()

        if name not in contestants_db:
            return {"error": "Contestant not found"}

        contestant = contestants_db[name]

        if dob is not None:
            age = self._calculate_age(dob)
            if age is None:
                return {"error": "Invalid date of birth. Use YYYY-MM-DD format or date cannot be in future"}
            contestant["date_of_birth"] = dob
            contestant["age"] = age

        if starting_weight is not None:
            contestant["starting_weight"] = starting_weight
            # Recalculate weight lost and percentage
            contestant["weight_lost"] = self._calculate_weight_lost(
                starting_weight, contestant["current_weight"]
            )
            contestant["percentage_lost"] = self._calculate_percentage_lost(
                contestant["weight_lost"], starting_weight
            )
        
        if current_weight is not None:
            contestant["current_weight"] = current_weight
            # Recalculate weight lost and percentage
            contestant["weight_lost"] = self._calculate_weight_lost(
                contestant["starting_weight"], current_weight
            )
            contestant["percentage_lost"] = self._calculate_percentage_lost(
                contestant["weight_lost"], contestant["starting_weight"]
            )

        save_contestants(contestants_db)
        return {"status": "ok"}

