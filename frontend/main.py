"""
Weight Loss Challenge - Frontend (Python GUI)
Main application entry point
"""

import tkinter as tk
from tkinter import messagebox

from ui_components import InputPanel, ButtonPanel, ResultsPanel
from contestant_manager import ContestantManager


class WeightLossChallengeApp:
    """Main application window"""

    def __init__(self, root):
        self.root = root
        self.root.title("Weight Loss Challenge Tracker")
        self.root.geometry("900x700")

        self.manager = ContestantManager()

        # Check backend availability
        if not self.manager.is_backend_available():
            messagebox.showwarning(
                "Backend Warning",
                "Backend executable not found.\n"
                "Please compile the C backend:\n"
                "cd backend && gcc -Wall -Wextra -std=c11 -o data-manipulator.exe data-manipulator.c",
            )

        self._setup_ui()

        # Load existing contestants on startup
        self._refresh_contestant_list()

    def _setup_ui(self):
        """
        Setup the user interface
        """
        # Create main frame
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = tk.Label(
            self.main_frame, text="Weight Loss Challenge Tracker", font=("Arial", 24, "bold")
        )
        title_label.pack(pady=20)

        # Input Panel
        self.input_panel = InputPanel(
            self.main_frame, selection_callback=self._on_contestant_selected
        )
        self.input_panel.pack(padx=10, pady=10, fill=tk.X)

        # Button Panel
        self.button_panel = ButtonPanel(
            self.main_frame,
            add_callback=self.add_contestant,
            edit_callback=self.edit_contestant,
            rankings_callback=self.view_rankings,
            delete_callback=self.delete_contestant,
        )
        self.button_panel.pack(pady=20)

        # Results Panel
        self.results_panel = ResultsPanel(self.main_frame)
        self.results_panel.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def add_contestant(self):
        """
        Add a new contestant
        """
        name = self.input_panel.get_name()
        dob = self.input_panel.get_dob()
        start_weight = self.input_panel.get_start_weight()

        result = self.manager.add_contestant(name, dob, start_weight)

        if "error" in result:
            messagebox.showerror("Error", result["error"])
            self.results_panel.append(f"❌ Error: {result['error']}\n")
        else:
            self.results_panel.append(f"✓ Added contestant: {name}\n")
            self.input_panel.clear_fields()
            self._refresh_contestant_list()

    def edit_contestant(self):
        """
        Edit a contestant's DOB, starting weight, and/or current weight
        """
        name = self.input_panel.get_selected_contestant()
        dob = self.input_panel.get_edit_dob()
        start_weight = self.input_panel.get_edit_start_weight()
        current_weight = self.input_panel.get_current_weight()

        if not name:
            messagebox.showwarning("Error", "Please select a contestant to edit")
            return

        if not dob and not start_weight and not current_weight:
            messagebox.showwarning(
                "Error", "Please enter at least one field to update (DOB, Starting Weight, or Current Weight)"
            )
            return

        # Convert weights to float if provided
        sw = None
        cw = None
        if start_weight:
            try:
                sw = float(start_weight)
            except ValueError:
                messagebox.showerror("Error", "Starting weight must be a valid number")
                return
        
        if current_weight:
            try:
                cw = float(current_weight)
            except ValueError:
                messagebox.showerror("Error", "Current weight must be a valid number")
                return

        result = self.manager.edit_contestant(
            name, 
            dob=dob if dob else None, 
            starting_weight=sw,
            current_weight=cw
        )

        if "error" in result:
            messagebox.showerror("Error", result["error"])
            self.results_panel.append(f"❌ Error: {result['error']}\n")
        else:
            self.results_panel.append(f"✏️ Updated contestant: {name}\n")
            # Refresh the contestant info to show updated data
            info = self.manager.get_contestant_info(name)
            if "error" not in info:
                self.input_panel.populate_edit_fields(info)

    def _refresh_contestant_list(self):
        """
        Refresh the contestant dropdown list
        """
        self.manager.refresh_contestants()
        contestants = self.manager.get_contestants()
        self.input_panel.update_contestant_list(contestants)

        # If there are contestants, populate edit fields for the first one
        if contestants:
            self._on_contestant_selected(contestants[0])

    def _on_contestant_selected(self, name):
        """
        Callback when contestant is selected from dropdown

        :param name: Selected contestant name
        :type name: str
        """
        if not name:
            self.input_panel.clear_edit_fields()
            return

        # Get contestant info from backend
        info = self.manager.get_contestant_info(name)

        if "error" not in info:
            self.input_panel.populate_edit_fields(info)

    def view_rankings(self):
        """
        View current rankings
        """
        # Save current selection
        current_selection = self.input_panel.get_selected_contestant()
        
        result = self.manager.get_rankings()

        self.results_panel.clear()

        if "error" in result:
            messagebox.showerror("Error", result["error"])
            self.results_panel.append(f"❌ Error: {result['error']}\n")
        else:
            self.results_panel.append("=== Current Rankings ===\n\n")
            self.results_panel.append(result.get("rankings", "No data available"))
            # Refresh the dropdown but preserve selection
            self.manager.refresh_contestants()
            contestants = self.manager.get_contestants()
            self.input_panel.update_contestant_list(contestants)
            # Restore the previous selection if it still exists
            if current_selection and current_selection in contestants:
                self.input_panel.set_selected_contestant(current_selection)

    def delete_contestant(self):
        """
        Delete a contestant
        """
        name = self.input_panel.get_selected_contestant()

        if not name:
            messagebox.showwarning("Error", "Please select a contestant to delete")
            return

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            return

        result = self.manager.delete_contestant(name)

        if "error" in result:
            messagebox.showerror("Error", result["error"])
            self.results_panel.append(f"❌ Error: {result['error']}\n")
        else:
            self.results_panel.append(f"🗑️ Deleted contestant: {name}\n")
            self._refresh_contestant_list()


def main():
    """Application entry point"""
    root = tk.Tk()
    WeightLossChallengeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
