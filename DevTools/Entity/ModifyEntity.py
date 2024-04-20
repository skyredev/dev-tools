import importlib
import json
import os

from DevTools.Base.BaseCommand import BaseCommand


class ModifyEntity(BaseCommand):
    MODIFY_ACTIONS = {
        "1": "Add Field",
        "2": "Delete Field",
        "3": "Translate Field",
        "4": "Add Link",
        "5": "Delete Link",
        "6": "Translate Link",
        "7": "Exit"
    }

    YES_NO = {
        "1": "Yes",
        "2": "No"
    }

    def __init__(self):
        super().__init__(commandFile=__file__)

    def modify(self, filepath):
        while True:
            choice = (self.TerminalManager.get_choice
                      (self.TerminalManager.sent_choice_to_user("Entity exists. Choose an action:",
                                                                self.MODIFY_ACTIONS),
                       self.MODIFY_ACTIONS
                       ))
            match choice:
                case "Add Field":
                    self.add_values(filepath, ['fields'])
                case "Delete Field":
                    self.delete_keys(filepath, ['fields'])
                case "Translate Field":
                    self.translate_field(filepath)
                case "Add Link":
                    self.add_values(filepath, ['links'])
                case "Delete Link":
                    self.delete_keys(filepath, ['links'])
                case "Translate Link":
                    self.translate_field(filepath)
                case "Exit":
                    break

    def add_values(self, filepath, section_path):
        selectedValue = ""
        if section_path[0] == 'fields':
            selectedValue = 'field'
        else:
            selectedValue = 'link'

        while True:
            values = self.get_available_values(section_path)
            values_dict = {str(i + 1): field for i, field in enumerate(values)}
            value_type = self.TerminalManager.get_choice(
                self.TerminalManager.sent_choice_to_user(f"Select a {selectedValue} to add or 'Exit' to finish:",
                                                         values_dict),
                values_dict)

            if value_type == 'Exit':
                break

            value_name = self.TerminalManager.get_user_input(f"Enter the name for the new {selectedValue}")
            label = self.TerminalManager.get_user_input("Enter the label for the new field", default=value_name)
            # TODO: Add a check to see if the field already exists (?)
            # TODO: Add setting labels, fiels, link ... in i18n file
            # TODO: Implement the translation logic
            # TODO: Ask about filedDefs etc.
            # TODO: Tooltip for the field (optional) + add tooltip: true to entity

            value_instance = self.get_value_instance(value_type, value_name, section_path)
            options = value_instance.availableOptions
            self.configure_value_options(options, value_instance)

            field_data = value_instance.generate_data()
            print(f"\033[94m{value_name}: {json.dumps(field_data, indent=4)}\033[0m")

            self.MetadataManager.set(section_path, value_name, field_data, filepath)

    def get_available_values(self, section_path):
        if section_path[0] == 'fields':
            values_dir = os.path.join(self.script_dir, 'Fields')
        else:
            values_dir = os.path.join(os.path.dirname(__file__), 'Links')

        values = [filename.split('.')[0] for filename in os.listdir(values_dir) if
                  filename.endswith('.py') and filename != '__init__.py']
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
            print(f"\033[94m{value_instance.get_name()}: {json.dumps(value_instance.generate_data(), indent=4)}\033[0m")

        value_instance.set_value('isCustom', True)

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
                    f"\033[93mAre you sure you want to delete the field '{section_path[0]}'?\033[0m",
                    self.YES_NO),
                self.YES_NO)

            if confirm == "Yes":
                self.MetadataManager.delete(section_path, field_choice, filepath)
                print(f"\033[93m'{field_choice}' has been deleted\033[0m")
            else:
                print(f"\033[93m'{field_choice}' was not deleted\033[0m")

    @staticmethod
    def translate_field(filepath):
        print("Translation logic here")
