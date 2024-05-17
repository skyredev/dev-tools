import os
from DevTools.Base.Base_Command import BaseCommand


class DynamicHandlerCommand(BaseCommand):
    def __init__(self):
        super().__init__(command_file=__file__)

    def run(self):
        module = self.get_module()
        entity = self.get_autocomplete_names(self.metadata_entities, "Enter the entity name: ")

        name = self.TerminalManager.get_user_input("Enter the dynamic handler name",
                                                   self.Validators.handler_name_validator)

        converted_name = self.TerminalManager.get_converted_name(name, noFunctionMessage=True)

        while self.file_exists_local_folder(f"{converted_name}-handler",
                                            os.path.join(self.current_dir, f"src/client/src/handlers/{entity}"),
                                            ".js"):
            print(self.colorization("yellow",
                                    "Handler with the same name (after conversion) already exists locally. Please type a different name."))
            name = self.TerminalManager.get_user_input("Enter the dynamic handler name",
                                                       self.Validators.handler_name_validator)
            converted_name = self.TerminalManager.get_converted_name(name, noFunctionMessage=True)

        json_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Backend/" + "dynamicHandler.json")),
            self.generate_template_values(
                module, entity, converted_name)
        )
        js_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Frontend/" + "dynamicHandler.js")),
            self.generate_template_values(
                module, entity, converted_name)
        )

        handler_dir = self.PathManager.get_handler_path(entity, converted_name)
        metadata_dir = self.PathManager.get_client_defs_path(entity)
        merged_json = self.FileManager.merge_json_file(metadata_dir, json_populated_template)

        self.FileManager.write_file(metadata_dir, merged_json)
        self.FileManager.write_file(handler_dir, js_populated_template)

    @staticmethod
    def generate_template_values(module, entity, converted_name):
        return {
            "{ModuleNamePlaceholder}": module,
            "{EntityNamePlaceholder}": entity,
            "{HandlerNamePlaceholder}": converted_name,
        }
