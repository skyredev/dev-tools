from DevTools.Utils.Validators import (
    entity_validator, entity_validator_error,
    empty_string_validator, empty_string_validator_error,
)

from DevTools.Utils.TerminalManager import TerminalManager
from DevTools.Utils.Configurator import Configurator
from DevTools.Utils.FileManager import FileManager
from DevTools.Utils.TemplateManager import TemplateManager


class BaseCommand:

    def __init__(self):
        self.Configurator = Configurator()
        self.TerminalManager = TerminalManager()
        self.TemplateManager = TemplateManager()
        self.FileManager = FileManager(self.TerminalManager, self.TemplateManager)

    def get_module(self):
        module = self.TerminalManager.get_user_input(
            "Enter the module name", empty_string_validator, empty_string_validator_error(),
            default=self.Configurator.get_module_suggestion())
        return module

    def get_entity_name(self):
        entity = self.TerminalManager.get_user_input("Enter the entity name",
                                                     entity_validator,
                                                     entity_validator_error())
        return entity
