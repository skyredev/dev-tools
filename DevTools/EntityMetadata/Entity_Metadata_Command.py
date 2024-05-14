import os

from DevTools.Base.Base_Command import BaseCommand
from DevTools.EntityMetadata.Create_Entity import CreateEntity
from DevTools.EntityMetadata.Modify_Entity import ModifyEntity


class EntityMetadataCommand(BaseCommand):
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
        entity_name = self.get_autocomplete_names(self.metadata_entities, "Enter the entity name: ")
        entity_file_path = self.PathManager.get_entity_defs_path(entity_name)

        if entity_name in [entity[1] for entity in self.metadata_entities]:
            self.ModifyEntity.modify(entity_file_path, entity_name, self.metadata_entities)
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
                self.FileManager.ensure_file_exists(entity_file_path)
                self.ModifyEntity.modify(entity_file_path, entity_name, self.metadata_entities)
