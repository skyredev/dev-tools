import os
from DevTools.Base.Base_Command import BaseCommand


class FieldViewCommand(BaseCommand):
    VIEW_TYPES = [
        "list",
        "detail",
        "edit",
    ]

    def __init__(self):
        super().__init__(command_file=__file__)

    def run(self):
        module = self.get_module()
        entity = self.get_autocomplete_names(self.metadata_entities, "Enter the entity name: ")

        entity_fields_list = []

        for entity_cache in self.metadata_entities:
            if entity_cache[1] == entity:
                entity_fields_list += self.MetadataManager.list(["fields"], entity_cache[0])
        if os.path.exists(self.PathManager.get_entity_defs_path(entity)):
            entity_fields_list += self.MetadataManager.list(["fields"], self.PathManager.get_entity_defs_path(entity))

        entity_fields_list = list(set(entity_fields_list))

        if not entity_fields_list:
            print(self.colorization("red", "No fields found for this entity."))
            return

        field = self.TerminalManager.get_choice_with_autocomplete(
            "Enter the field name: ",
            entity_fields_list,
            validator=self.Validators.ChoiceValidator(entity_fields_list)
        )
        entity_path = self.FileManager.ensure_file_exists(self.PathManager.get_entity_defs_path(entity))

        field_type = self.MetadataManager.get(self.PathManager.get_entity_defs_path(entity), ["fields", field, "type"])

        js_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Frontend/" + "fieldView.js")),
            self.generate_template_values(
                module, entity, field_type)
        )

        file_name = field_type
        while self.file_exists_local_folder(file_name, os.path.join(self.current_dir, f"src/client/src/views/fields/{entity}"),
                                            ".js"):
            print(self.colorization("yellow",
                                    "Field view already exists locally. Please type a different name."))
            file_name = self.TerminalManager.get_user_input("Enter the field type", validator=self.Validators.view_name_validator())

        view_path = self.PathManager.get_view_path(entity, file_name, "fields")

        view = f"{module}:views/fields/{entity}/{file_name}"

        self.FileManager.write_file(view_path, js_populated_template)

        self.MetadataManager.set(["fields", field], "view", view, entity_path)

    @staticmethod
    def generate_template_values(module, entity, file_name):
        return {
            "{ModuleNamePlaceholder}": module,
            "{EntityNamePlaceholder}": entity,
            "{FieldTypePlaceholder}": file_name,
        }
