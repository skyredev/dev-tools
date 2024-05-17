import os
from DevTools.Base.Base_Command import BaseCommand


class SetupHandlerCommand(BaseCommand):
    VIEW_TYPES = [
        "list",
        "detail",
        "edit",
        "record/list",
        "record/search",
        "record/detail",
        "record/edit",
        "record/kanban",
        "login"
    ]

    def __init__(self):
        super().__init__(command_file=__file__)

    def run(self):
        module = self.get_module()

        # Ask if the user wants to define the handler globally or for a specific entity
        entity = self.get_autocomplete_names(self.metadata_entities, "Enter the entity name: ")

        is_global = self.TerminalManager.get_yes_no("Do you want to define the handler in Global.json?")

        view = self.TerminalManager.get_choice_with_autocomplete(
            "Start typing the view type: ",
            self.VIEW_TYPES,
            validator=self.Validators.ChoiceValidator(self.VIEW_TYPES)
        )

        name = self.TerminalManager.get_user_input("Enter the setup handler name",
                                                   self.Validators.handler_name_validator)
        converted_name = self.TerminalManager.get_converted_name(name, noFunctionMessage=True)

        while self.file_exists_local_folder(f"{converted_name}-handler",
                                            os.path.join(self.current_dir, f"src/client/src/handlers/{entity}"),
                                            ".js"):
            print(self.colorization("yellow",
                                    "Handler with the same name (after conversion) already exists locally. Please type a different name."))
            name = self.TerminalManager.get_user_input("Enter the setup handler name",
                                                       self.Validators.handler_name_validator)
            converted_name = self.TerminalManager.get_converted_name(name, noFunctionMessage=True)

        json_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Backend/" + "viewSetupHandler.json")),
            self.generate_template_values(
                module, entity, view, converted_name)
        )
        js_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Frontend/" + "viewSetupHandler.js")),
            self.generate_template_values(
                module, entity, view, converted_name)
        )

        handler_dir = self.PathManager.get_handler_path(entity, converted_name)
        metadata_dir = self.PathManager.get_client_defs_path(entity if not is_global else "Global")
        merged_json = self.FileManager.merge_json_file(metadata_dir, json_populated_template)

        self.FileManager.write_file(metadata_dir, merged_json)
        self.FileManager.write_file(handler_dir, js_populated_template)

    @staticmethod
    def generate_template_values(module, entity, view, converted_name):
        return {
            "{ModuleNamePlaceholder}": module,
            "{EntityNamePlaceholder}": entity,
            "{ViewTypePlaceholder}": view,
            "{HandlerNamePlaceholder}": converted_name,
        }
