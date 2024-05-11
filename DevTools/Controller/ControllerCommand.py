import os

from DevTools.Base.BaseCommand import BaseCommand


class ControllerCommand(BaseCommand):

    def __init__(self):
        super().__init__(command_file=__file__)

    ACTION = [
        "Create",
        "Extend"
    ]

    YES_NO = [
        "Yes",
        "No"
    ]

    def run(self):
        module = self.get_module()
        controller_name = self.get_controller_name()
        controller_file_path = self.FileManager.get_controller_path(controller_name)

        if controller_name in [controller[1] for controller in self.controllers]:
            existing_controllers_list = self.get_cache_path(controller_name)

            cleaner_paths = self.set_cleaner_paths_dict(existing_controllers_list)

            unextendable_controllers = []
            for existing_controller in existing_controllers_list:
                if "custom.Espo.Custom" in existing_controller[0]:
                    unextendable_controllers.append(existing_controller[0])

            if len(unextendable_controllers) == len(existing_controllers_list):
                print(self.colorization("yellow",
                                        "Found existing controller(s) with the same name, but they are all custom controllers and cannot be extended."))
                self.base_process(module, controller_name, controller_file_path)
                return

            extend = self.TerminalManager.get_choice_with_autocomplete(
                "Existing controller(s) with the same name found. Would you like to extend any of them? ",
                self.YES_NO,
                validator=self.Validators.ChoiceValidator(self.YES_NO)
            )

            if extend == "Yes":
                while True:
                    extending_controller = self.TerminalManager.get_choice_with_autocomplete(
                        "Choose the controller you would like to extend: ",
                        cleaner_paths.values(),
                        validator=self.Validators.ChoiceValidator(cleaner_paths.values())
                    )
                    extending_controller_path = self.get_real_controller_path(cleaner_paths, extending_controller)

                    if extending_controller_path in unextendable_controllers:
                        print(
                            self.colorization("yellow", "Custom controllers (custom.Espo.Custom) cannot be extended."))
                        continue
                    else:
                        break

                self.extend_controller(module, controller_name, controller_file_path, extending_controller_path)

            else:
                self.base_process(module, controller_name, controller_file_path)

        else:
            self.base_process(module, controller_name, controller_file_path)

    def base_process(self, module, controller_name, controller_file_path):
        action = self.TerminalManager.get_choice_with_autocomplete(
            "What would you like to do with the controller? ",
            self.ACTION,
            validator=self.Validators.ChoiceValidator(self.ACTION)
        )

        if action == "Create":
            self.create_controller(module, controller_name, controller_file_path)
        else:
            self.extend_controller(module, controller_name, controller_file_path)

    def create_controller(self, module, controller_name, controller_file_path, extension=""):
        controller_content = self.TemplateManager.set_template_values(
            self.FileManager.read_file(os.path.join(self.script_path, "Templates/" + "BaseController" + ".php")),
            self.generate_template_values(module, controller_name, extension=extension)
        )

        self.FileManager.write_file(controller_file_path, controller_content)

    def get_cache_path(self, controller_name):
        existing_values = []
        for controller in self.controllers:
            if controller[1] == controller_name:
                existing_values.append(controller)
        return existing_values

    def extend_controller(self, module, controller_name, controller_file_path, extending_controller_path=None):
        extension = ""
        if extending_controller_path:
            extending_controller_content = self.FileManager.read_file(extending_controller_path)
            extension = self.get_extension_from_content(extending_controller_content, controller_name)
        else:
            current_dir = os.path.join(self.cache_path, "Controllers")

            while True:
                folder_items = os.listdir(current_dir)
                folder_items.remove("custom.Espo.Custom")

                extending_controller = self.TerminalManager.get_choice_with_autocomplete(
                    "Choose the controller you would like to extend: ",
                    folder_items,
                    validator=self.Validators.ChoiceValidator(folder_items)
                )

                if os.path.isdir(os.path.join(current_dir, extending_controller)):
                    current_dir = os.path.join(current_dir, extending_controller)
                    continue
                else:
                    extending_controller_path = os.path.join(current_dir, extending_controller)
                    extending_controller_content = self.FileManager.read_file(extending_controller_path)
                    extension = self.get_extension_from_content(extending_controller_content, extending_controller.replace(".php", ""))
                    break

        self.create_controller(module, controller_name, controller_file_path, extension=extension)

    def set_cleaner_paths_dict(self, existing_controllers_list):
        cleaner_paths_dict = {}
        for controller in existing_controllers_list:
            cleaner_paths_dict[controller[0]] = controller[0].replace(self.cache_path, "").replace("\\", "/").replace(
                "/Controllers/", "")
        return cleaner_paths_dict

    @staticmethod
    def get_real_controller_path(cleaner_paths_dict, extending_controller):
        return list(cleaner_paths_dict.keys())[list(cleaner_paths_dict.values()).index(extending_controller)]

    @staticmethod
    def get_extension_from_content(content, controller_name):
        if "namespace" in content:
            namespace = content.split("namespace ")[1].split(";")[0]
        else:
            namespace = "NO NAMESPACE FOUND IN EXTENDING CONTROLLER"
        return f"extends {namespace}\\{controller_name}"

    @staticmethod
    def generate_template_values(module, controller_name, extension=""):
        return {
            "{ModuleNamePlaceholder}": ''.join(part.capitalize() for part in module.split('-')),
            "{ControllerNamePlaceholder}": controller_name,
            "{ExtensionPlaceholder}": extension
        }
