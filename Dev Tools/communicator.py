import os
import json
import re
from validators import (
    validate_input
)


class TerminalCommunicator:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.package_json_path = os.path.join(self.root_dir, "../package.json")

    def get_module_suggestion(self):
        if os.path.isfile(self.package_json_path):
            with open(self.package_json_path, "r") as file:
                package_data = json.load(file)
                return package_data.get("name", "")
        return ""

    @staticmethod
    def get_user_input(prompt, validator=None, error_message=None, default=None):
        return validate_input(prompt, validator, error_message, default)

    def get_choice(self, prompt, choices):
        choice = None
        while choice not in choices:
            choice = self.get_user_input(prompt, lambda x: x in choices, "Invalid choice. Please try again.")
        return choices[choice]

    @staticmethod
    def get_converted_name(name):
        converted_name = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip().lower().replace(' ', '-')
        converted_name = re.sub(r'-+', '-', converted_name)
        print(f"Button name converted: {name} -> {converted_name}")
        print(
            f"Function names will be: init{converted_name.capitalize().replace('-', '')}, action{converted_name.capitalize().replace('-', '')}")
        return converted_name
