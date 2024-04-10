from ..validators import (
    button_name_validator, button_name_validator_error,
    entity_validator, entity_validator_error,
    empty_string_validator, empty_string_validator_error,
    hook_name_validator, hook_name_validator_error
)

from ..Utils.TerminalManager import TerminalManager
from ..Utils.Configurator import Configurator
from ..filegenerators import FileGenerator

class BaseCommand:

    def __init__(self):
        self.Configurator = Configurator()
        self.TerminalManager = TerminalManager()
        self.FileGenerator = FileGenerator(self.TerminalManager)

    def get_module(self):
        module = self.TerminalManager.get_user_input(
            "Enter the module name", empty_string_validator, empty_string_validator_error(),
            default=self.TerminalManager.get_module_suggestion())
        return module

    def get_entity_name(self):
        entity = self.TerminalManager.get_user_input("Enter the entity name",
                                                     entity_validator,
                                                     entity_validator_error())
        return entity