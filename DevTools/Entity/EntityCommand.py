import os

from DevTools.Base.BaseCommand import BaseCommand
from DevTools.Entity.CreateEntity import CreateEntity
from DevTools.Entity.ModifyEntity import ModifyEntity


class EntityCommand(BaseCommand):
    ENTITY_TYPES = [
        "Base",
        "BasePlus",
        "Event",
        "Person",
        "Company"
    ]

    ACTION = [
        "Create",
        "Modify"
    ]

    def __init__(self):
        super().__init__(commandFile=__file__)
        self.CreateEntity = CreateEntity(ENTITY_TYPES=self.ENTITY_TYPES)
        self.ModifyEntity = ModifyEntity()

    def run(self):
        module = self.get_module()
        entity_name = self.get_entity_name()
        entity_file_path = self.get_entity_file_path(entity_name)

        if os.path.exists(entity_file_path):
            self.ModifyEntity.modify(entity_file_path, entity_name)
        else:
            action = self.TerminalManager.get_choice_with_autocomplete(
                "What would you like to do with the entity? ",
                self.ACTION,
                validator=self.Validators.ChoiceValidator(self.ACTION)
            )
            if action == "Create":
                entity_type = self.TerminalManager.get_choice_with_autocomplete(
                    "Start typing the entity type: ", self.ENTITY_TYPES, validator=self.Validators.ChoiceValidator(self.ENTITY_TYPES)
                )

                self.CreateEntity.create(module, entity_name, entity_type)
            else:
                self.FileManager.ensure_json_exists(entity_file_path)
                self.ModifyEntity.modify(entity_file_path, entity_name)

    def get_entity_file_path(self, entity_name):
        return os.path.join(self.script_dir, f"../../src/backend/Resources/metadata/entityDefs/{entity_name}.json")
