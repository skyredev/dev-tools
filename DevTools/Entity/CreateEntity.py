import os
import sys

from DevTools.Base.BaseCommand import BaseCommand

# The following imports are used to dynamically import the entity templates based on the user's choice DO NOT DELETE THEME
from DevTools.Entity.Templates.Backend.Metadata.EntityDefs.Base import Base
from DevTools.Entity.Templates.Backend.Metadata.EntityDefs.BasePlus import BasePlus
from DevTools.Entity.Templates.Backend.Metadata.EntityDefs.Event import Event
from DevTools.Entity.Templates.Backend.Metadata.EntityDefs.Person import Person
from DevTools.Entity.Templates.Backend.Metadata.EntityDefs.Company import Company


class CreateEntity(BaseCommand):
    def __init__(self, ENTITY_TYPES):
        super().__init__(commandFile=__file__)
        self.ENTITY_TYPES = ENTITY_TYPES

    def create(self, module, entity_name, entity_type):
        ENTITY_DEFS_TEMPLATES = self.generate_entity_defs_templates(entity_name)
        paths = self.get_paths(entity_name)
        templates = self.get_templates(entity_type, entity_name, module, ENTITY_DEFS_TEMPLATES)
        self.write_files(paths, templates)

    def get_paths(self, entity_name):
        return {
            "scopes": os.path.join(self.script_dir, f"../../src/backend/Resources/metadata/scopes/{entity_name}.json"),
            "entityDefs": os.path.join(self.script_dir,
                                       f"../../src/backend/Resources/metadata/entityDefs/{entity_name}.json"),
            "recordDefs": os.path.join(self.script_dir,
                                       f"../../src/backend/Resources/metadata/recordDefs/{entity_name}.json"),
            "clientDefs": os.path.join(self.script_dir,
                                       f"../../src/backend/Resources/metadata/clientDefs/{entity_name}.json"),
            "i18n_cs_CZ": os.path.join(self.script_dir, f"../../src/backend/Resources/i18n/cs_CZ/{entity_name}.json"),
            "i18n_en_US": os.path.join(self.script_dir, f"../../src/backend/Resources/i18n/en_US/{entity_name}.json")
        }

    def get_templates(self, entity_type, entity_name, module, ENTITY_DEFS_TEMPLATES):
        return {
            "scopes": self.TemplateManager.set_template_values(
                self.FileManager.read_file(
                    os.path.join(self.script_dir, f"Templates/Backend/Metadata/Scopes/{entity_type}.json")),
                {"{ModuleNamePlaceholder}": module}
            ),
            "entityDefs": ENTITY_DEFS_TEMPLATES[entity_type],
            "recordDefs": self.FileManager.read_file(
                os.path.join(self.script_dir, f"Templates/Backend/Metadata/RecordDefs/{entity_type}.json")),
            "clientDefs": self.FileManager.read_file(
                os.path.join(self.script_dir, f"Templates/Backend/Metadata/ClientDefs/{entity_type}.json")),
            "i18n_cs_CZ": self.TemplateManager.set_template_values(
                self.FileManager.read_file(
                    os.path.join(self.script_dir, f"Templates/Backend/i18n/cs_CZ/{entity_type}.json")),
                {"{EntityNamePlaceholder}": entity_name}
            ),
            "i18n_en_US": self.TemplateManager.set_template_values(
                self.FileManager.read_file(
                    os.path.join(self.script_dir, f"Templates/Backend/i18n/en_US/{entity_type}.json")),
                {"{EntityNamePlaceholder}": entity_name}
            )
        }

    def write_files(self, paths, templates):
        for key, path in paths.items():
            self.FileManager.write_file(path, templates[key])

    def generate_entity_defs_templates(self, entity_name):
        return {
            entity_type: getattr(sys.modules[__name__], entity_type).create_new_entity(entity_name=entity_name)
            for entity_type in self.ENTITY_TYPES
        }
