import os

from DevTools.Utils.Validators import (
    entity_validator, empty_string_validator
)

from DevTools.Utils.TerminalManager import TerminalManager
from DevTools.Utils.Configurator import Configurator
from DevTools.Utils.FileManager import FileManager
from DevTools.Utils.TemplateManager import TemplateManager
from DevTools.Utils.MetadataManager import MetadataManager


class BaseCommand:

    def __init__(self, commandFile):
        self.script_dir = os.path.dirname(os.path.abspath(commandFile))
        self.Configurator = Configurator()
        self.TerminalManager = TerminalManager()
        self.TemplateManager = TemplateManager()
        self.MetadataManager = MetadataManager()
        self.FileManager = FileManager(self.TerminalManager, self.TemplateManager)



    def get_module(self):
        module = self.TerminalManager.get_user_input(
            "Enter the module name", empty_string_validator, default=self.Configurator.get_module_suggestion())
        return module

    def get_entity_name(self):
        entity = self.TerminalManager.get_user_input("Enter the entity name", entity_validator)
        return entity
