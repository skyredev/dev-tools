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
            view = self.get_valid_view_path()
            extend_path_parts = view.split("/")
            record_view = "record" in extend_path_parts
            view_path = "/".join(extend_path_parts[1:])
            view_type = extend_path_parts[-1]
        else:
            view_type = self.get_view_type()
            record_view = self.TerminalManager.get_yes_no("Is this a record view?")
            view_path = f"record/{view_type}" if record_view else view_type

        name = self.get_unique_view_name(entity)

        tpl_template = self.FileManager.read_file(
            os.path.join(self.script_path, "Templates/Frontend/" + "customView.tpl"))

        template, middleView, sideView, bottomView = self.get_view_options(view_type)

        json_template = "customRecordView.json" if record_view else "customView.json"
        template_values = self.generate_template_values(
            module, entity, view_path, view_type, name, template, middleView, sideView, bottomView)

        json_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Backend/" + json_template)), template_values)

        js_populated_template = self.TemplateManager.set_template_values(
            self.FileManager.read_file(
                os.path.join(self.script_path, "Templates/Frontend/" + "customView.js")), template_values)

        view_dir = self.PathManager.get_view_path(entity, name, view_path)
        metadata_dir = self.PathManager.get_client_defs_path(entity)
        merged_json = self.FileManager.merge_json_file(metadata_dir, json_populated_template)

        self.FileManager.write_file(metadata_dir, merged_json)
        self.FileManager.write_file(view_dir, js_populated_template)
        self.write_optional_templates(entity, view_path, tpl_template, template, middleView, sideView, bottomView)

    def get_valid_view_path(self):
        view = self.TerminalManager.get_user_input(
            "Enter the full path of the view you want to extend (Input format Hint: views/email/record/detail)")

        while not view.startswith("views/"):
            print(self.colorization("red", "Invalid view path. Please make sure the path starts with 'views/'"))
            view = self.TerminalManager.get_user_input(
                "Enter the full path of the view you want to extend (Input format Hint: views/email/record/detail)")
        return view

    def get_view_type(self):
        return self.TerminalManager.get_choice_with_autocomplete(
            "Start typing the view type: ",
            self.VIEW_TYPES,
            validator=self.Validators.ChoiceValidator(self.VIEW_TYPES)
        )

    def get_unique_view_name(self, entity):
        name = self.TerminalManager.get_user_input("Enter the view name", self.Validators.view_name_validator)
        converted_name = self.TerminalManager.get_converted_name(name, "View", noFunctionMessage=True)

        while self.file_exists_local_folder(f"{converted_name}",
                                            os.path.join(self.current_dir, f"src/client/src/views/{entity}"), ".js"):
            print(self.colorization("yellow",
                                    "View with the same name (after conversion) already exists locally. Please type a different name."))
            name = self.TerminalManager.get_user_input("Enter the view name", self.Validators.view_name_validator)
            converted_name = self.TerminalManager.get_converted_name(name, "View", noFunctionMessage=True)

        return converted_name

    def get_view_options(self, view_type):
        template = self.TerminalManager.get_yes_no("Do you want to create a template file for this view?")
        if view_type != "list":
            middleView = self.TerminalManager.get_yes_no("Do you want to create a middle view for this view?")
            sideView = self.TerminalManager.get_yes_no("Do you want to create a side view for this view?")
            bottomView = self.TerminalManager.get_yes_no("Do you want to create a bottom view for this view?")
        else:
            middleView = False
            sideView = False
            bottomView = False

        return template, middleView, sideView, bottomView

    def write_optional_templates(self, entity, view_path, tpl_template, template, middleView, sideView, bottomView):
        if template:
            self.FileManager.write_file(self.PathManager.get_tpl_path(entity, view_path, 'detail'), tpl_template)
        if middleView:
            self.FileManager.write_file(self.PathManager.get_tpl_path(entity, view_path, 'detail-middle'), tpl_template)
        if sideView:
            self.FileManager.write_file(self.PathManager.get_tpl_path(entity, view_path, 'detail-side'), tpl_template)
        if bottomView:
            self.FileManager.write_file(self.PathManager.get_tpl_path(entity, view_path, 'detail-bottom'), tpl_template)

    @staticmethod
    def generate_template_values(module, entity, view_path, view_type, converted_name, template, middleView, sideView,
                                 bottomView):
        return {
            "{ModuleNamePlaceholder}": module,
            "{EntityNamePlaceholder}": entity,
            "{ViewTypePlaceholder}": view_type,
            "{ViewPathPlaceholder}": view_path,
            "{ViewNamePlaceholder}": converted_name,
            "{TemplatePlaceholder}": f"template: '{module}:{entity}/{view_path}/detail'," if template else "",
            "{MiddleViewPlaceholder}": f"middleView: '{module}:{entity}/{view_path}/detail-middle'," if middleView else "",
            "{SideViewPlaceholder}": f"sideView: '{module}:{entity}/{view_path}/detail-side'," if sideView else "",
            "{BottomViewPlaceholder}": f"bottomView: '{module}:{entity}/{view_path}/detail-bottom'," if bottomView else ""
        }
