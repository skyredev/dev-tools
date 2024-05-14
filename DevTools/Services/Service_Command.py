from DevTools.Base.Base_Extender import BaseProcessor


class ServiceCommand(BaseProcessor):
    def __init__(self, command_file=__file__):
        super().__init__(command_file=command_file, item_type='service', template_name='BaseService',
                         folder_name='Services')
        self.set_items(self.services, self.services_dir)

    def run(self):
        module = self.get_module()
        service_name = self.get_autocomplete_names(self.items, "Enter the service name: ", validator=self.Validators.service_validator)
        service_file_path = self.PathManager.get_service_path(service_name)

        if service_name in [service[1] for service in self.items]:
            self.suggest_extension(module, service_name, service_file_path, self.base_process)
        else:
            self.base_process(module, service_name, service_file_path)

    def base_process(self, module, service_name, service_file_path):
        exists_locally = self.file_exists_local_folder(service_name, self.items_dir, ".php")

        if exists_locally:
            print(self.colorization("yellow",
                                    "Service with the same name already exists locally. You can only extend from it"))
            action = "Extend"
        else:
            action = self.TerminalManager.get_choice_with_autocomplete(
                "What would you like to do with the service? ",
                self.ACTIONS,
                validator=self.Validators.ChoiceValidator(self.ACTIONS)
            )

        if action == "Create":
            self.create_item(module, service_name, service_file_path)
        elif action == "Extend":
            if exists_locally:
                self.get_extension_from_content(self.FileManager.read_file(service_file_path),
                                                service_name,
                                                message=True)
                new_service_name = self.Helpers.get_new_value_name(self.items_dir,
                                                                   self.Validators.service_validator,
                                                                   ".php",
                                                                   "service")
                new_service_file_path = self.PathManager.get_service_path(new_service_name)
                self.extend_item(module, service_name, new_service_file_path,
                                 extending_item_path=service_file_path,
                                 new_item_name=new_service_name)
            else:
                self.extend_item(module, service_name, service_file_path)
