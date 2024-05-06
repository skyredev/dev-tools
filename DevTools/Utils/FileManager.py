import os
import json


class FileManager:

    def __init__(self, TerminalManager, TemplateManager, MetadataManager, Validators, cache_path):
        self.TerminalManager = TerminalManager
        self.TemplateManager = TemplateManager
        self.MetadataManager = MetadataManager
        self.Validators = Validators
        self.cache_path = cache_path
        self.resources_dir = os.path.join(os.path.dirname(__file__), '../../src/backend/Resources')

    YES_NO = [
        "Yes",
        "No"
    ]

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
                    if value and value[0] == "__APPEND__":
                        existing_items = {json.dumps(item, sort_keys=True) for item in merged_json[key]}
                        for item in value[1:]:
                            item_json = json.dumps(item, sort_keys=True)
                            if item_json not in existing_items:
                                merged_json[key].append(item)
                                existing_items.add(item_json)
                    else:
                        existing_items = {json.dumps(item, sort_keys=True) for item in merged_json[key]}
                        for item in value:
                            item_json = json.dumps(item, sort_keys=True)
                            if item_json not in existing_items:
                                merged_json[key].append(item)
                                existing_items.add(item_json)
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
        if extension == 'folder':
            if exclude is None:
                exclude = ['__init__.py']
            folder_names = [folder for folder in os.listdir(directory) if
                            os.path.isdir(os.path.join(directory, folder)) and folder not in exclude]
            return folder_names

        else:
            if exclude is None:
                exclude = ['__init__.py']

            if not os.path.exists(directory) or not os.path.isdir(directory):
                return []

            file_names = [filename.split('.')[0] for filename in os.listdir(directory) if
                          filename.endswith(extension) and filename not in exclude]
            return file_names

    def get_entity_defs_cache_path(self, entity_name):
        return os.path.join(self.cache_path, f"entityDefs/{entity_name}.json")

    def get_entity_defs_path(self, entity_name):
        return os.path.join(self.resources_dir, f"metadata/entityDefs/{entity_name}.json")

    def get_scopes_path(self, entity_name):
        return os.path.join(self.resources_dir, f"metadata/scopes/{entity_name}.json")

    def get_record_defs_path(self, entity_name):
        return os.path.join(self.resources_dir, f"metadata/recordDefs/{entity_name}.json")

    def get_client_defs_path(self, entity_name):
        return os.path.join(self.resources_dir, f"metadata/clientDefs/{entity_name}.json")

    def get_i18n_path(self, entity_name=None, language_code=None):
        if language_code is None:
            return os.path.join(self.resources_dir, "i18n")
        return os.path.join(self.resources_dir, f"i18n/{language_code}/{entity_name}.json")

    def add_translations(self, entity_name, section_path, key, default_value):
        default_translation_filepath = self.ensure_json_exists(self.get_i18n_path(entity_name, 'en_US'))

        other_languages = self.get_file_names(self.get_i18n_path(), extension='folder', exclude=['en_US'])

        self.MetadataManager.set(section_path, key, default_value, default_translation_filepath)
        for language in other_languages:
            add_translation = self.TerminalManager.get_choice_with_autocomplete(
                f"Would you like to set a translation for {'>'.join(section_path)}>{key} in {language}? ",
                self.YES_NO,
                validator=self.Validators.ChoiceValidator(self.YES_NO)
            )
            if add_translation == "Yes":
                translation_filepath = self.ensure_json_exists(
                    self.get_i18n_path(entity_name, language))

                translation = self.TerminalManager.get_user_input(
                    f"Enter the translation for {'>'.join(section_path)}>{key} in {language}")
                self.MetadataManager.set(section_path, key, translation, translation_filepath)
