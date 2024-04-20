import re


def array_validator(value):
    try:
        result = eval(value)
        if isinstance(result, list):
            return result
        raise ValidationError("Input is not a valid list.")
    except:
        raise ValidationError("Invalid input for a list.")


def integer_validator(value):
    if value.lstrip('-').isdigit():
        return int(value)
    raise ValidationError("Input is not a valid integer.")


def true_false_validator(value):
    value = value.strip().lower()
    if value in ['true', 'false']:
        return value == 'true'
    raise ValidationError("Input must be either 'true' or 'false'.")


def array_int_validator(value):
    try:
        items = eval(value)
        if isinstance(items, list) and all(isinstance(item, int) for item in items):
            return items
        raise ValidationError("List must contain only integers.")
    except:
        raise ValidationError("Invalid input for an array of integers.")


def float_validator(value):
    try:
        return float(value)
    except ValueError:
        raise ValidationError("Input is not a valid float.")


def string_validator(value):
    if isinstance(value, str):
        return value
    raise ValidationError("Input is not a valid string.")


def button_name_validator(name):
    if re.fullmatch(r'[a-zA-Z0-9\s-]+', name):
        return name
    raise ValidationError("Button name can only contain letters, numbers, spaces, and hyphens.")


def entity_validator(name):
    if re.fullmatch(r'[a-zA-Z]+', name):
        return name
    raise ValidationError("Entity name can only contain letters.")


def hook_name_validator(name):
    if re.fullmatch(r'[a-zA-Z_]+', name):
        return name
    raise ValidationError("Hook name can only contain letters and underscores.")


def empty_string_validator(value):
    if value.strip():
        return value
    raise ValidationError("Input cannot be empty.")


def validate_input(prompt, validator=None, default=None):
    while True:
        user_input = input(f"{prompt}: ") if default is None else input(f"{prompt} (default: {default}): ") or default
        try:
            if validator:
                return validator(user_input)
            return user_input
        except ValidationError as e:
            print(f"\033[91m{e}\033[0m")


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class ChoiceValidator:
    def __init__(self, choices):
        self.choices = choices

    def __call__(self, value):
        if value in self.choices:
            return value
        raise ValidationError("Invalid choice. Please try again.")


class ValidationOptions:
    Float = float_validator
    ArrayInt = array_int_validator
    String = string_validator
    TrueFalse = true_false_validator
    Integer = integer_validator
    Array = array_validator

    Float.description = "\033[93mOption data type: Float\nRequired input format: Any number with or without decimal points\033[0m"
    ArrayInt.description = "\033[93mOption data type: Array of Integers\nRequired input format: [1, 2, 3]\033[0m"
    String.description = "\033[93mOption type: String\nRequired input format: Any text\033[0m"
    TrueFalse.description = "\033[93mOption data type: Boolean\nRequired input format: true or false\033[0m"
    Integer.description = "\033[93mOption data type: Integer\nRequired input format: Any whole number\033[0m"
    Array.description = "\033[93mOption data type: Array\nRequired input format: [\"value1\", \"value2\", \"value3\"]\033[0m"

