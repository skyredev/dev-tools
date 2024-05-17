from DevTools.Base.Base_Extender import BaseProcessor


class ToolCommand(BaseProcessor):
    def __init__(self, command_file=__file__):
        super().__init__(command_file=command_file, item_type='tool', template_name='BaseTool',
                         folder_name='Tools')
        self.set_items(self.tools, self.tools_dir)

    def run(self):
        module = self.get_module()
        tool_name = self.get_autocomplete_names(self.items, "Enter the tool name: ",
                                                validator=self.Validators.tool_validator)
        tool_file_path = self.PathManager.get_tool_path(tool_name)

        if tool_name in [tool[1] for tool in self.items]:
            self.suggest_extension(module, tool_name, tool_file_path, self.base_process)
        else:
            self.base_process(module, tool_name, tool_file_path)

    def base_process(self, module, tool_name, tool_file_path):
        exists_locally = self.file_exists_local_folder(tool_name, self.items_dir, ".php")

        if exists_locally:
            print(self.colorization("yellow",
                                    "Tool with the same name already exists locally. You can only extend from it"))
            action = "Extend"
        else:
            action = self.TerminalManager.get_choice_with_autocomplete(
                "What would you like to do with the tool? ",
                self.ACTIONS,
                validator=self.Validators.ChoiceValidator(self.ACTIONS)
            )

        if action == "Create":
            self.create_item(module, tool_name, tool_file_path)
        elif action == "Extend":
            if exists_locally:
                self.get_extension_from_content(self.FileManager.read_file(tool_file_path),
                                                tool_name,
                                                message=True)
                new_tool_name = self.Helpers.get_new_value_name(self.items_dir,
                                                                self.Validators.tool_validator,
                                                                ".php",
                                                                "tool")
                new_tool_file_path = self.PathManager.get_tool_path(new_tool_name)
                self.extend_item(module, tool_name, new_tool_file_path,
                                 extending_item_path=tool_file_path,
                                 new_item_name=new_tool_name)
            else:
                self.extend_item(module, tool_name, tool_file_path)
