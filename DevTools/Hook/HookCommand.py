import os

from DevTools.Utils.Validators import (
    hook_name_validator, hook_name_validator_error,
)
from DevTools.Base.BaseCommand import BaseCommand


class HookCommand(BaseCommand):
    HOOK_TYPES = {
        "1": "beforeSave",
        "2": "afterSave",
        "3": "beforeRemove",
        "4": "afterRemove",
        "5": "afterRelate",
        "6": "afterUnrelate",
        "7": "afterMassRelate"
    }

    # Get the directory path of the current script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        module = self.get_module()
        entity = self.get_entity_name()

        hook_type = self.TerminalManager.get_choice(
            self.TerminalManager.sent_choice_to_user("Select the hook type:", self.HOOK_TYPES),
            self.HOOK_TYPES)

        hook_name = self.TerminalManager.get_user_input("Enter the hook name", hook_name_validator,
                                                        hook_name_validator_error())

        #self.FileManager.create_hook_file(module, hook_type, hook_name, entity)
        populatedTemplate = self.TemplateManager.set_template_values(
            self.FileManager.read_file(os.path.join(self.script_dir, "Templates/" + hook_type)), self.generateTemplateValues(
                module, entity, hook_type, hook_name)
        )

        php_dir = os.path.join(self.script_dir, f"../../src/backend/Hooks/{entity}/{hook_name}.php")

        self.FileManager.write_file(php_dir, populatedTemplate)

    def generateTemplateValues(self, module, entity, hook_type, hook_name):
        return {
                "{ModuleNamePlaceholder}": module,
                "{EntityNamePlaceholder}": entity,
                "{HookNamePlaceHolder}": hook_name,
                "{HookTypePlaceHolder}": hook_type
            }