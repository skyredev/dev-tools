import os

from DevTools.Base.BaseCommand import BaseCommand


class ControllerProcesses(BaseCommand):
    def __init__(self, Helpers, base_process):
        super().__init__(command_file=__file__)
        self.base_process = base_process
        self.Helpers = Helpers

    YES_NO = [
        "Yes",
        "No"
    ]

    ACTIONS_METHODS = [
        "post",
        "get",
        "put",
        "delete",
        "Custom Route",
        "Exit"
    ]

    def create_controller(self, module, controller_name, controller_file_path, extension=""):
        controller_content = self.TemplateManager.set_template_values(
            self.FileManager.read_file(os.path.join(self.script_path, "Templates/" + "BaseController" + ".php")),
            self.Helpers.generate_template_values_controller(module, controller_name, extension=extension)
        )

        self.FileManager.write_file(controller_file_path, controller_content)

        add_actions = self.TerminalManager.get_choice_with_autocomplete(
            "Would you like to add actions to the controller? ",
            self.YES_NO,
            validator=self.Validators.ChoiceValidator(self.YES_NO)
        )

        if add_actions == "Yes":
            self.add_actions(controller_file_path, controller_content)

    def extend_controller(self, module, controller_name, controller_file_path, extending_controller_path=None,
                          new_controller_name=None):
        extension = ""
        if not new_controller_name:
            new_controller_name = controller_name
        if extending_controller_path:
            extending_controller_content = self.FileManager.read_file(extending_controller_path)
            extension = self.Helpers.get_extension_from_content(extending_controller_content, controller_name)
        else:
            root_dir = os.path.join(self.cache_path, "Controllers")
            current_dir = root_dir

            while True:
                folder_items = os.listdir(current_dir)
                if current_dir == root_dir:
                    folder_items.remove("custom.Espo.Custom")
                    folder_items.append('local')

                extending_controller = self.TerminalManager.get_choice_with_autocomplete(
                    "Choose the controller you would like to extend: ",
                    folder_items,
                    validator=self.Validators.ChoiceValidator(folder_items)
                )
                if extending_controller == 'local':
                    current_dir = self.controllers_dir  # Change directory to local controllers
                    continue

                if os.path.isdir(os.path.join(current_dir, extending_controller)):
                    current_dir = os.path.join(current_dir, extending_controller)
                    continue
                else:
                    extending_controller_path = os.path.join(current_dir, extending_controller)
                    extending_controller_content = self.FileManager.read_file(extending_controller_path)
                    extension = self.Helpers.get_extension_from_content(extending_controller_content,
                                                                        extending_controller.replace(".php", ""),
                                                                        message=True)
                    break

        self.create_controller(module, new_controller_name, controller_file_path, extension=extension)

    def add_actions(self, controller_file_path, controller_content):
        methods = self.ACTIONS_METHODS.copy()

        custom_route = False
        while True:
            method = self.TerminalManager.get_choice_with_autocomplete(
                "Choose the action you would like to add: ",
                methods,
                validator=self.Validators.ChoiceValidator(methods)
            )

            if method == "Exit":
                break
            elif method == "Custom Route":
                methods.remove("Custom Route")
                methods.remove("Exit")
                custom_route = True
                continue

            action = self.TerminalManager.get_user_input(
                "Enter the action name",
                validator=self.Validators.action_validator
            )

            action_content = self.TemplateManager.set_template_values(
                self.FileManager.read_file(
                    os.path.join(self.script_path, "Templates/Actions/" + f"{method}Action" + ".php")),
                self.Helpers.generate_template_values_action(method, action)
            )

            controller_content = controller_content.rsplit("}", 1)[0] + f"\n{action_content}" + "}"

            self.FileManager.write_file(controller_file_path, controller_content)

            if custom_route:
                route = self.TerminalManager.get_user_input("Enter the route for the action",
                                                            self.Validators.empty_string_validator)
                noAuth = self.TerminalManager.get_choice_with_autocomplete(
                    "Does this action require authentication? ",
                    self.YES_NO,
                    validator=self.Validators.ChoiceValidator(self.YES_NO)
                )

                if noAuth == "Yes":
                    noAuth = True
                else:
                    noAuth = False

                controller_name = controller_file_path.split("/")[-1].replace(".php", "")

                self.append_route(method, route, controller_name, action, noAuth)

                print(self.colorization("green", f"Route added successfully: {method.upper()} {route} -> {controller_name}.php -> {method}Action{action}"))

                custom_route = False
                methods = self.ACTIONS_METHODS.copy()

    def suggest_extension(self, module, controller_name, controller_file_path):
        existing_controllers_list = self.Helpers.get_cache_path(controller_name)

        cleaner_paths = self.Helpers.set_cleaner_paths_dict(existing_controllers_list)

        unextendable_controllers = []
        for existing_controller in existing_controllers_list:
            if "custom.Espo.Custom" in existing_controller[0]:
                unextendable_controllers.append(existing_controller[0])

        if len(unextendable_controllers) == len(existing_controllers_list):
            print(self.colorization("yellow",
                                    "Found existing controller(s) with the same name, but they are all custom controllers (custom.Espo.Custom) and cannot be extended."))
            self.base_process(module, controller_name, controller_file_path)
            return

        extend = self.TerminalManager.get_choice_with_autocomplete(
            "Existing controller(s) with the same name found. Would you like to extend from one of them? ",
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
                extending_controller_path = self.Helpers.get_real_controller_path(cleaner_paths,
                                                                                  extending_controller)

                if extending_controller_path in unextendable_controllers:
                    print(
                        self.colorization("yellow", "Custom controllers (custom.Espo.Custom) cannot be extended."))
                    continue
                else:
                    break

            self.Helpers.get_extension_from_content(self.FileManager.read_file(extending_controller_path),
                                                    controller_name,
                                                    message=True)
            new_controller_name = self.Helpers.get_new_controller_name()
            new_controller_file_path = self.FileManager.get_controller_path(new_controller_name)

            self.extend_controller(module, controller_name, new_controller_file_path,
                                   extending_controller_path=extending_controller_path,
                                   new_controller_name=new_controller_name)

        else:
            self.base_process(module, controller_name, controller_file_path)

    def append_route(self, method, route_string, controller_name, action_name, noAuth):
        route = {
            "route": route_string,
            "method": method,
            "params": {
                "controller": controller_name,
                "action": action_name
            }
        }

        if noAuth:
            route["noAuth"] = True

        params = route_string.split("/")
        for param in params:
            if ':' in param:
                route["params"][param.split(":")[1]] = param

        path = self.FileManager.ensure_file_exists(self.routes_path, json_list=True)
        self.MetadataManager.append_array([], route, path)
