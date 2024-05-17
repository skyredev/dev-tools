import json
import os

from DevTools.Utils.Validators import Validators
from DevTools.Utils.TerminalManager import TerminalManager
from DevTools.Utils.FileManager import FileManager
from DevTools.Utils.TemplateManager import TemplateManager
from DevTools.Utils.MetadataManager import MetadataManager
from DevTools.Utils.CacheManager import CacheManager
from DevTools.Utils.PathManager import PathManager


class BaseCommand:

    def __init__(self, command_file):

        ## SCRIPT PATHS ##
        self.current_dir = os.getcwd()
        self.script_path = os.path.dirname(os.path.abspath(command_file))

        ## DIRECTORIES ##
        self.entity_defs_dir = os.path.join(self.current_dir, "src/backend/Resources/metadata/entityDefs")
        self.i18n_dir = os.path.join(self.current_dir, "src/backend/Resources/i18n")
        self.controllers_dir = os.path.join(self.current_dir, "src/backend/Controllers")
        self.php_entities_dir = os.path.join(self.current_dir, "src/backend/Entities")
        self.services_dir = os.path.join(self.current_dir, "src/backend/Services")
        self.tools_dir = os.path.join(self.current_dir, "src/backend/Tools")
        self.api_actions_dir = os.path.join(self.current_dir, "src/backend/Api")
        self.mass_actions_dir = os.path.join(self.current_dir, "src/backend/MassAction")
        self.routes_path = os.path.join(self.current_dir, "src/backend/Resources/routes.json")

        ## ESSENTIAL PATHS ##
        self.tool_dir = os.path.join(self.current_dir, "apertia-tool")
        self.cache_dir = os.path.join(self.current_dir, "apertia-tool/cache")
        self.package_json_dir = os.path.join(self.current_dir, "package.json")

        ## VARIABLES ##
        self.languages = []
        self.default_language = ""

        ## UTILS ##
        self.Validators = Validators()
        self.TerminalManager = TerminalManager(self.Validators)
        self.TemplateManager = TemplateManager()
        self.MetadataManager = MetadataManager()
        self.PathManager = PathManager(self.current_dir)
        self.FileManager = FileManager(self.TerminalManager, self.TemplateManager, self.MetadataManager,
                                       self.PathManager,
                                       self.Validators, self.languages, self.default_language,
                                       self.colorization)
        self.CacheManager = CacheManager(self.FileManager)

        ## CONFIG ##
        self.read_config()

        ## CACHE ##
        self.metadata_entities = self.get_cache_list("entityDefs", self.entity_defs_dir, ".json")

        self.command_name_without_extension = os.path.basename(command_file).split(".")[0]

        if self.command_name_without_extension == "Controller_Command":
            self.controllers = self.get_cache_list("Controllers", self.controllers_dir, ".php")

        if self.command_name_without_extension == "Entity_PHP_Command":
            self.php_entities = self.get_cache_list("Entities", self.php_entities_dir, ".php")

        if self.command_name_without_extension == "Service_Command":
            self.services = self.get_cache_list("Services", self.services_dir, ".php")

        if self.command_name_without_extension == "Tool_Command":
            self.tools = self.get_cache_list("Tools", self.tools_dir, ".php")

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

    @staticmethod
    def file_exists_local_folder(file_name, folder, extension):
        if not os.path.exists(folder):
            return False
        lower_files = [f.lower() for f in os.listdir(folder)]
        if file_name.lower() + extension in lower_files:
            return True
        return False

    def get_extension_from_content(self, content, name, message=False):
        if "namespace" in content:
            namespace = content.split("namespace ")[1].split(";")[0]
        else:
            namespace = "NO NAMESPACE FOUND IN EXTENDING CONTROLLER"
        if message:
            print(self.colorization("green", f"New class will extend from {namespace}\\{name}"))
        return f"extends \\{namespace}\\{name}"

    def get_autocomplete_names(self, array, message, validator=None):
        if not validator:
            validator = self.Validators.entity_validator
        autocomplete_array = list(set([element[1] for element in array]))

        return self.TerminalManager.get_choice_with_autocomplete(
            message, autocomplete_array, validator=validator, send_choices=False)

    def get_cache_list(self, cache_name, local_path, extension):
        cache_path = os.path.join(self.cache_dir, cache_name)

        return self.CacheManager.fetch_cache(cache_path, [extension]) + self.CacheManager.fetch_cache(local_path,
                                                                                                      [extension])

    def read_config(self):
        config_path = os.path.join(self.tool_dir, 'config.json')
        if not os.path.exists(config_path):
            self.init_config()

        self.languages = self.MetadataManager.get(config_path, ['languages'])
        self.default_language = self.MetadataManager.get(config_path, ['default_language'])
        self.FileManager.languages = self.languages
        self.FileManager.default_language = self.default_language

    def init_config(self):
        if not os.path.exists(self.tool_dir):
            os.makedirs(self.tool_dir)

        content = self.FileManager.read_file(os.path.join(self.script_path, 'DevTools/config.json'))
        self.FileManager.write_file(os.path.join(self.tool_dir, 'config.json'), content)

        print(self.colorization("yellow",
                                f"Config initialized with default settings: {os.path.join(self.tool_dir, 'config.json')}\nYou can modify the config file to change the settings (Dev Tool must be restarted)"))

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
