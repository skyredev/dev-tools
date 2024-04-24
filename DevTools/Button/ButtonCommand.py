import os

from DevTools.Base.BaseCommand import BaseCommand


class ButtonCommand(BaseCommand):
    BUTTON_VIEW_TYPES = {
        "1": "detail",
        "2": "list",
        "3": "edit"
    }

    BUTTON_DETAIL_TYPES = {
        "1": "dropdown",
        "2": "top-right"
    }

    BUTTON_STYLES = {
        "1": "default",
        "2": "success",
        "3": "danger",
        "4": "warning"
    }

    def __init__(self):
        super().__init__(commandFile=__file__)

    def run(self):
        module = self.get_module()
        entity = self.get_entity_name()
        view = self.TerminalManager.get_choice(
            self.TerminalManager.sent_choice_to_user("Select the view:", self.BUTTON_VIEW_TYPES),
            self.BUTTON_VIEW_TYPES)

        if view == "detail":
            button_type = self.TerminalManager.get_choice(
                self.TerminalManager.sent_choice_to_user("Select the button type for the detail view:",
                                                         self.BUTTON_DETAIL_TYPES), self.BUTTON_DETAIL_TYPES)
        elif view == "list":
            button_type = "mass-action"
        else:
            button_type = "top-right"

        name = self.TerminalManager.get_user_input("Enter the button name", self.Validators.button_name_validator)
        converted_name = self.TerminalManager.get_converted_name(name)
        label = self.TerminalManager.get_user_input("Enter the button label", default=name)

        style = self.TerminalManager.get_choice(
            self.TerminalManager.sent_choice_to_user("Select the button style:", self.BUTTON_STYLES),
            self.BUTTON_STYLES)

        json_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_dir, "Templates/Backend/" + self.get_json_template(view, button_type))),
            self.generate_template_values(
                module, entity, label, converted_name, name, style, view)
        )
        js_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                    os.path.join(self.script_dir, "Templates/Frontend/" + self.get_js_template(view, button_type))),
            self.generate_template_values(
                module, entity, label, converted_name, name, style, view)
        )

        json_dir = os.path.join(self.script_dir, f"../../src/backend/Resources/metadata/clientDefs/{entity}.json")
        merged_json = self.FileManager.merge_json_file(json_dir, json_populated_template)
        self.FileManager.write_file(json_dir, merged_json)

        js_dir = os.path.join(self.script_dir, f"../../src/client/src/handlers/{entity}/{converted_name}-handler.js")

        if os.path.isfile(js_dir):
            print(f"Error: JS file already exists: {js_dir}")
            return

        self.FileManager.write_file(js_dir, js_populated_template)

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

    def generate_template_values(self, module, entity, label, converted_name, name, style, view):
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
