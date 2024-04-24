import json
import re


class Validators:
    class ValidationError(Exception):
        """Custom exception for validation errors."""
        pass

    class ChoiceValidator:
        def __init__(self, choices):
            self.choices = choices

        def __call__(self, value):
            if value in self.choices:
                return value
            raise Validators.ValidationError("Invalid choice. Please try again.")

    def validate_input(self, prompt, validator=None, default=None):
        while True:
            user_input = input(f"{prompt}: ") if default is None else input(
                f"{prompt} (default: {default}): ") or default
            try:
                if validator:
                    return validator(user_input)
                return user_input
            except self.ValidationError as e:
                print(f"\033[91m{e}\033[0m")

    @staticmethod
    def array_validator(value):
        try:
            result = eval(value)
            if isinstance(result, list):
                return result
            raise Validators.ValidationError("Input is not a valid list.")
        except:
            raise Validators.ValidationError("Invalid input for a list.")

    @staticmethod
    def integer_validator(value):
        if value.lstrip('-').isdigit():
            return int(value)
        raise Validators.ValidationError("Input is not a valid integer.")

    @staticmethod
    def true_false_validator(value):
        value = value.strip().lower()
        if value in ['true', 'false']:
            return value == 'true'
        raise Validators.ValidationError("Input must be either 'true' or 'false'.")

    @staticmethod
    def array_int_validator(value):
        try:
            items = eval(value)
            if isinstance(items, list) and all(isinstance(item, int) for item in items):
                return items
            raise Validators.ValidationError("List must contain only integers.")
        except:
            raise Validators.ValidationError("Invalid input for an array of integers.")

    @staticmethod
    def float_validator(value):
        try:
            return float(value)
        except ValueError:
            raise Validators.ValidationError("Input is not a valid float.")

    @staticmethod
    def string_validator(value):
        if isinstance(value, str):
            return value
        raise Validators.ValidationError("Input is not a valid string.")

    @staticmethod
    def json_object_validator(value):
        try:
            result = json.loads(value)
            if isinstance(result, dict):
                return result
            else:
                raise Validators.ValidationError("Input is not a valid JSON object. It must be a dictionary.")
        except json.JSONDecodeError:
            raise Validators.ValidationError("Input is not valid JSON.")

    @staticmethod
    def button_name_validator(name):
        if re.fullmatch(r'[a-zA-Z0-9\s-]+', name):
            return name
        raise Validators.ValidationError("Button name can only contain letters, numbers, spaces, and hyphens.")

    @staticmethod
    def entity_validator(name):
        if re.fullmatch(r'[a-zA-Z]+', name):
            return name
        raise Validators.ValidationError("Entity name can only contain letters.")

    @staticmethod
    def hook_name_validator(name):
        if re.fullmatch(r'[a-zA-Z_]+', name):
            return name
        raise Validators.ValidationError("Hook name can only contain letters and underscores.")

    @staticmethod
    def empty_string_validator(value):
        if value.strip():
            return value
        raise Validators.ValidationError("Input cannot be empty.")


class ValidationOptions:
    Float = Validators.float_validator
    ArrayInt = Validators.array_int_validator
    String = Validators.string_validator
    TrueFalse = Validators.true_false_validator
    Integer = Validators.integer_validator
    Array = Validators.array_validator
    JsonObject = Validators.json_object_validator

    Float.description = "\033[93mOption data type: Float\nRequired input format: Any number with or without decimal points\033[0m"
    ArrayInt.description = "\033[93mOption data type: Array of Integers\nRequired input format: [1, 2, 3]\033[0m"
    String.description = "\033[93mOption type: String\nRequired input format: Any text\033[0m"
    TrueFalse.description = "\033[93mOption data type: Boolean\nRequired input format: true or false\033[0m"
    Integer.description = "\033[93mOption data type: Integer\nRequired input format: Any whole number\033[0m"
    Array.description = "\033[93mOption data type: Array\nRequired input format: [\"value1\", \"value2\", \"value3\"]\033[0m"
    JsonObject.description = "\033[93mOption data type: JSON Object\nRequired input format: {\"key1\": \"value1\", \"key2\": \"value2\"}\033[0m"
