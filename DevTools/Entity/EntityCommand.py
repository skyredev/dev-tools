import os

from DevTools.Base.BaseCommand import BaseCommand
from DevTools.Entity.CreateEntity import CreateEntity
from DevTools.Entity.ModifyEntity import ModifyEntity


class EntityCommand(BaseCommand):
    ENTITY_TYPES = {
        "1": "Base",
        "2": "BasePlus",
        "3": "Event",
        "4": "Person",
        "5": "Company"
    }

    ACTION = {
        "1": "Create",
        "2": "Modify"
    }

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
            action = self.TerminalManager.get_choice(
                self.TerminalManager.sent_choice_to_user("Would you like to create or modify the existing entity?",
                                                         self.ACTION),
                self.ACTION
            )
            if action == "Create":
                entity_type = self.TerminalManager.get_choice(
                    self.TerminalManager.sent_choice_to_user("Select the Entity type:", self.ENTITY_TYPES),
                    self.ENTITY_TYPES
                )

                self.CreateEntity.create(module, entity_name, entity_type)
            else:
                self.FileManager.ensure_json_exists(entity_file_path)
                self.ModifyEntity.modify(entity_file_path, entity_name)

    def get_entity_file_path(self, entity_name):
        return os.path.join(self.script_dir, f"../../src/backend/Resources/metadata/entityDefs/{entity_name}.json")
