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

    def ensure_json_exists(self, file_path):
        if not os.path.exists(file_path):
            self.write_file(file_path, '{}')
        return file_path

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

    @staticmethod
    def read_file(source_path):
        # Load file from path_to_template
        try:
            with open(source_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
        except json.JSONDecodeError:
            with open(source_path, 'r', encoding='utf-8') as file:
                content = file.read()
        return content

    def write_file(self, destination_path, content):
        self.create_directory(os.path.dirname(destination_path))

        if isinstance(content, str):
            with open(destination_path, 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            with open(destination_path, 'w', encoding='utf-8') as file:
                json.dump(content, file, indent=2, ensure_ascii=False)

        print(f"File created/updated: {destination_path}")

    @staticmethod
    def get_file_names(directory, extension='.py', exclude=None):
        if exclude is None:
            exclude = ['__init__.py']

        if not os.path.exists(directory) or not os.path.isdir(directory):
            return []

        file_names = [filename.split('.')[0] for filename in os.listdir(directory) if
                      filename.endswith(extension) and filename not in exclude]
        return file_names
