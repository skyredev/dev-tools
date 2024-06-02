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
        entity_name = self.get_autocomplete_names(self.metadata_entities, "Enter the entity name: ")

        entity_fields_list = []

        for entity_cache in self.metadata_entities:
            if entity_cache[1] == entity_name and 'custom.Espo.Custom' not in entity_cache[0]:
                fields = self.MetadataManager.list(["fields"], entity_cache[0])
                for field in fields:
                    field_type = self.MetadataManager.get(entity_cache[0], ["fields", field, "type"])
                    if field_type:
                        entity_fields_list.append((field, field_type))
        if os.path.exists(self.PathManager.get_entity_defs_path(entity_name)):
            fields = self.MetadataManager.list(["fields"], self.PathManager.get_entity_defs_path(entity_name))
            for field in fields:
                field_type = self.MetadataManager.get(self.PathManager.get_entity_defs_path(entity_name),
                                                      ["fields", field, "type"])
                if field_type:
                    entity_fields_list.append((field, field_type))

        entity_fields_list = list(set(entity_fields_list))

        if not entity_fields_list:
            print(self.colorization("red", "No fields found for this entity."))
            return

        field = self.TerminalManager.get_choice_with_autocomplete(
            "Enter the field name: ",
            [field[0] for field in entity_fields_list],
            validator=self.Validators.ChoiceValidator([field[0] for field in entity_fields_list])
        )

        field_type = entity_fields_list[[field[0] for field in entity_fields_list].index(field)][1]

        if not field_type:
            print(self.colorization("red", "No type found for this field."))
            return

        local_entity_path = self.FileManager.ensure_file_exists(self.PathManager.get_entity_defs_path(entity_name))

        local_entity_has_view = self.MetadataManager.get(local_entity_path, ["fields", field, "view"])

        if local_entity_has_view:
            print(self.colorization("yellow", f"This field already has a view ({local_entity_has_view} in src/entityDefs/{entity_name}.json)"))
        # if local_entity_has_view:
        #     print(self.colorization("yellow",
        #                             f"This field already has a view ({local_entity_has_view} - in local entityDefs)"))
        #     actions = ["Overwrite Field View (Create new view)", "Choose a different field", "Cancel"]
        #     action = self.TerminalManager.get_choice_with_autocomplete(
        #         "What do you want to do? ",
        #         actions,
        #         validator=self.Validators.ChoiceValidator(actions)
        #     )
        #     if action == "Cancel":
        #         return
        #     elif action == "Choose a different field":
        #         continue
        #     elif action == "Overwrite Field View (Create new view)":
        #         delete_old = self.TerminalManager.get_yes_no("Do you want to delete the old view?")
        #         if delete_old:
        #             os.remove(os.path.join(self.current_dir, f"src/client/src/views/{entity_name}/fields",
        #                                    local_entity_has_view.split("/")[-1] + ".js"))

        file_name = self.TerminalManager.get_converted_name(field_type, "Field View", noFunctionMessage=True)

        while self.file_exists_local_folder(file_name, os.path.join(self.current_dir,
                                                                    f"src/client/src/views/{entity_name}/fields"),
                                            ".js"):
            print(self.colorization("yellow",
                                    "Field view already exists locally. Please type a different name."))
            file_name = self.TerminalManager.get_converted_name(
                self.TerminalManager.get_user_input("Enter the field type",
                                                    validator=self.Validators.view_name_validator), "Field View",
                noFunctionMessage=True)

        js_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Frontend/" + "fieldView.js")),
            self.generate_template_values(
                module, entity_name, file_name)
        )

        view_path = self.PathManager.get_view_path(entity_name, file_name, "fields")

        view = f"{module}:views/fields/{entity_name}/{file_name}"

        self.FileManager.write_file(view_path, js_populated_template)

        self.MetadataManager.set(["fields", field], "view", view, local_entity_path)

    @staticmethod
    def generate_template_values(module, entity, file_name):
        return {
            "{ModuleNamePlaceholder}": module,
            "{EntityNamePlaceholder}": entity,
            "{FieldTypePlaceholder}": file_name,
        }
