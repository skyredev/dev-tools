import os

from DevTools.Base.BaseCommand import BaseCommand
from DevTools.Controller.ControllerHelpers import ControllerHelpers
from DevTools.Controller.ControllerProcesses import ControllerProcesses


class ControllerCommand(BaseCommand):

    def __init__(self):
        super().__init__(command_file=__file__)
        self.Controller_Helpers = ControllerHelpers(controllers=self.controllers)
        self.Controller_Processes = ControllerProcesses(Helpers=self.Controller_Helpers, base_process=self.base_process)

    ACTION = [
        "Create",
        "Extend",
        "Add Actions",
    ]

    def run(self):
        module = self.get_module()
        controller_name = self.get_controller_name()
        controller_file_path = self.FileManager.get_controller_path(controller_name)

        if controller_name in [controller[1] for controller in self.controllers]:
            self.Controller_Processes.suggest_extension(module, controller_name, controller_file_path)
        else:
            self.base_process(module, controller_name, controller_file_path)

    def base_process(self, module, controller_name, controller_file_path):
        adjusted_action = self.ACTION.copy()
        exists_locally = self.Controller_Helpers.controller_name_exists_locally(controller_name)

        if exists_locally:
            print(self.colorization("yellow",
                                    "Controller with the same name already exists locally. You can only extend from it or add actions to it"))
            adjusted_action.remove("Create")
        else:
            adjusted_action.remove("Add Actions")

        action = self.TerminalManager.get_choice_with_autocomplete(
            "What would you like to do with the controller? ",
            adjusted_action,
            validator=self.Validators.ChoiceValidator(adjusted_action)
        )

        if action == "Create":
            self.Controller_Processes.create_controller(module, controller_name, controller_file_path)
        elif action == "Extend":
            if exists_locally:
                self.Controller_Helpers.get_extension_from_content(self.FileManager.read_file(controller_file_path),
                                                                   controller_name,
                                                                   message=True)
                new_controller_name = self.Controller_Helpers.get_new_controller_name()
                new_controller_file_path = self.FileManager.get_controller_path(new_controller_name)
                self.Controller_Processes.extend_controller(module, controller_name, new_controller_file_path,
                                                            extending_controller_path=controller_file_path,
                                                            new_controller_name=new_controller_name)
            else:
                self.Controller_Processes.extend_controller(module, controller_name, controller_file_path)
        elif action == "Add Actions":
            self.Controller_Processes.add_actions(controller_file_path, self.FileManager.read_file(controller_file_path))
