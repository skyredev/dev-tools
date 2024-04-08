from constants import (
    BUTTON_VIEW_TYPES, BUTTON_DETAIL_TYPES, BUTTON_STYLES, HOOK_TYPES, ENTITY_TYPES
)
from validators import (
    button_name_validator, button_name_validator_error,
    entity_validator, entity_validator_error,
    empty_string_validator, empty_string_validator_error,
    hook_name_validator, hook_name_validator_error
)


class CommandHandler:
    def __init__(self, communicator, file_generator):
        self.communicator = communicator
        self.file_generator = file_generator

    def get_module(self):
        module = self.communicator.get_user_input(
            "Enter the module name", empty_string_validator, empty_string_validator_error(),
            default=self.communicator.get_module_suggestion())
        return module

    def create_button(self):
        module = self.get_module()
        entity = self.communicator.get_user_input("Enter the entity name", entity_validator, entity_validator_error())
        view = self.communicator.get_choice(
            "Select the view:\n1. Detail\n2. List\n3. Edit\nEnter the view number", BUTTON_VIEW_TYPES)

        if view == "detail":
            button_type = self.communicator.get_choice(
                "Select the button type for the detail view:\n1. Dropdown\n2. Top-right corner\nEnter the button type number",
                BUTTON_DETAIL_TYPES)
        elif view == "list":
            button_type = "mass-action"
        else:
            button_type = "top-right"

        name = self.communicator.get_user_input("Enter the button name", button_name_validator,
                                                button_name_validator_error())
        converted_name = self.communicator.get_converted_name(name)
        label = self.communicator.get_user_input("Enter the button label", default=name)
        style = self.communicator.get_choice(
            "Select the button style:\n1. Default\n2. Success\n3. Danger\n4. Warning\nEnter the style number",
            BUTTON_STYLES)

        self.file_generator.create_button_files(module, entity, view, button_type, label, converted_name, style)

    def create_hook(self):
        module = self.get_module()
        entity = self.communicator.get_user_input("Enter the entity name", entity_validator, entity_validator_error())
        hook_type = self.communicator.get_choice(
            "Select the hook type:\n1. beforeSave\n2. afterSave\n3. beforeRemove\n4. afterRemove\n5. afterRelate\n6. afterUnrelate\n7. afterMassRelate\nEnter the hook type number",
            HOOK_TYPES)
        hook_name = self.communicator.get_user_input("Enter the hook name", hook_name_validator,
                                                     hook_name_validator_error())

        self.file_generator.create_hook_file(module, hook_type, hook_name, entity)

    def create_entity(self):
        module = self.get_module()
        entity_type = self.communicator.get_choice(
            "Select the entity type:\n1. Base\n2. Base Plus\n3. Event\n4. Person\n5. Company\nEnter the entity type number",
            ENTITY_TYPES)
        entity_name = self.communicator.get_user_input("Enter the entity name", entity_validator,
                                                       entity_validator_error())

        self.file_generator.create_entity_files(module, entity_name, entity_type)
