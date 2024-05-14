import os

from DevTools.Base.Base_Command import BaseCommand


class ButtonCommand(BaseCommand):
    BUTTON_VIEW_TYPES = [
        "detail",
        "list",
        "edit"
    ]

    BUTTON_DETAIL_TYPES = [
        "dropdown",
        "top-right"
    ]

    BUTTON_STYLES = [
        "default",
        "success",
        "danger",
        "warning"
    ]

    MASS_ACTIONS = [
        "Frontend",
        "Backend"
    ]

    def __init__(self):
        super().__init__(command_file=__file__)

    def run(self):
        module = self.get_module()
        entity = self.get_autocomplete_names(self.metadata_entities, "Enter the entity name: ")
        view = self.TerminalManager.get_choice_with_autocomplete(
            "Start typing the view type: ",
            self.BUTTON_VIEW_TYPES,
            validator=self.Validators.ChoiceValidator(self.BUTTON_VIEW_TYPES)
        )

        if view == "detail":
            button_type = self.TerminalManager.get_choice_with_autocomplete(
                "Start typing the button type: ",
                self.BUTTON_DETAIL_TYPES,
                validator=self.Validators.ChoiceValidator(self.BUTTON_DETAIL_TYPES)
            )
        elif view == "list":
            button_type = "mass-action"
        else:
            button_type = "top-right"

        if button_type == "mass-action":
            handle_method = self.TerminalManager.get_choice_with_autocomplete(
                "Would you like to handle the mass action on the frontend or backend? ",
                self.MASS_ACTIONS,
                validator=self.Validators.ChoiceValidator(self.MASS_ACTIONS)
            )
            if handle_method == "Backend":
                self.create_backend_mass_action(module, entity)
                return

        name = self.TerminalManager.get_user_input("Enter the button name", self.Validators.button_name_validator)
        converted_name = self.TerminalManager.get_converted_name(name)

        while self.file_exists_local_folder(f"{converted_name}-handler",
                                            os.path.join(self.current_dir, f"src/client/src/handlers/{entity}"),
                                            ".js"):
            print(self.colorization("yellow",
                                    "Button with the same name already exists locally. Please type a different name."))
            name = self.TerminalManager.get_user_input("Enter the button name", self.Validators.button_name_validator)
            converted_name = self.TerminalManager.get_converted_name(name)

        label = self.TerminalManager.get_user_input("Enter the button label", default=name)

        if button_type != "mass-action" and button_type != "dropdown":
            style = self.TerminalManager.get_choice_with_autocomplete(
                "Start typing the button style: ",
                self.BUTTON_STYLES,
                validator=self.Validators.ChoiceValidator(self.BUTTON_STYLES)
            )
        else:
            style = None

        json_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Backend/" + self.get_json_template(view, button_type))),
            self.generate_template_values(
                module, entity, label, converted_name, name, view, style)
        )
        js_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Frontend/" + self.get_js_template(view, button_type))),
            self.generate_template_values(
                module, entity, label, converted_name, name, view, style)
        )

        handler_dir = self.PathManager.get_handler_path(entity, converted_name)
        metadata_dir = self.PathManager.get_client_defs_path(entity)
        merged_json = self.FileManager.merge_json_file(metadata_dir, json_populated_template)

        self.FileManager.write_file(metadata_dir, merged_json)
        self.FileManager.write_file(handler_dir, js_populated_template)

        if button_type == "mass-action":
            self.FileManager.add_translations(entity, ["massActions"], converted_name, label)

    @staticmethod
    def get_json_template(view, button_type):
        templates = {
            ('detail', 'dropdown'): 'detailActionList.json',
            ('list', 'mass-action'): 'massActionList.json'
        }
        return templates.get((view, button_type), 'detail.json')

    @staticmethod
    def get_js_template(view, button_type):
        if view == "list" and button_type == "mass-action":
            return "mass_action.js"
        return "button.js"

    def create_backend_mass_action(self, module, entity):

        name = self.TerminalManager.get_user_input("Enter the mass-action class name",
                                                   validator=self.Validators.class_name_validator)
        while self.file_exists_local_folder(name, os.path.join(self.current_dir, f"src/backend/MassAction/{entity}"),
                                            ".php"):
            print(self.colorization("yellow",
                                    "Mass-action with the same name already exists locally. Please type a different name."))
            name = self.TerminalManager.get_user_input("Enter the mass-action class name",
                                                       validator=self.Validators.class_name_validator)

        php_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Backend/massAction.php")),
            self.generate_mass_action_template_values(module, entity, name)
        )

        php_dir = self.PathManager.get_backend_mass_action_path(entity, name)
        self.FileManager.write_file(php_dir, php_populated_template)

        app_metadata_path = os.path.join(self.current_dir, "src/backend/Resources/metadata/app/massActions.json")
        self.FileManager.ensure_file_exists(app_metadata_path)

        implementation_class_name = self.get_mass_action_classname(php_populated_template, name)
        self.MetadataManager.set([name], "implementationClassName", implementation_class_name, app_metadata_path)

        self.FileManager.add_translations(entity, ["massActions"], name, name)

    @staticmethod
    def generate_mass_action_template_values(module, entity, name):
        return {
            "{ModuleNamePlaceholder}": ''.join(part.capitalize() for part in module.split('-')),
            "{EntityNamePlaceholder}": entity,
            "{ActionNamePlaceHolder}": name
        }

    def generate_template_values(self, module, entity, label, converted_name, name, view, style=None):
        return {
            "{ModuleNamePlaceholder}": module,
            "{EntityNamePlaceholder}": entity,
            "{ButtonLabelPlaceholder}": label,
            "{ButtonNamePlaceholder}": converted_name,
            "{ButtonNameNoDashPlaceholder}": self.TerminalManager.convert_to_camel_case(name),
            "{ButtonStylePlaceholder}": style,
            "{EntityNameUpperPlaceholder}": entity[0].upper() + entity[1:],
            "{FunctionNamePlaceholder}": self.TerminalManager.convert_to_camel_case(name, start_lower=False),
            "{ViewPlaceholder}": view
        }

    @staticmethod
    def get_mass_action_classname(content, controller_name):
        if "namespace" in content:
            namespace = content.split("namespace ")[1].split(";")[0]
        else:
            namespace = "NO NAMESPACE FOUND IN EXTENDING CONTROLLER"

        return f"{namespace}\\{controller_name}"
