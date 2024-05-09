import importlib
import json
import os

from DevTools.Base.BaseCommand import BaseCommand


class ModifyEntity(BaseCommand):
    MODIFY_ACTIONS = [
        "Add Field",
        "Delete Field",
        "Add Link",
        "Delete Link",
        "Translate Value",
        "Exit"
    ]

    YES_NO = [
        "Yes",
        "No"
    ]

    def __init__(self):
        super().__init__(command_file=__file__)

    def modify(self, filepath, entity_name, entities: list):
        while True:
            choice = self.TerminalManager.get_choice_with_autocomplete(
                f"Entity '{entity_name}' already exists. What would you like to do? ",
                self.MODIFY_ACTIONS,
                validator=self.Validators.ChoiceValidator(self.MODIFY_ACTIONS)
            )
            match choice:
                case "Add Field":
                    self.add_values(filepath, ['fields'], entity_name, entities)
                case "Delete Field":
                    self.delete_keys(filepath, ['fields'], entity_name)
                case "Add Link":
                    self.add_values(filepath, ['links'], entity_name, entities)
                case "Delete Link":
                    self.delete_keys(filepath, ['links'], entity_name)
                case "Translate Value":
                    self.translate_values(entity_name)
                case "Exit":
                    break

    def add_values(self, filepath, section_path, entity_name, entities: list):
        self.FileManager.ensure_file_exists(filepath)

        selectedValue = ""
        if section_path[0] == 'fields':
            selectedValue = 'field'
        else:
            selectedValue = 'link'

        existing_values = []
        for entity in entities:
            if entity[1] == entity_name:
                fetched_values = self.MetadataManager.list(section_path, entity[0])
                for value in fetched_values:
                    existing_values.append(value.lower())
        existing_values = list(set(existing_values))

        while True:
            values = self.get_available_values(section_path)
            value_type = self.TerminalManager.get_choice_with_autocomplete(
                f"Start typing a {selectedValue} type you want to add or 'Exit' to finish: ",
                values, validator=self.Validators.ChoiceValidator(values)
            )
            if value_type == 'Exit':
                break

            while True:
                value_name = self.TerminalManager.get_user_input(f"Enter the name for the new {selectedValue}",
                                                                 validator=self.Validators.empty_string_validator)

                if value_name.lower().strip() in existing_values:
                    print(self.colorization('red',
                                            f"Field '{value_name}' already exists. Please choose a different name."))
                    continue
                else:
                    value_name = self.TerminalManager.get_converted_field_name(value_name, selectedValue.capitalize())
                    break

            label = self.TerminalManager.get_user_input("Enter the label for the new field",
                                                        default=value_name[0].upper() + value_name[1:])

            hiddenField = ""
            tooltip = "None"

            if selectedValue == 'field':
                hiddenField = self.TerminalManager.get_choice_with_autocomplete(
                    "Should the field be hidden? ", self.YES_NO, validator=self.Validators.ChoiceValidator(self.YES_NO)
                )

                tooltip = self.TerminalManager.get_user_input("Enter the tooltip for the new field", default='None')

            value_instance = self.get_value_instance(value_type, value_name, section_path)
            options = value_instance.availableOptions
            options_AvailableValues = value_instance.availableOptionsAvailableValues
            options_AvailableTranslations = value_instance.availableOptionsForTranslate

            self.configure_value_options(options, options_AvailableValues, options_AvailableTranslations,
                                         value_instance, entity_name)

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

            self.FileManager.add_translations(entity_name, section_path, value_name, label)

            if tooltip != "None":
                self.FileManager.add_translations(entity_name, ['tooltips'], value_name, tooltip)

    def get_available_values(self, section_path):
        if section_path[0] == 'fields':
            values_dir = os.path.join(self.script_path, 'Fields')
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

    def configure_value_options(self, options, availableValues, availableTranslations, value_instance, entity_name):
        option_keys = list(options.keys())
        option_keys.append('Exit')
        while True:
            option_choice = self.TerminalManager.get_choice_with_autocomplete(
                "Select an option to configure or 'Exit' to finish: ",
                option_keys, validator=self.Validators.ChoiceValidator(option_keys)
            )

            if option_choice == 'Exit':
                break

            optionAvailableValues = availableValues.get(option_choice, [])

            if optionAvailableValues:
                value = self.TerminalManager.get_choice_with_autocomplete(
                    f"Select an option value for '{option_choice}': ",
                    optionAvailableValues, validator=self.Validators.ChoiceValidator(optionAvailableValues)
                )

            else:
                validator = options.get(option_choice)
                description = getattr(validator, 'description', "No description available.")

                # Show the description before getting user input
                print(description)

                value = self.TerminalManager.get_user_input(f"Set value for {option_choice}", validator)

            if option_choice == 'options' and 'style' in options:
                style = {}
                styles = availableValues.get('style', [])
                for option in value:
                    if option_choice in availableTranslations:
                        self.FileManager.add_translations(entity_name, ['options', value_instance.get_name()], option, option)
                    option_style = self.TerminalManager.get_choice_with_autocomplete(f"Select a style for '{option}': ", styles, validator=self.Validators.ChoiceValidator(styles))
                    if option_style == 'Default':
                        option_style = None
                    else:
                        option_style = option_style.lower()
                    style[option] = option_style

                value_instance.set_value('style', style)

            elif option_choice in availableTranslations:
                for option in value:
                    self.FileManager.add_translations(entity_name, ['options', value_instance.get_name()], option, option)

            value_instance.set_value(option_choice, value)

            print(self.colorization('blue',
                                    f"{value_instance.get_name()}: {json.dumps(value_instance.get_data(), indent=4)})"))

    def delete_keys(self, filepath, section_path, entity_name):
        while True:
            keys = self.MetadataManager.list(section_path, filepath)
            if not keys:
                print(self.colorization("yellow", f"No {section_path[0]} available to delete"))
                return

            keys.append('Exit')

            field_choice = self.TerminalManager.get_choice_with_autocomplete(
                "Start typing a field to delete or 'Exit' to finish: ",
                keys,
                validator=self.Validators.ChoiceValidator(keys)
            )

            if field_choice == 'Exit':
                break

            confirm = self.TerminalManager.get_choice_with_autocomplete(
                f"Are you sure you want to delete '{field_choice}'? ",
                self.YES_NO,
                validator=self.Validators.ChoiceValidator(self.YES_NO)
            )

            if confirm == "Yes":
                self.MetadataManager.delete(section_path, field_choice, filepath)

                language_files = self.FileManager.get_file_names(self.FileManager.get_i18n_path(), extension='folder')
                for language in language_files:
                    translation_filepath = self.FileManager.ensure_file_exists(
                        self.FileManager.get_i18n_path(entity_name, language))
                    self.MetadataManager.delete(section_path, field_choice, translation_filepath)

                    self.MetadataManager.delete(['tooltips'], field_choice, translation_filepath)
                print(self.colorization('yellow', f"'{field_choice}' was deleted"))
            else:
                print(self.colorization('yellow', f"'{field_choice}' was not deleted"))

    def translate_values(self, entity_name):

        languages = self.languages.copy()

        language = self.TerminalManager.get_choice_with_autocomplete(
            "Select the language to translate to: ",
            languages,
            validator=self.Validators.ChoiceValidator(languages)
        )

        while True:
            opposite_language = self.TerminalManager.get_choice_with_autocomplete(
                "Select the language to translate from: ",
                languages,
                validator=self.Validators.ChoiceValidator(languages)
            )
            if language != opposite_language:
                break
            else:
                print(self.colorization('red', "You can't translate to the same language."))

        filepath = self.FileManager.ensure_file_exists(self.FileManager.get_i18n_path(entity_name, opposite_language))

        translation_filepath = self.FileManager.ensure_file_exists(
            self.FileManager.get_i18n_path(entity_name, language))

        print(self.colorization('green', f"Translating '{entity_name}' from {opposite_language} to {language}"))

        data = self.MetadataManager.get(filepath)
        if not data:
            print("No data available to translate.")
            return

        self.translate_section(data, [], translation_filepath)

    def translate_section(self, section_data, section_path, translation_filepath):
        if isinstance(section_data, dict):
            items = list(section_data.keys())
            items.append('Exit')

            while True:
                item_choice = self.TerminalManager.get_choice_with_autocomplete(
                    f"Start typing a field to translate or 'Exit' to finish: ",
                    items,
                    validator=self.Validators.ChoiceValidator(items)
                )

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
