import os
import json

class Configurator:
    def get_module_suggestion(self):
        if os.path.isfile(self.package_json_path):
            with open(self.package_json_path, "r") as file:
                package_data = json.load(file)
                return package_data.get("name", "")
        return ""