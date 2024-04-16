import re


class ValidationOptions:
    Float = None
    Int = None
    ArrayInt = None
    TrueFalse = "true/false"
    String = "string"
    Integer = "integer"
    Array = "array"


def validate_input(prompt, validator=None, error_message=None, default=None):
    while True:
        if default is None:
            user_input = input(f"{prompt}: ")
        else:
            user_input = input(f"{prompt} (default: {default}): ") or default

        if validator is None or validator(user_input):
            return user_input
        else:
            if error_message:
                print("Invalid input. " + error_message)
            else:
                print("Invalid input. Please try again.")


# Validators #
def button_name_validator(name):
    return re.fullmatch(r'[a-zA-Z0-9\s-]+', name) is not None


def entity_validator(name):
    return re.fullmatch(r'[a-zA-Z]+', name) is not None


def hook_name_validator(name):
    return re.fullmatch(r'[a-zA-Z_]+', name) is not None


def empty_string_validator(name):
    return bool(name.strip())


def converted_name_validator(name):
    return re.fullmatch(r'[a-z0-9-]+', name) is not None


# Validator error messages #
def button_name_validator_error():
    return "Button name can only contain letters, numbers, spaces, and hyphens."


def entity_validator_error():
    return "Entity name can only contain letters."


def hook_name_validator_error():
    return "Hook name can only contain letters and underscores."


def empty_string_validator_error():
    return "Input cannot be empty."


def converted_name_validator_error():
    return "Converted name can only contain lowercase letters, numbers, and hyphens."
