import re

from DevTools.Utils.Validators import validate_input, ChoiceValidator


class TerminalManager:

    @staticmethod
    def get_user_input(prompt, validator=None, default=None):
        return validate_input(prompt, validator, default)

    @staticmethod
    def sent_choice_to_user(introMsg, choices):
        output = introMsg + '\n'
        if isinstance(choices, dict):
            for choiceKey, choiceValue in choices.items():
                output += f"{choiceKey}. {choiceValue}\n"
        elif isinstance(choices, list):
            # This case is handled by converting lists to dictionaries beforehand
            for index, choice in enumerate(choices):
                output += f"{index + 1}. {choice}\n"
        output += 'Please enter your choice'
        return output

    def get_choice(self, prompt, choices):
        choice_validator = ChoiceValidator(choices)
        choice = None
        while choice not in choices:
            choice = self.get_user_input(prompt, choice_validator)
        return choices[choice]

    @staticmethod
    def get_converted_name(name):
        converted_name = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip().lower().replace(' ', '-')
        converted_name = re.sub(r'-+', '-', converted_name)
        print(f"Button name converted: {name} -> {converted_name}")
        print(
            f"Function names will be: init{converted_name.capitalize().replace('-', '')}, action{converted_name.capitalize().replace('-', '')}")
        return converted_name

    @staticmethod
    def get_converted_field_name(name, type):
        cleaned_name = re.sub(r'[^a-zA-Z0-9 ]', '', name)

        parts = cleaned_name.split()

        if parts:
            converted_parts = [parts[0].lower()]
            converted_parts += [part.capitalize() for part in parts[1:]]
        else:
            return ''

        converted_name = ''.join(converted_parts)
        print(f"{type} name converted: {name} -> {converted_name}")

        return converted_name



