import os

from DevTools.Base.Base_Extender import BaseProcessor


class ControllerCommand(BaseProcessor):
    ACTIONS_METHODS = ["post", "get", "put", "delete", "Custom Route", "Exit"]

    def __init__(self, command_file=__file__):
        super().__init__(command_file=command_file, item_type='controller', template_name='BaseController',
                         folder_name='Controllers')
        self.set_items(self.controllers, self.controllers_dir)

    def run(self):
        module = self.get_module()
        controller_name = self.get_autocomplete_names(self.items, "Enter the controller name: ",
                                                      validator=self.Validators.controller_validator)
        controller_file_path = self.PathManager.get_controller_path(controller_name)

        if controller_name in [controller[1] for controller in self.items]:
            self.suggest_extension(module, controller_name, controller_file_path, self.base_process)
        else:
            self.base_process(module, controller_name, controller_file_path)

    def base_process(self, module, controller_name, controller_file_path):
        exists_locally = self.file_exists_local_folder(controller_name, self.items_dir, ".php")

        if exists_locally:
            print(self.colorization("yellow",
                                    "Controller with the same name already exists locally. You can only extend from it or add actions to it"))
            adjusted_action = ["Extend", "Add Actions"]
        else:
            adjusted_action = ["Create", "Extend"]

        action = self.TerminalManager.get_choice_with_autocomplete(
            "What would you like to do with the controller? ",
            adjusted_action,
            validator=self.Validators.ChoiceValidator(adjusted_action)
        )

        if action == "Create":
            self.create_item(module, controller_name, controller_file_path)
        elif action == "Extend":
            if exists_locally:
                self.get_extension_from_content(self.FileManager.read_file(controller_file_path),
                                                controller_name,
                                                message=True)
                new_controller_name = self.Helpers.get_new_value_name(self.items_dir,
                                                                      self.Validators.controller_validator,
                                                                      ".php",
                                                                      "controller")
                new_controller_file_path = self.PathManager.get_controller_path(new_controller_name)
                self.extend_item(module, controller_name, new_controller_file_path,
                                 extending_item_path=controller_file_path,
                                 new_item_name=new_controller_name)
            else:
                self.extend_item(module, controller_name, controller_file_path)
        elif action == "Add Actions":
            self.add_actions(controller_file_path,
                             self.FileManager.read_file(controller_file_path))

    def create_item(self, module, item_name, item_file_path, extension=""):
        item_content = self.TemplateManager.set_template_values(
            self.FileManager.read_file(os.path.join(self.script_path, "Templates/" + "BaseController" + ".php")),
            self.generate_template_values_extend(module, item_name, extension=extension)
        )

        self.FileManager.write_file(item_file_path, item_content)

        add_actions = self.TerminalManager.get_choice_with_autocomplete(
            "Would you like to add actions to the controller? ",
            self.YES_NO,
            validator=self.Validators.ChoiceValidator(self.YES_NO)
        )

        if add_actions == "Yes":
            self.add_actions(item_file_path, item_content)

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
                self.generate_template_values_action(method, action)
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

                noAuth = noAuth == "Yes"
                controller_name = controller_file_path.split("/")[-1].replace(".php", "")

                self.append_route(method, route, controller_name, action, noAuth)

                print(self.colorization("green",
                                        f"Route added successfully: {method.upper()} {route} -> {controller_name}.php -> {method}Action{action}"))

                custom_route = False
                methods = self.ACTIONS_METHODS.copy()

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

    @staticmethod
    def generate_template_values_action(method, action):
        return {
            "{MethodPlaceholder}": method,
            "{ActionPlaceholder}": action
        }
