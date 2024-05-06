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
        super().__init__(command_file=__file__)
        self.CreateEntity = CreateEntity(ENTITY_TYPES=self.ENTITY_TYPES)
        self.ModifyEntity = ModifyEntity()

    def run(self):
        module = self.get_module()
        entity_name = self.get_entity_name()
        entity_file_path = self.FileManager.get_entity_defs_path(entity_name)
        entity_cache_path = self.FileManager.get_entity_defs_cache_path(entity_name)

        if os.path.exists(entity_cache_path):
            self.ModifyEntity.modify(entity_file_path, entity_cache_path, entity_name)
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
                self.ModifyEntity.modify(entity_file_path, entity_cache_path, entity_name)
