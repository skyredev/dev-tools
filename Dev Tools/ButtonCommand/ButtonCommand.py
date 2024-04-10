import os
from ..validators import (
    button_name_validator, button_name_validator_error,
    entity_validator, entity_validator_error,
    empty_string_validator, empty_string_validator_error,
    hook_name_validator, hook_name_validator_error
)
from ..BaseCommand.BaseCommand import BaseCommand
from ..Utils.TerminalManager import TerminalManager

class ButtonCommand(BaseCommand):

    BUTTON_VIEW_TYPES = {
        "1": "detail",
        "2": "list",
        "3": "edit"
    }

    BUTTON_DETAIL_TYPES = {
        "1": "dropdown",
        "2": "top-right"
    }

    BUTTON_STYLES = {
        "1": "default",
        "2": "success",
        "3": "danger",
        "4": "warning"
    }

    def run(self):
        module = self.get_module()
        entity = self.get_entity_name()
        view = TerminalManager.get_choice(
            self.TerminalManager.sent_choice_to_user("Select the view:", self.BUTTON_VIEW_TYPES), self.BUTTON_VIEW_TYPES)

        if view == "detail":
            button_type = TerminalManager.get_choice(
                self.TerminalManager.sent_choice_to_user("Select the button type for the detail view:", self.BUTTON_DETAIL_TYPES), self.BUTTON_DETAIL_TYPES)
        elif view == "list":
            button_type = "mass-action"
        else:
            button_type = "top-right"

        name = self.TerminalManager.get_user_input("Enter the button name", button_name_validator,
                                                button_name_validator_error())
        converted_name = self.TerminalManager.get_converted_name(name)
        label = self.TerminalManager.get_user_input("Enter the button label", default=name)

        style = TerminalManager.get_choice(
            self.TerminalManager.sent_choice_to_user("Select the button style:", self.BUTTON_STYLES), self.BUTTON_STYLES)

        self.FileGenerator.create_button_files(module, entity, view, button_type, label, converted_name, style)

