import re
from DevTools.Utils.Validators import (
    validate_input
)


class TerminalManager:

    @staticmethod
    def get_user_input(prompt, validator=None, error_message=None, default=None):
        return validate_input(prompt, validator, error_message, default)

    @staticmethod
    def sent_choice_to_user(introMsg, choices: dict):
        output = introMsg + '\n'
        for choiceKey, choiceValue in choices.items():
            output += f"{choiceKey}. {choiceValue}\n"
        output += 'Please enter your choice'
        return output

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
