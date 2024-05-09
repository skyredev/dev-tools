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
        self.tool_path = os.path.join(self.current_dir, "apertia-tool")
        self.cache_path = os.path.join(self.current_dir, "apertia-tool/cache")
        self.package_json_dir = os.path.join(self.current_dir, "package.json")

        ## VARIABLES ##
        self.languages = []
        self.default_language = ""

        ## UTILS ##
        self.Validators = Validators()
        self.TerminalManager = TerminalManager(self.Validators)
        self.TemplateManager = TemplateManager()
        self.MetadataManager = MetadataManager()
        self.FileManager = FileManager(self.TerminalManager, self.TemplateManager, self.MetadataManager,
                                       self.Validators, self.cache_path, self.languages, self.default_language,
                                       self.colorization)
        self.CacheManager = CacheManager(self.FileManager)

        ## CONFIG ##
        self.read_config()

        ## CACHE ##
        self.entities = self.get_entities_list()

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
        auto_complete_entities_array = list(set([entity[1] for entity in self.entities]))

        entity = self.TerminalManager.get_choice_with_autocomplete(
            "Enter the entity name: ", auto_complete_entities_array, validator=self.Validators.entity_validator,
            send_choices=False)
        return entity

    def get_entities_list(self):
        entity_defs_cache = os.path.join(self.cache_path, "entityDefs")
        entity_defs_local = self.entity_defs_dir

        entities = self.CacheManager.fetch_cache(entity_defs_cache, [".json"]) + self.CacheManager.fetch_cache(
            entity_defs_local, [".json"])
        return entities

    def read_config(self):
        config_path = os.path.join(self.tool_path, 'config.json')
        if not os.path.exists(config_path):
            self.init_config()

        self.languages = self.MetadataManager.get(config_path, ['languages'])
        self.default_language = self.MetadataManager.get(config_path, ['default_language'])
        self.FileManager.languages = self.languages
        self.FileManager.default_language = self.default_language

    def init_config(self):
        if not os.path.exists(self.tool_path):
            os.makedirs(self.tool_path)

        content = self.FileManager.read_file(os.path.join(self.script_path, 'DevTools/config.json'))
        self.FileManager.write_file(os.path.join(self.tool_path, 'config.json'), content)

        print(self.colorization("yellow",
                                f"Config initialized with default settings: {os.path.join(self.tool_path, 'config.json')}\nYou can modify the config file to change the settings (Dev Tool must be restarted)"))

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
