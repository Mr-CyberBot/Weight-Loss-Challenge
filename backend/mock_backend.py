"""
Mock Backend - Temporary test backend for frontend development
Simulates the C backend behavior without compilation
Uses JSON file for persistent data storage
"""

import json
import sys
from pathlib import Path
from datetime import datetime


DATA_FILE = "mock_contestants.json"


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
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def calculate_age(dob_str):
    """
    Calculate age from date of birth

    :param dob_str: Date of birth in YYYY-MM-DD format
    :type dob_str: str
    :return: Age in years
    :rtype: int
    """
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except ValueError:
        return None


def add_contestant(name, weight, dob):
    """
    :param name: Contestant name
    :type name: str
    :param weight: Starting weight
    :type weight: float
    :param dob: Date of birth (YYYY-MM-DD format)
    :type dob: str
    :return: Success or error response
    :rtype: dict
    """
    contestants_db = load_contestants()

    if name in contestants_db:
        return {"error": "Contestant already exists"}

    age = calculate_age(dob)
    if age is None:
        return {"error": "Invalid date of birth format. Use YYYY-MM-DD"}

    if age < 0:
        return {"error": "Date of birth cannot be in the future"}

    contestants_db[name] = {
        "date_of_birth": dob,
        "age": age,
        "starting_weight": weight,
        "current_weight": weight,
        "weight_lost": 0.0,
        "percentage_lost": 0.0,
    }
    save_contestants(contestants_db)
    return {"success": "Contestant added successfully"}


def update_weight(name, weight):
    """
    :param name: Contestant name
    :type name: str
    :param weight: New weight
    :type weight: float
    :return: Success or error response
    :rtype: dict
    """
    contestants_db = load_contestants()

    if name not in contestants_db:
        return {"error": "Contestant not found"}

    contestant = contestants_db[name]
    contestant["current_weight"] = weight
    contestant["weight_lost"] = contestant["starting_weight"] - weight

    if contestant["starting_weight"] > 0:
        contestant["percentage_lost"] = (
            contestant["weight_lost"] / contestant["starting_weight"]
        ) * 100

    save_contestants(contestants_db)
    return {"success": "Weight updated successfully"}


def edit_contestant(name, dob=None, starting_weight=None):
    """
    Edit a contestant's information

    :param name: Contestant name
    :type name: str
    :param dob: Date of birth (YYYY-MM-DD format)
    :type dob: str
    :param starting_weight: Starting weight
    :type starting_weight: float
    :return: Success or error response
    :rtype: dict
    """
    contestants_db = load_contestants()

    if name not in contestants_db:
        return {"error": "Contestant not found"}

    contestant = contestants_db[name]

    if dob is not None:
        age = calculate_age(dob)
        if age is None:
            return {"error": "Invalid date of birth format. Use YYYY-MM-DD"}
        if age < 0:
            return {"error": "Date of birth cannot be in the future"}
        contestant["date_of_birth"] = dob
        contestant["age"] = age

    if starting_weight is not None:
        contestant["starting_weight"] = starting_weight
        # Recalculate weight lost and percentage
        contestant["weight_lost"] = contestant["starting_weight"] - contestant["current_weight"]
        if contestant["starting_weight"] > 0:
            contestant["percentage_lost"] = (
                contestant["weight_lost"] / contestant["starting_weight"]
            ) * 100

    save_contestants(contestants_db)
    return {"success": "Contestant updated successfully"}


def delete_contestant(name):
    """
    Delete a contestant

    :param name: Contestant name
    :type name: str
    :return: Success or error response
    :rtype: dict
    """
    contestants_db = load_contestants()

    if name not in contestants_db:
        return {"error": "Contestant not found"}

    del contestants_db[name]
    save_contestants(contestants_db)
    return {"success": "Contestant deleted successfully"}


def get_rankings():
    """
    :return: Rankings formatted as string
    :rtype: dict
    """
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


def main():
    """
    Main entry point - processes command line arguments
    """
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified"}))
        return 1

    command = sys.argv[1]

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing data for add command"}))
                return 1

            data = json.loads(sys.argv[2])
            result = add_contestant(data["name"], data["weight"], data["dob"])
            print(json.dumps(result))

        elif command == "update":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing data for update command"}))
                return 1

            data = json.loads(sys.argv[2])
            result = update_weight(data["name"], data["weight"])
            print(json.dumps(result))

        elif command == "rankings":
            result = get_rankings()
            print(json.dumps(result))

        elif command == "delete":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing data for delete command"}))
                return 1

            data = json.loads(sys.argv[2])
            result = delete_contestant(data["name"])
            print(json.dumps(result))

        elif command == "edit":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing data for edit command"}))
                return 1

            data = json.loads(sys.argv[2])
            result = edit_contestant(
                data["name"], dob=data.get("dob"), starting_weight=data.get("starting_weight")
            )
            print(json.dumps(result))

        elif command == "list":
            contestants_db = load_contestants()
            names = list(contestants_db.keys())
            print(json.dumps({"contestants": names}))

        elif command == "info":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing contestant name"}))
                return 1

            name = sys.argv[2]
            contestants_db = load_contestants()

            if name not in contestants_db:
                print(json.dumps({"error": "Contestant not found"}))
                return 1

            contestant = contestants_db[name]
            print(
                json.dumps(
                    {
                        "name": name,
                        "date_of_birth": contestant.get("date_of_birth"),
                        "age": contestant.get("age"),
                        "starting_weight": contestant.get("starting_weight"),
                        "current_weight": contestant.get("current_weight"),
                    }
                )
            )

        else:
            print(json.dumps({"error": "Unknown command"}))
            return 1

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON data"}))
        return 1
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
