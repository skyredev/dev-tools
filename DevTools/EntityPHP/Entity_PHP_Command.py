from DevTools.Base.Base_Extender import BaseProcessor


class EntityPHPCommand(BaseProcessor):
    def __init__(self, command_file=__file__):
        super().__init__(command_file=command_file, item_type='entity', template_name='BaseEntity', folder_name='Entities')
        self.set_items(self.php_entities, self.php_entities_dir)

    def run(self):
        module = self.get_module()
        entity_name = self.get_autocomplete_names(self.items, "Enter the entity name: ")
        entity_file_path = self.PathManager.get_entity_path(entity_name)

        if entity_name in [entity[1] for entity in self.items]:
            self.suggest_extension(module, entity_name, entity_file_path, self.base_process)
        else:
            self.base_process(module, entity_name, entity_file_path)

    def base_process(self, module, entity_name, entity_file_path):
        exists_locally = self.file_exists_local_folder(entity_name, self.items_dir, ".php")

        if exists_locally:
            print(self.colorization("yellow",
                                    "Entity with the same name already exists locally. You can only extend from it"))
            action = "Extend"
        else:
            action = self.TerminalManager.get_choice_with_autocomplete(
                "What would you like to do with the entity? ",
                self.ACTIONS,
                validator=self.Validators.ChoiceValidator(self.ACTIONS)
            )

        if action == "Create":
            self.create_item(module, entity_name, entity_file_path)
        elif action == "Extend":
            if exists_locally:
                self.get_extension_from_content(self.FileManager.read_file(entity_file_path),
                                                entity_name,
                                                message=True)
                new_entity_name = self.Helpers.get_new_value_name(self.items_dir,
                                                                  self.Validators.entity_validator,
                                                                  ".php",
                                                                  "entity")
                new_entity_file_path = self.PathManager.get_entity_path(new_entity_name)
                self.extend_item(module, entity_name, new_entity_file_path,
                                 extending_item_path=entity_file_path,
                                 new_item_name=new_entity_name)
            else:
                self.extend_item(module, entity_name, entity_file_path)
