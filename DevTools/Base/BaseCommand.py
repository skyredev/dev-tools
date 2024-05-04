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
        self.current_dir = os.getcwd()
        self.script_path = os.path.dirname(os.path.abspath(command_file))
        self.Validators = Validators()
        self.TerminalManager = TerminalManager(self.Validators)
        self.TemplateManager = TemplateManager()
        self.MetadataManager = MetadataManager()
        self.FileManager = FileManager(self.TerminalManager, self.TemplateManager, self.MetadataManager, self.Validators)
        self.CacheManager = CacheManager(self.FileManager)
        self.entity_defs_dir = os.path.join(self.current_dir, "src/backend/Resources/metadata/entityDefs")
        self.package_json_dir = os.path.join(self.current_dir, "package.json")

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

    def cache_entities(self):
        instance_entities = self.CacheManager.get_instance_file_names("custom/Espo/Custom/Resources/metadata/entityDefs")
        local_entities = self.FileManager.get_file_names(self.entity_defs_dir, ".json")
        all_entities = instance_entities + local_entities
        content = {"instance": instance_entities, "local": local_entities, "all": all_entities}
        self.FileManager.write_file(os.path.join(self.current_dir, "cache/entities.json"), content)

    def get_entity_name(self):
        all_entities = self.MetadataManager.get("cache/entities.json", ['all'])
        print(all_entities)
        entity = self.TerminalManager.get_choice_with_autocomplete(
            "Enter the entity name: ", all_entities, send_choices=False, validator=self.Validators.entity_validator)
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
