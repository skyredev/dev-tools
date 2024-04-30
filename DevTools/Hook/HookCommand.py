import os

from DevTools.Base.BaseCommand import BaseCommand


class HookCommand(BaseCommand):
    HOOK_TYPES = [
        "beforeSave",
        "afterSave",
        "beforeRemove",
        "afterRemove",
        "afterRelate",
        "afterUnrelate",
        "afterMassRelate"
    ]

    def __init__(self):
        super().__init__(command_file=__file__)

    def run(self):
        module = self.get_module()
        entity = self.get_entity_name()

        hook_type = self.TerminalManager.get_choice_with_autocomplete(
            "Start typing the hook type: ",
            self.HOOK_TYPES,
            validator=self.Validators.ChoiceValidator(self.HOOK_TYPES)
        )

        hook_name = self.TerminalManager.get_user_input("Enter the hook name", self.Validators.hook_name_validator)

        populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(os.path.join(self.script_path, "Templates/BaseHooks/" + hook_type + ".php")),
            self.generate_template_values(
                module, entity, hook_type, hook_name)
        )

        php_dir = os.path.join(self.current_dir, f"src/backend/Hooks/{entity}/{hook_name}.php")

        self.FileManager.write_file(php_dir, populated_template)

    @staticmethod
    def generate_template_values(module, entity, hook_type, hook_name):
        return {
            "{ModuleNamePlaceholder}": ''.join(part.capitalize() for part in module.split('-')),
            "{EntityNamePlaceholder}": entity,
            "{HookNamePlaceHolder}": hook_name,
            "{HookTypePlaceHolder}": hook_type
        }
