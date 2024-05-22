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

        entities = []

        for entity_cache in self.metadata_entities:
            if entity_cache[1] == entity_name:
                entities.append(entity_cache)

        if len(entities) > 1:
            print(self.colorization("yellow", "Multiple entities found with the same name."))
            entity_path = self.TerminalManager.get_choice_with_autocomplete(
                "Select from which entity you want to list the fields: ",
                [entity[0] for entity in entities],
                validator=self.Validators.ChoiceValidator([entity[0] for entity in entities])
            )
        else:
            entity_path = entities[0][0]

        entity_fields_list = self.MetadataManager.list(["fields"], entity_path)

        if not entity_fields_list:
            print(self.colorization("red", "No fields found for this entity."))
            return

        while True:
            field = self.TerminalManager.get_choice_with_autocomplete(
                "Enter the field name: ",
                entity_fields_list,
                validator=self.Validators.ChoiceValidator(entity_fields_list)
            )

            field_type = self.MetadataManager.get(entity_path,
                                                  ["fields", field, "type"])

            if not field_type:
                print(self.colorization("red", "No type found for this field."))
                return

            local_entity_path = self.FileManager.ensure_file_exists(self.PathManager.get_entity_defs_path(entity_name))

            local_entity_has_view = self.MetadataManager.get(local_entity_path, ["fields", field, "view"])

            if local_entity_has_view:
                print(self.colorization("yellow", f"This field already has a view ({local_entity_has_view} - in local entityDefs)"))
                actions = ["Overwrite Field View (Create new view)", "Choose a different field", "Cancel"]
                action = self.TerminalManager.get_choice_with_autocomplete(
                    "What do you want to do? ",
                    actions,
                    validator=self.Validators.ChoiceValidator(actions)
                )
                if action == "Cancel":
                    return
                elif action == "Choose a different field":
                    continue
                elif action == "Overwrite Field View (Create new view)":
                    delete_old = self.TerminalManager.get_yes_no("Do you want to delete the old view?")
                    if delete_old:
                        os.remove(os.path.join(self.current_dir, f"src/client/src/views/{entity_name}/fields", local_entity_has_view.split("/")[-1] + ".js"))

            file_name = self.TerminalManager.get_converted_name(field_type, "Field View", noFunctionMessage=True)

            while self.file_exists_local_folder(file_name, os.path.join(self.current_dir, f"src/client/src/views/{entity_name}/fields"),
                                                ".js"):
                print(self.colorization("yellow",
                                        "Field view already exists locally. Please type a different name."))
                file_name = self.TerminalManager.get_converted_name(self.TerminalManager.get_user_input("Enter the field type", validator=self.Validators.view_name_validator), "Field View", noFunctionMessage=True)

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
            break

    @staticmethod
    def generate_template_values(module, entity, file_name):
        return {
            "{ModuleNamePlaceholder}": module,
            "{EntityNamePlaceholder}": entity,
            "{FieldTypePlaceholder}": file_name,
        }
