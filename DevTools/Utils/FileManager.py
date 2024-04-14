import os
import json


class FileManager:

    def __init__(self, TerminalManager, TemplateManager):
        self.TerminalManager = TerminalManager
        self.TemplateManager = TemplateManager

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def merge_json(self, existing_json, new_json):
        merged_json = existing_json.copy()
        for key, value in new_json.items():
            if key in merged_json:
                if isinstance(value, dict):
                    merged_json[key] = self.merge_json(merged_json[key], value)
                elif isinstance(value, list):
                    if value[0] == "__APPEND__":
                        merged_json[key].extend(value[1:])
                    else:
                        merged_json[key] = value
                else:
                    merged_json[key] = value
            else:
                merged_json[key] = value
        return merged_json

    def merge_json_file(self, json_file, new_json):
        if os.path.isfile(json_file):
            with open(json_file, "r") as file:
                existing_json = json.load(file)
            return self.merge_json(existing_json, new_json)
        else:
            return new_json

    def read_file(self, source_path):
        # Load file from path_to_template
        with open(source_path, 'r') as file:
            content = file.read()

        return content

    def write_file(self, destination_path, content):
        self.create_directory(os.path.dirname(destination_path))

        with open(destination_path, 'w') as file:
            file.write(content)
