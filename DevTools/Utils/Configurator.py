import os
import json


class Configurator:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.package_json_path = os.path.join(self.root_dir, "../../package.json")

    def get_module_suggestion(self):
        if os.path.isfile(self.package_json_path):
            with open(self.package_json_path, "r") as file:
                package_data = json.load(file)
                return package_data.get("name", "")
        return ""
