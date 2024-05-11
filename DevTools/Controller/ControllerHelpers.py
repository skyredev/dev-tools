import os

from DevTools.Base.BaseCommand import BaseCommand


class ControllerHelpers(BaseCommand):
    def __init__(self, controllers):
        super().__init__(command_file=__file__)
        self.controllers = controllers

    def get_cache_path(self, controller_name):
        existing_values = []
        for controller in self.controllers:
            if controller[1] == controller_name:
                existing_values.append(controller)
        return existing_values

    def set_cleaner_paths_dict(self, existing_controllers_list):
        cleaner_paths_dict = {}
        for controller in existing_controllers_list:
            if self.cache_path in controller[0]:
                cleaner_paths_dict[controller[0]] = controller[0].replace(self.cache_path, "").replace("\\",
                                                                                                       "/").replace(
                    "/Controllers/", "")
            else:
                cleaner_paths_dict[controller[0]] = controller[0].replace(self.current_dir, "").replace("\\",
                                                                                                        "/").lstrip(
                    "/")
        return cleaner_paths_dict

    def get_new_controller_name(self):
        new_controller_name = self.TerminalManager.get_user_input(
            "Enter the NEW controller name",
            validator=self.Validators.controller_validator
        )
        while self.file_exists_local_folder(new_controller_name, self.controllers_dir, ".php"):
            print(self.colorization("yellow",
                                    "Controller with the same name already exists locally. Please type a different name."))
            new_controller_name = self.TerminalManager.get_user_input(
                "Enter the NEW controller name",
                validator=self.Validators.controller_validator
            )
        return new_controller_name

    @staticmethod
    def get_real_controller_path(cleaner_paths_dict, extending_controller):
        return list(cleaner_paths_dict.keys())[list(cleaner_paths_dict.values()).index(extending_controller)]

    @staticmethod
    def generate_template_values_controller(module, controller_name, extension=""):
        return {
            "{ModuleNamePlaceholder}": ''.join(part.capitalize() for part in module.split('-')),
            "{ControllerNamePlaceholder}": controller_name,
            "{ExtensionPlaceholder}": extension,
        }

    @staticmethod
    def generate_template_values_action(method, action):
        return {
            "{MethodPlaceholder}": method,
            "{ActionPlaceholder}": action
        }
