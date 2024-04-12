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

    def run(self):
        module = self.get_module()
        entity = self.get_entity_name()

        hook_type = self.TerminalManager.get_choice(
            self.TerminalManager.sent_choice_to_user("Select the hook type:", self.HOOK_TYPES),
            self.HOOK_TYPES)

        hook_name = self.TerminalManager.get_user_input("Enter the hook name", hook_name_validator,
                                                        hook_name_validator_error())

        self.FileManager.create_hook_file(module, hook_type, hook_name, entity)
