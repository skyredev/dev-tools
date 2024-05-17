import os

from DevTools.Base.Base_Command import BaseCommand


class ActionCommand(BaseCommand):

    def __init__(self):
        super().__init__(command_file=__file__)

    ACTION_METHODS = [
        "post",
        "get",
        "put",
        "delete",
    ]

    def run(self):
        module = self.get_module()
        entity = self.get_autocomplete_names(self.metadata_entities, "Enter the entity name: ")

        action_name = self.TerminalManager.get_user_input("Enter the action name", self.Validators.class_name_validator)
        while self.file_exists_local_folder(action_name, os.path.join(self.current_dir, f"src/backend/Api/{entity}"),
                                            ".php"):
            print(self.colorization("yellow",
                                    "Action with the same name already exists locally. Please type a different name."))
            action_name = self.TerminalManager.get_user_input("Enter the action name",
                                                              self.Validators.class_name_validator)

        method = self.TerminalManager.get_choice_with_autocomplete(
            "Select the method for the action: ",
            self.ACTION_METHODS,
            validator=self.Validators.ChoiceValidator(self.ACTION_METHODS)
        )

        route = self.TerminalManager.get_user_input("Enter the route for the action",
                                                    self.Validators.empty_string_validator)

        noAuth = self.TerminalManager.get_yes_no("Does this action require authentication?")

        populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(os.path.join(self.script_path, "Templates/" + "BaseAction" + ".php")),
            self.generate_template_values(
                module, entity, action_name)
        )

        php_dir = self.PathManager.get_api_action_path(entity, action_name)

        self.FileManager.write_file(php_dir, populated_template)

        actionClassName = self.get_action_classname(populated_template, action_name)

        self.append_route(method, route, actionClassName, noAuth)

        print(self.colorization("green", f"Route added successfully: {method.upper()} {route} -> {actionClassName}"))

    @staticmethod
    def generate_template_values(module, entity, action_name):
        return {
            "{ModuleNamePlaceholder}": ''.join(part.capitalize() for part in module.split('-')),
            "{EntityNamePlaceholder}": entity,
            "{ActionNamePlaceholder}": action_name
        }

    @staticmethod
    def get_action_classname(content, controller_name):
        if "namespace" in content:
            namespace = content.split("namespace ")[1].split(";")[0]
        else:
            namespace = "NO NAMESPACE FOUND IN EXTENDING CONTROLLER"

        return f"{namespace}\\{controller_name}"

    def append_route(self, method, route_string, actionClassName, noAuth):
        route = {
            "route": route_string,
            "method": method,
            "actionClassName": actionClassName
        }

        if noAuth:
            route["noAuth"] = True

        path = self.FileManager.ensure_file_exists(self.routes_path, json_list=True)
        self.MetadataManager.append_array([], route, path)
