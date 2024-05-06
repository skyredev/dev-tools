import json
import os

from DevTools.Utils.Validators import Validators
from DevTools.Utils.TerminalManager import TerminalManager
from DevTools.Utils.FileManager import FileManager
from DevTools.Utils.TemplateManager import TemplateManager
from DevTools.Utils.MetadataManager import MetadataManager
from DevTools.Utils.CacheManager import CacheManager


class BaseCommand:

    def __init__(self, command_file):

        ## PATHS ##
        self.current_dir = os.getcwd()
        self.script_path = os.path.dirname(os.path.abspath(command_file))
        self.entity_defs_dir = os.path.join(self.current_dir, "src/backend/Resources/metadata/entityDefs")
        self.i18n_dir = os.path.join(self.current_dir, "src/backend/Resources/i18n")
        self.controllers_dir = os.path.join(self.current_dir, "src/backend/Controllers")
        self.cache_path = os.path.join(self.current_dir, "apertia-tool/cache")
        self.package_json_dir = os.path.join(self.current_dir, "package.json")

        ## UTILS ##
        self.Validators = Validators()
        self.TerminalManager = TerminalManager(self.Validators)
        self.TemplateManager = TemplateManager()
        self.MetadataManager = MetadataManager()
        self.FileManager = FileManager(self.TerminalManager, self.TemplateManager, self.MetadataManager, self.Validators, self.cache_path)
        self.CacheManager = CacheManager(self.FileManager)

    def get_module_suggestion(self):
        if os.path.isfile(self.package_json_dir):
            with open(self.package_json_dir, "r") as file:
                package_data = json.load(file)
                return package_data.get("name", "")
        return ""

    def get_module(self):
        module = self.TerminalManager.get_user_input(
            "Enter the module name", self.Validators.empty_string_validator, default=self.get_module_suggestion())
        return module

    def get_entity_name(self):
        entities = self.FileManager.get_file_names(os.path.join(self.cache_path, "entityDefs"), ".json")
        entity = self.TerminalManager.get_choice_with_autocomplete(
            "Enter the entity name: ", entities, validator=self.Validators.entity_validator, send_choices=False)
        return entity

    @staticmethod
    def colorization(color, text):
        if color == 'red':
            return f"\033[91m{text}\033[0m"
        elif color == 'green':
            return f"\033[92m{text}\033[0m"
        elif color == 'yellow':
            return f"\033[93m{text}\033[0m"
        elif color == 'blue':
            return f"\033[94m{text}\033[0m"
        elif color == 'magenta':
            return f"\033[95m{text}\033[0m"
        else:
            return text
