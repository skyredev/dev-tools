import os
import json


class FileManager:

    def __init__(self, TerminalManager, TemplateManager):
        self.TerminalManager = TerminalManager
        self.TemplateManager = TemplateManager()

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

    def create_button_files(self, module, entity, view, button_type, label, name, style):
        entity = entity.upper()

        json_dir = os.path.join(self.TerminalManager.root_dir, "../../src/backend/Resources/metadata/clientDefs")
        json_file = os.path.join(json_dir, f"{entity}.json")
        self.create_directory(json_dir)

        new_json = get_json_template(command="button", view=view, button_type=button_type, label=label, name=name,
                                     module=module, entity=entity, style=style)
        merged_json = self.merge_json_file(json_file, new_json)
        with open(json_file, "w", encoding='utf-8') as file:
            json.dump(merged_json, file, indent=2, ensure_ascii=False)
        print(f"JSON file created/updated: {json_file}")

        js_dir = os.path.join(self.TerminalManager.root_dir, f"../src/client/src/handlers/{entity}")
        js_file = os.path.join(js_dir, f"{name}-handler.js")

        if os.path.isfile(js_file):
            print(f"Error: JS file already exists: {js_file}")
            return

        self.create_directory(js_dir)
        js_content = get_js_template("button", view, button_type, module, name, entity)
        with open(js_file, "w") as file:
            file.write(js_content.strip())
        print(f"JS file created: {js_file}")

    def create_hook_file(self, module, hook_type, name, entity):
        php_dir = os.path.join(self.TerminalManager.root_dir, f"../src/backend/Hooks/{entity}")
        php_file = os.path.join(php_dir, f"{name}.php")
        self.create_directory(php_dir)

        if os.path.isfile(php_file):
            print(f"Error: PHP file already exists: {php_file}")
            return

        php_content = get_php_template(module, hook_type, name, entity)
        with open(php_file, "w") as file:
            file.write(php_content.strip())
        print(f"PHP file created: {php_file}")

    def create_entity_files(self, module, entity_name, entity_type):
        entity_defs_dir = os.path.join(self.TerminalManager.root_dir, "../src/backend/Resources/metadata/entityDefs")
        entity_defs_file = os.path.join(entity_defs_dir, f"{entity_name}.json")
        self.create_directory(entity_defs_dir)
        entity_defs_json = get_json_template(command="entity", entity_name=entity_name, entity_type=entity_type)
        with open(entity_defs_file, "w", encoding='utf-8') as file:
            json.dump(entity_defs_json, file, indent=2, ensure_ascii=False)
        print(f"entityDefs JSON file created: {entity_defs_file}")

        scopes_dir = os.path.join(self.TerminalManager.root_dir, "../src/backend/Resources/metadata/scopes")
        scopes_file = os.path.join(scopes_dir, f"{entity_name}.json")
        self.create_directory(scopes_dir)
        scopes_json = get_json_template(command="scope", entity_name=entity_name, entity_type=entity_type,
                                        module=module)
        with open(scopes_file, "w", encoding='utf-8') as file:
            json.dump(scopes_json, file, indent=2, ensure_ascii=False)
        print(f"scopes JSON file created: {scopes_file}")
