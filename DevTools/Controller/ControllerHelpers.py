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
                cleaner_paths_dict[controller[0]] = controller[0].replace(self.cache_path, "").replace("\\", "/").replace(
                    "/Controllers/", "")
            else:
                cleaner_paths_dict[controller[0]] = controller[0].replace(self.current_dir, "").replace("\\", "/").lstrip(
                    "/")
        return cleaner_paths_dict

    def get_new_controller_name(self):
        new_controller_name = self.TerminalManager.get_user_input(
            "Enter the NEW controller name",
            validator=self.Validators.controller_validator
        )
        while self.controller_name_exists_locally(new_controller_name):
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

    def controller_name_exists_locally(self, controller_name):
        if controller_name + ".php" in os.listdir(self.controllers_dir):
            return True
        return False

    def get_extension_from_content(self, content, controller_name, message=False):
        if "namespace" in content:
            namespace = content.split("namespace ")[1].split(";")[0]
        else:
            namespace = "NO NAMESPACE FOUND IN EXTENDING CONTROLLER"
        if message:
            print(self.colorization("green", f"New controller will extend from {namespace}\\{controller_name}"))
        return f"extends {namespace}\\{controller_name}"

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
