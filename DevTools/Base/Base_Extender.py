import os

from DevTools.Base.Base_Command import BaseCommand
from DevTools.Utils.HelperFunctions import Helpers


class BaseProcessor(BaseCommand):
    YES_NO = ["Yes", "No"]
    ACTIONS = ["Create", "Extend"]

    def __init__(self, command_file, item_type, template_name, folder_name):
        super().__init__(command_file=command_file)
        self.item_type = item_type
        self.template_name = template_name
        self.folder_name = folder_name
        self.items_dir = None
        self.items = None
        self.Helpers = Helpers(values=self.items)

    def set_items(self, items, items_dir):
        self.items = items
        self.items_dir = items_dir
        self.Helpers = Helpers(values=self.items)

    def create_item(self, module, item_name, item_file_path, extension=""):
        item_content = self.TemplateManager.set_template_values(
            self.FileManager.read_file(os.path.join(self.script_path, f"Templates/{self.template_name}.php")),
            self.generate_template_values_extend(module, item_name, extension=extension)
        )

        self.FileManager.write_file(item_file_path, item_content)

    def extend_item(self, module, item_name, item_file_path, extending_item_path=None, new_item_name=None):
        extension = ""
        if not new_item_name:
            new_item_name = item_name
        if extending_item_path:
            extending_item_content = self.FileManager.read_file(extending_item_path)
            extension = self.get_extension_from_content(extending_item_content, item_name)
        else:
            root_dir = os.path.join(self.cache_dir, self.folder_name)
            current_dir = root_dir

            while True:
                folder_items = os.listdir(current_dir)
                if current_dir == root_dir:
                    folder_items.remove("custom.Espo.Custom") if "custom.Espo.Custom" in folder_items else None
                    folder_items.append('local')

                extending_item = self.TerminalManager.get_choice_with_autocomplete(
                    f"Choose the {self.item_type} you would like to extend: ",
                    folder_items,
                    validator=self.Validators.ChoiceValidator(folder_items)
                )
                if extending_item == 'local':
                    current_dir = self.items_dir
                    continue

                if os.path.isdir(os.path.join(current_dir, extending_item)):
                    current_dir = os.path.join(current_dir, extending_item)
                    continue
                else:
                    extending_item_path = os.path.join(current_dir, extending_item)
                    extending_item_content = self.FileManager.read_file(extending_item_path)
                    extension = self.get_extension_from_content(extending_item_content,
                                                                extending_item.replace(".php", ""),
                                                                message=True)
                    break

        self.create_item(module, new_item_name, item_file_path, extension=extension)

    def suggest_extension(self, module, item_name, item_file_path, base_process):
        existing_items_list = self.Helpers.get_cache_path(item_name)

        cleaner_paths = self.Helpers.set_cleaner_paths_dict(existing_items_list, self.folder_name)

        unextendable_items = []
        for existing_items in existing_items_list:
            if "custom.Espo.Custom" in existing_items[0]:
                unextendable_items.append(existing_items[0])

        if len(unextendable_items) == len(existing_items_list):
            print(self.colorization("yellow",
                                    f"Found existing {self.item_type}(s) with the same name, but they are all custom {self.item_type}s (custom.Espo.Custom) and cannot be extended."))
            base_process(module, item_name, item_file_path)
            return

        extend = self.TerminalManager.get_choice_with_autocomplete(
            f"Existing {self.item_type}(s) with the same name found. Would you like to extend from one of them? ",
            self.YES_NO,
            validator=self.Validators.ChoiceValidator(self.YES_NO)
        )

        if extend == "Yes":
            while True:
                extending_item = self.TerminalManager.get_choice_with_autocomplete(
                    f"Choose the {self.item_type} you would like to extend: ",
                    cleaner_paths.values(),
                    validator=self.Validators.ChoiceValidator(cleaner_paths.values())
                )
                extending_item_path = self.Helpers.get_real_value_path(cleaner_paths,
                                                                       extending_item)

                if extending_item_path in unextendable_items:
                    print(
                        self.colorization("yellow",
                                          f"Custom {self.item_type} (custom.Espo.Custom) cannot be extended."))
                    continue
                else:
                    break

            self.get_extension_from_content(self.FileManager.read_file(extending_item_path),
                                            item_name,
                                            message=True)
            new_item_name = self.Helpers.get_new_value_name(self.items_dir,
                                                            self.Validators.new_name_validator,
                                                            ".php",
                                                            self.item_type)
            new_item_file_path = self.PathManager.get_item_path(self.folder_name, new_item_name)

            self.extend_item(module, item_name, new_item_file_path,
                             extending_item_path=extending_item_path,
                             new_item_name=new_item_name)

        else:
            base_process(module, item_name, item_file_path)

    @staticmethod
    def generate_template_values_extend(module, name, extension=""):
        return {
            "{ModuleNamePlaceholder}": ''.join(part.capitalize() for part in module.split('-')),
            "{ClassNamePlaceholder}": name,
            "{ExtensionPlaceholder}": extension,
        }

