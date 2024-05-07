import re

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion


class CaseInsensitiveCompleter(Completer):
    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lower()
        for word in self.words:
            if word.lower().startswith(text):
                yield Completion(word, start_position=-len(text))


class TerminalManager:

    def __init__(self, Validators):
        self.Validators = Validators

    def get_user_input(self, prompt_text, validator=None, default=None):
        return self.Validators.validate_input(prompt_text, validator, default)

    # DEPRECATED METHODS BELOW, USE get_choice_with_autocomplete INSTEAD (list should be passed as choices)
    #
    # @staticmethod
    # def sent_choice_to_user(introMsg, choices):
    #     output = introMsg + '\n'
    #     if isinstance(choices, dict):
    #         for choiceKey, choiceValue in choices.items():
    #             output += f"{choiceKey}. {choiceValue}\n"
    #     elif isinstance(choices, list):
    #         # This case is handled by converting lists to dictionaries beforehand
    #         for index, choice in enumerate(choices):
    #             output += f"{index + 1}. {choice}\n"
    #     output += 'Please enter your choice'
    #     return output
    #
    # def get_choice(self, prompt_text, choices):
    #     choice_validator = self.Validators.ChoiceValidator(choices)
    #     choice = None
    #     while choice not in choices:
    #         choice = self.get_user_input(prompt_text, choice_validator)
    #     return choices[choice]

    @staticmethod
    def input_with_autocomplete(prompt_text, choices):
        completer = CaseInsensitiveCompleter(choices)
        user_input = prompt(prompt_text, completer=completer)
        return user_input

    def get_choice_with_autocomplete(self, prompt_text, choices: list, send_choices=True, validator=None):
        if send_choices:
            output = ''
            for index, choice in enumerate(choices):
                if index == len(choices) - 1:
                    output += f"{index + 1}. {choice}"
                else:
                    output += f"{index + 1}. {choice}\n"
            print(output)
        while True:
            user_input = self.input_with_autocomplete(prompt_text, choices)
            try:
                if validator:
                    return validator(user_input)
                return user_input
            except self.Validators.ValidationError as e:
                print(f"\033[91m{e}\033[0m")

    @staticmethod
    def convert_to_camel_case(name, start_lower=True):
        cleaned_name = re.sub(r'[^a-zA-Z0-9 ]', '', name)

        parts = cleaned_name.split()

        if parts:
            converted_parts = [parts[0].lower() if start_lower else parts[0].capitalize()]
            converted_parts += [part.capitalize() for part in parts[1:]]
            return ''.join(converted_parts)
        else:
            return ''

    def get_converted_name(self, name):
        converted_name = re.sub(r'[^a-zA-Z0-9\s-]', '', name).strip().lower().replace(' ', '-')
        converted_name = re.sub(r'-+', '-', converted_name)
        functions_name = self.convert_to_camel_case(name, start_lower=False)
        print(f"Button name converted: {name} -> {converted_name}")
        print(
            f"Function names will be: init{functions_name}, action{functions_name}")
        return converted_name

    @staticmethod
    def get_converted_field_name(name, field_type):
        converted_name = TerminalManager.convert_to_camel_case(name)
        print(f"{field_type} name converted: {name} -> {converted_name}")
        return converted_name
