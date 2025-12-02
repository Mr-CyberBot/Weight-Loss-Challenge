"""
Contestant Manager - Handles business logic for contestant operations
"""

from backend_api import BackendAPI


class ContestantManager:
    """Manages contestant operations"""

    def __init__(self):
        self.api = BackendAPI()
        self.contestants = []  # Track list of contestants

    def is_backend_available(self):
        """Check if backend is available"""
        return self.api.is_available()

    def add_contestant(self, name, dob, start_weight):
        """
        Add a new contestant

        :param name: Contestant name
        :type name: str
        :param dob: Date of birth (YYYY-MM-DD format)
        :type dob: str
        :param start_weight: Starting weight
        :type start_weight: float
        :return: Response from backend
        :rtype: dict
        """
        if not name or not dob or not start_weight:
            return {"error": "Name, date of birth, and starting weight are required"}

        try:
            weight = float(start_weight)
            result = self.api.add_contestant(name, weight, dob)

            # Add to local list if successful
            if "success" in result and name not in self.contestants:
                self.contestants.append(name)

            return result
        except ValueError:
            return {"error": "Weight must be a valid number"}

    def update_weight(self, name, current_weight):
        """
        Update contestant's current weight

        :param name: Contestant name
        :type name: str
        :param current_weight: Current weight
        :type current_weight: float
        :return: Response from backend
        :rtype: dict
        """
        if not name or not current_weight:
            return {"error": "Name and current weight are required"}

        try:
            weight = float(current_weight)
            return self.api.update_weight(name, weight)
        except ValueError:
            return {"error": "Weight must be a valid number"}

    def get_rankings(self):
        """
        Get current rankings

        :return: Rankings from backend
        :rtype: dict
        """
        return self.api.get_rankings()

    def delete_contestant(self, name):
        """
        Delete a contestant

        :param name: Contestant name
        :type name: str
        :return: Response from backend
        :rtype: dict
        """
        if not name:
            return {"error": "Contestant name is required"}

        result = self.api.delete_contestant(name)

        # Remove from local list if successful
        if "success" in result and name in self.contestants:
            self.contestants.remove(name)

        return result

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
        if not name:
            return {"error": "Contestant name is required"}

        if dob is not None and not dob:
            return {"error": "Date of birth cannot be empty"}

        if starting_weight is not None:
            try:
                float(starting_weight)
            except ValueError:
                return {"error": "Starting weight must be a valid number"}

        return self.api.edit_contestant(
            name, dob=dob, starting_weight=float(starting_weight) if starting_weight else None
        )

    def get_contestants(self):
        """
        Get list of all contestants

        :return: List of contestant names
        :rtype: list
        """
        return self.contestants

    def get_contestant_info(self, name):
        """
        Get information for a specific contestant

        :param name: Contestant name
        :type name: str
        :return: Contestant information
        :rtype: dict
        """
        return self.api.get_contestant_info(name)

    def refresh_contestants(self):
        """
        Refresh the list of contestants from backend
        """
        result = self.api.get_contestants()
        if "contestants" in result:
            self.contestants = result["contestants"]
        else:
            self.contestants = []
