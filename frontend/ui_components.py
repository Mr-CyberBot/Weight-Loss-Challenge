"""
UI Components - Reusable UI elements
"""

import tkinter as tk
from tkinter import ttk


class InputPanel(ttk.Frame):
    """Panel for contestant input fields"""

    def __init__(self, parent, selection_callback=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.selection_callback = selection_callback

        # Contestant Name (for adding new)
        ttk.Label(self, text="Contestant Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        # Date of Birth
        ttk.Label(self, text="Date of Birth (YYYY-MM-DD):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.dob_entry = ttk.Entry(self, width=30)
        self.dob_entry.grid(row=1, column=1, pady=5, padx=5)

        # Starting Weight
        ttk.Label(self, text="Starting Weight (lbs):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.start_weight_entry = ttk.Entry(self, width=30)
        self.start_weight_entry.grid(row=2, column=1, pady=5, padx=5)

        # Separator
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=10
        )

        # Select Contestant (for updating)
        ttk.Label(self, text="Select Contestant:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.contestant_combo = ttk.Combobox(self, width=28, state="readonly")
        self.contestant_combo.grid(row=4, column=1, pady=5, padx=5)
        self.contestant_combo.bind("<<ComboboxSelected>>", self._on_selection_change)

        # Edit DOB (for selected contestant)
        ttk.Label(self, text="DOB (YYYY-MM-DD):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.edit_dob_entry = ttk.Entry(self, width=30)
        self.edit_dob_entry.grid(row=5, column=1, pady=5, padx=5)

        # Edit Starting Weight
        ttk.Label(self, text="Starting Weight (lbs):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.edit_start_weight_entry = ttk.Entry(self, width=30)
        self.edit_start_weight_entry.grid(row=6, column=1, pady=5, padx=5)

        # Current Weight
        ttk.Label(self, text="Current Weight (lbs):").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.current_weight_entry = ttk.Entry(self, width=30)
        self.current_weight_entry.grid(row=7, column=1, pady=5, padx=5)

    def get_name(self):
        """
        Get contestant name

        :return: Contestant name
        :rtype: str
        """
        return self.name_entry.get().strip()

    def get_dob(self):
        """
        Get date of birth

        :return: Date of birth in YYYY-MM-DD format
        :rtype: str
        """
        return self.dob_entry.get().strip()

    def get_start_weight(self):
        """
        Get starting weight

        :return: Starting weight
        :rtype: str
        """
        return self.start_weight_entry.get().strip()

    def get_current_weight(self):
        """
        Get current weight

        :return: Current weight
        :rtype: str
        """
        return self.current_weight_entry.get().strip()

    def clear_fields(self):
        """
        Clear all input fields
        """
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.start_weight_entry.delete(0, tk.END)
        self.current_weight_entry.delete(0, tk.END)

    def clear_weight_field(self):
        """
        Clear only current weight field
        """
        self.current_weight_entry.delete(0, tk.END)

    def update_contestant_list(self, names):
        """
        Update the contestant dropdown list

        :param names: List of contestant names
        :type names: list
        """
        self.contestant_combo["values"] = tuple(names)  # Ensure it's a tuple
        if names:
            self.contestant_combo.current(0)
        else:
            # Clear selection when no contestants
            self.contestant_combo.set("")

    def get_selected_contestant(self):
        """
        Get the selected contestant from dropdown

        :return: Selected contestant name
        :rtype: str
        """
        return self.contestant_combo.get()

    def set_selected_contestant(self, name):
        """
        Set the selected contestant in dropdown

        :param name: Contestant name to select
        :type name: str
        """
        self.contestant_combo.set(name)

    def get_edit_dob(self):
        """
        Get edited date of birth

        :return: Edited DOB in YYYY-MM-DD format
        :rtype: str
        """
        return self.edit_dob_entry.get().strip()

    def get_edit_start_weight(self):
        """
        Get edited starting weight

        :return: Edited starting weight
        :rtype: str
        """
        return self.edit_start_weight_entry.get().strip()

    def clear_edit_fields(self):
        """
        Clear the edit fields
        """
        self.edit_dob_entry.delete(0, tk.END)
        self.edit_start_weight_entry.delete(0, tk.END)
        self.current_weight_entry.delete(0, tk.END)

    def _on_selection_change(self, event=None):
        """
        Handle contestant selection change
        """
        if self.selection_callback:
            self.selection_callback(self.get_selected_contestant())

    def populate_edit_fields(self, info):
        """
        Populate edit fields with contestant information

        :param info: Contestant information dictionary
        :type info: dict
        """
        # Clear fields first
        self.clear_edit_fields()

        # Populate with current data
        if "date_of_birth" in info and info["date_of_birth"]:
            self.edit_dob_entry.insert(0, info["date_of_birth"])

        if "starting_weight" in info and info["starting_weight"]:
            self.edit_start_weight_entry.insert(0, str(info["starting_weight"]))

        if "current_weight" in info and info["current_weight"]:
            self.current_weight_entry.insert(0, str(info["current_weight"]))


class ButtonPanel(ttk.Frame):
    """Panel for control buttons"""

    def __init__(
        self,
        parent,
        add_callback=None,
        rankings_callback=None,
        delete_callback=None,
        edit_callback=None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.add_callback = add_callback
        self.rankings_callback = rankings_callback
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback

        ttk.Button(self, text="Add Contestant", command=self._on_add).pack(side=tk.LEFT, padx=5)
        ttk.Button(self, text="Update Info", command=self._on_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(self, text="View Rankings", command=self._on_rankings).pack(side=tk.LEFT, padx=5)
        ttk.Button(self, text="Delete Contestant", command=self._on_delete).pack(
            side=tk.LEFT, padx=5
        )

    def _on_add(self):
        if self.add_callback:
            self.add_callback()

    def _on_edit(self):
        if self.edit_callback:
            self.edit_callback()

    def _on_rankings(self):
        if self.rankings_callback:
            self.rankings_callback()

    def _on_delete(self):
        if self.delete_callback:
            self.delete_callback()


class ResultsPanel(ttk.Frame):
    """Panel for displaying results and output"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Label
        ttk.Label(self, text="Results:").pack(anchor=tk.W, pady=(0, 5))

        # Text widget with scrollbar
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        self.text_widget = tk.Text(frame, height=15, width=70)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)

    def append(self, text):
        """
        Append text to results

        :param text: Text to append
        :type text: str
        """
        self.text_widget.insert(tk.END, text)

    def clear(self):
        """
        Clear all results
        """
        self.text_widget.delete(1.0, tk.END)

    def get_text(self):
        """
        Get all text from results

        :return: All text from results widget
        :rtype: str
        """
        return self.text_widget.get(1.0, tk.END)
