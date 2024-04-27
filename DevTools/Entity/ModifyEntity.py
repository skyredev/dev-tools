import importlib
import json
import os

from DevTools.Base.BaseCommand import BaseCommand


class ModifyEntity(BaseCommand):
    MODIFY_ACTIONS = {
        "1": "Add Field",
        "2": "Delete Field",
        "3": "Add Link",
        "4": "Delete Link",
        "5": "Translate Value",
        "6": "Exit"
    }

    YES_NO = {
        "1": "Yes",
        "2": "No"
    }

    LANGUAGES = {
        "1": "cs_CZ",
        "2": "en_US"
    }

    def __init__(self):
        super().__init__(commandFile=__file__)

    def modify(self, filepath, entity_name):
        while True:
            choice = (self.TerminalManager.get_choice
                      (self.TerminalManager.sent_choice_to_user("Entity exists. Choose an action:",
                                                                self.MODIFY_ACTIONS),
                       self.MODIFY_ACTIONS
                       ))
            match choice:
                case "Add Field":
                    self.add_values(filepath, ['fields'], entity_name)
                case "Delete Field":
                    self.delete_keys(filepath, ['fields'])
                case "Add Link":
                    self.add_values(filepath, ['links'], entity_name)
                case "Delete Link":
                    self.delete_keys(filepath, ['links'])
                case "Translate Value":
                    self.translate_values(entity_name)
                case "Exit":
                    break

    def add_values(self, filepath, section_path, entity_name):
        translation_filepath = self.FileManager.ensure_json_exists(os.path.join(self.script_dir,
                                                                                f"../../src/backend/Resources/i18n/en_US/{entity_name}.json"))
        selectedValue = ""
        if section_path[0] == 'fields':
            selectedValue = 'field'
        else:
            selectedValue = 'link'

        while True:
            values = self.get_available_values(section_path)
            value_type = self.TerminalManager.get_choice_with_autocomplete(
                f"Start typing a {selectedValue} type you want to add or 'Exit' to finish: ",
                values, send_choices=True, validator=self.Validators.ChoiceValidator(values)
            )

            if value_type == 'Exit':
                break

            value_name = self.TerminalManager.get_converted_field_name(
                self.TerminalManager.get_user_input(f"Enter the name for the new {selectedValue}"),
                selectedValue.capitalize())
            label = self.TerminalManager.get_user_input("Enter the label for the new field",
                                                        default=value_name[0].upper() + value_name[1:])

            hiddenField = ""
            tooltip = "None"
            if selectedValue == 'field':
                hiddenField = self.TerminalManager.get_choice(
                    self.TerminalManager.sent_choice_to_user("Is this field hidden?", self.YES_NO),
                    self.YES_NO
                )

                tooltip = self.TerminalManager.get_user_input("Enter the tooltip for the new field", default='None')

            value_instance = self.get_value_instance(value_type, value_name, section_path)
            options = value_instance.availableOptions
            self.configure_value_options(options, value_instance)
            if hiddenField == "Yes":
                value_instance.set_value('hidden', True)
            if tooltip != "None":
                value_instance.set_value('tooltip', True)

            value_instance.set_value('isCustom', True)

            field_data = value_instance.get_data()
            print(f"\033[94m{value_name}: {json.dumps(field_data, indent=4)}\033[0m")

            if section_path[0] == 'fields':
                linkDefs = value_instance.get_link_defs()
                if len(linkDefs) > 0:
                    print('Link Definitions:')
                    print(self.colorization('blue', f"{value_name}: {json.dumps(linkDefs, indent=4)}"))
                    self.MetadataManager.set(['links'], value_name, linkDefs, filepath)

            self.MetadataManager.set(section_path, value_name, field_data, filepath)
            self.MetadataManager.set(section_path, value_name, label, translation_filepath)
            if tooltip != "None":
                self.MetadataManager.set(['tooltips'], value_name, tooltip, translation_filepath)

    def get_available_values(self, section_path):
        if section_path[0] == 'fields':
            values_dir = os.path.join(self.script_dir, 'Fields')
        else:
            values_dir = os.path.join(os.path.dirname(__file__), 'Links')

        values = self.FileManager.get_file_names(values_dir)
        values.append('Exit')
        return values

    @staticmethod
    def get_value_instance(value_type, value_name, section_path):
        try:
            if section_path[0] == 'fields':
                value_module = importlib.import_module(f"DevTools.Entity.Fields.{value_type}")
            else:
                value_module = importlib.import_module(f"DevTools.Entity.Links.{value_type}")

            value_class = getattr(value_module, value_type)
            value_instance = value_class(value_name)
            return value_instance
        except ModuleNotFoundError:
            print(f"No module found for the value type: {value_type}")
            return {}, value_type.lower()
        except AttributeError:
            print(f"No class found for the value type: {value_type} in the module")
            return {}, value_type.lower()

    def configure_value_options(self, options, value_instance):
        option_keys = {str(i + 1): option for i, option in enumerate(options.keys())}
        option_keys[str(len(option_keys) + 1)] = 'Exit'  # Add 'Exit' as the last option

        while True:
            option_choice = self.TerminalManager.get_choice(
                self.TerminalManager.sent_choice_to_user("Select an option to configure or 'Exit' to finish",
                                                         option_keys),
                option_keys)

            if option_choice == 'Exit':
                break

            validator = options.get(option_choice)
            description = getattr(validator, 'description', "No description available.")

            # Show the description before getting user input
            print(description)
            value = self.TerminalManager.get_user_input(f"Set value for {option_choice}", validator)
            value_instance.set_value(option_choice, value)
            print(self.colorization('blue',
                                    f"{value_instance.get_name()}: {json.dumps(value_instance.get_data(), indent=4)})"))

    def delete_keys(self, filepath, section_path):

        while True:
            keys = self.MetadataManager.list(section_path, filepath)
            if not keys:
                print("No fields available to delete.")
                return

            keys_dict = {str(i + 1): key for i, key in enumerate(keys)}
            keys_dict[str(len(keys_dict) + 1)] = "Exit"

            field_choice = self.TerminalManager.get_choice(
                self.TerminalManager.sent_choice_to_user(f"Select a {section_path[0]} to delete or 'Exit' to finish:",
                                                         keys_dict),
                keys_dict)

            if field_choice == 'Exit':
                break

            confirm = self.TerminalManager.get_choice(
                self.TerminalManager.sent_choice_to_user(
                    self.colorization('yellow', f"Are you sure you want to delete '{field_choice}'?"),
                    self.YES_NO),
                self.YES_NO)

            if confirm == "Yes":
                self.MetadataManager.delete(section_path, field_choice, filepath)
                print(self.colorization('yellow', f"'{field_choice}' was deleted"))
            else:
                print(self.colorization('yellow', f"'{field_choice}' was not deleted"))

    def translate_values(self, entity_name):
        language = self.TerminalManager.get_choice(
            self.TerminalManager.sent_choice_to_user("Select the language to translate to:", self.LANGUAGES),
            self.LANGUAGES)

        opposite_language = "cs_CZ" if language == "en_US" else "en_US"
        filepath = self.FileManager.ensure_json_exists(os.path.join(self.script_dir,
                                                                    f"../../src/backend/Resources/i18n/{opposite_language}/{entity_name}.json"))
        translation_filepath = self.FileManager.ensure_json_exists(os.path.join(self.script_dir,
                                                                                f"../../src/backend/Resources/i18n/{language}/{entity_name}.json"))

        data = self.MetadataManager.get(filepath)
        if not data:
            print("No data available to translate.")
            return

        self.translate_section(data, [], translation_filepath)

    def translate_section(self, section_data, section_path, translation_filepath):
        if isinstance(section_data, dict):
            items = {str(i + 1): key for i, key in enumerate(section_data.keys())}
            items[str(len(items) + 1)] = "Exit"

            while True:
                item_choice = self.TerminalManager.get_choice(
                    self.TerminalManager.sent_choice_to_user(f"Select an item to translate or 'Exit' to finish:",
                                                             items),
                    items)

                if item_choice == 'Exit':
                    break

                key = item_choice
                new_section_path = section_path + [key]
                current_value = section_data[key]

                if isinstance(current_value, dict):
                    # Recursively call translate_section if the selected item is a dictionary
                    self.translate_section(current_value, new_section_path, translation_filepath)
                else:
                    # Handle translation of the simple value
                    print(self.colorization('blue', f"Current value: {current_value}"))
                    translated_value = self.TerminalManager.get_user_input(
                        f"Enter the translation for '{' > '.join(new_section_path)}'")
                    self.MetadataManager.set(section_path, item_choice, translated_value, translation_filepath)
                    print(self.colorization('green',
                                            f"Value '{' > '.join(new_section_path)}' translated to '{translated_value}' and saved"))
