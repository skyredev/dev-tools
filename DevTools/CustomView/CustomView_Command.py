import os
from DevTools.Base.Base_Command import BaseCommand


class ViewCommand(BaseCommand):
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

        specific_view_extend = self.TerminalManager.get_yes_no("Do you want to extend a specific view?")

        if specific_view_extend:
            view = self.TerminalManager.get_user_input(
                "Enter the full path of the view you want to extend (Input format Hint: views/email/record/detail)")

            while not view.startswith("views/"):
                print(self.colorization("red",
                                        "Invalid view path. Please make sure the path starts with 'views/'"))
                view = self.TerminalManager.get_user_input(
                    "Enter the full path of the view you want to extend (Input format Hint: views/email/record/detail)")

            extend_path_parts = view.split("/")

            record_view = "record" in extend_path_parts
            view_path = "/".join(extend_path_parts[1:])
            view_type = extend_path_parts[-1]

        else:
            view_type = self.TerminalManager.get_choice_with_autocomplete(
                "Start typing the view type: ",
                self.VIEW_TYPES,
                validator=self.Validators.ChoiceValidator(self.VIEW_TYPES)
            )

            record_view = self.TerminalManager.get_yes_no("Is this a record view?")

            if record_view:
                view_path = f"record/{view_type}"
            else:
                view_path = view_type

        name = self.TerminalManager.get_user_input("Enter the view name",
                                                   self.Validators.view_name_validator)
        converted_name = self.TerminalManager.get_converted_name(name, "View")

        while self.file_exists_local_folder(f"{converted_name}",
                                            os.path.join(self.current_dir, f"src/client/src/views/{entity}"),
                                            ".js"):
            print(self.colorization("yellow",
                                    "View with the same name (after conversion) already exists locally. Please type a different name."))
            name = self.TerminalManager.get_user_input("Enter the view name",
                                                       self.Validators.view_name_validator)
            converted_name = self.TerminalManager.get_converted_name(name, "View")

        tpl_template = self.FileManager.read_file(
            os.path.join(self.script_path, "Templates/Frontend/" + "customView.tpl"))

        template = self.TerminalManager.get_yes_no("Do you want to create a template file for this view?")
        if view_type != "list":
            middleView = self.TerminalManager.get_yes_no("Do you want to create a middle view for this view?")
            sideView = self.TerminalManager.get_yes_no("Do you want to create a side view for this view?")
            bottomView = self.TerminalManager.get_yes_no("Do you want to create a bottom view for this view?")
        else:
            middleView = False
            sideView = False
            bottomView = False

        json_template = "customRecordView.json" if record_view else "customView.json"

        json_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Backend/" + json_template)),
            self.generate_template_values(
                module, entity, view_path, view_type, converted_name, template, middleView, sideView, bottomView)
        )
        js_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Frontend/" + "customView.js")),
            self.generate_template_values(
                module, entity, view_path, view_type, converted_name, template, middleView, sideView, bottomView)
        )
        tpl_dir = self.PathManager.get_tpl_path(entity, converted_name, view_path)
        view_dir = self.PathManager.get_view_path(entity, converted_name, view_path)
        metadata_dir = self.PathManager.get_client_defs_path(entity)
        merged_json = self.FileManager.merge_json_file(metadata_dir, json_populated_template)

        self.FileManager.write_file(metadata_dir, merged_json)
        self.FileManager.write_file(view_dir, js_populated_template)
        if template:
            self.FileManager.write_file(tpl_dir, tpl_template)


    @staticmethod
    def generate_template_values(module, entity, view_path, view_type, converted_name, template, middleView,
                                 sideView, bottomView):
        if template:
            template = f"template: '{module}:{entity}/{view_path}',"
        else:
            template = ""

        if middleView:
            middleView = f"middleView: '{module}:views/{entity}/{view_path}',"
        else:
            middleView = ""

        if sideView:
            sideView = f"sideView: '{module}:views/{entity}/{view_path}',"
        else:
            sideView = ""

        if bottomView:
            bottomView = f"bottomView: '{module}:views/{entity}/{view_path}',"
        else:
            bottomView = ""

        return {
            "{ModuleNamePlaceholder}": module,
            "{EntityNamePlaceholder}": entity,
            "{ViewTypePlaceholder}": view_type,
            "{ViewPathPlaceholder}": view_path,
            "{ViewNamePlaceholder}": converted_name,
            "{TemplatePlaceholder}": template,
            "{MiddleViewPlaceholder}": middleView,
            "{SideViewPlaceholder}": sideView,
            "{BottomViewPlaceholder}": bottomView
        }
