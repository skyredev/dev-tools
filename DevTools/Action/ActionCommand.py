import os

from DevTools.Base.BaseCommand import BaseCommand


class ActionCommand(BaseCommand):

    def __init__(self):
        super().__init__(command_file=__file__)

    def run(self):
        module = self.get_module()
        entity = self.get_entity_name()

        action_name = self.TerminalManager.get_user_input("Enter the action name", self.Validators.class_name_validator)

        populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(os.path.join(self.script_path, "Templates/" + "BaseAction" + ".php")),
            self.generate_template_values(
                module, entity, action_name)
        )

        php_dir = os.path.join(self.current_dir, f"src/backend/Api/{entity}/{action_name}.php")

        self.FileManager.write_file(php_dir, populated_template)

    @staticmethod
    def generate_template_values(module, entity, action_name):
        return {
            "{ModuleNamePlaceholder}": ''.join(part.capitalize() for part in module.split('-')),
            "{EntityNamePlaceholder}": entity,
            "{ActionNamePlaceholder}": action_name
        }
