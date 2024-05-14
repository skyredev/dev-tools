from DevTools.Button.Button_Command import ButtonCommand
from DevTools.Hook.Hook_Command import HookCommand
from DevTools.EntityMetadata.Entity_Metadata_Command import EntityMetadataCommand
from DevTools.Base.Base_Command import BaseCommand
from DevTools.Sync.Sync_Command import SyncCommand
from DevTools.Action.Action_Command import ActionCommand
from DevTools.Controller.Controller_Command import ControllerCommand
from DevTools.EntityPHP.Entity_PHP_Command import EntityPHPCommand
from DevTools.Services.Service_Command import ServiceCommand

COMMAND_DESCRIPTIONS = {
    "action": "Creates a new action",
    "button": "Creates a new button",
    "controller": "Creates a new controller",
    "entityDefs": "Creates a new metadata entity",
    "entityPHP": "Creates a new PHP entity",
    "hook": "Creates a new hook",
    "service": "Creates a new service",
    "sync": "Synchronizes with the instance",
    "help": "Displays help message",
    "exit": "Exit the script"
}


def help_message():
    print("\nNEJAKE KRATKE\nInstrukce k pouziti napr")


def usage():
    print("Available commands:")
    for command, description in COMMAND_DESCRIPTIONS.items():
        print(f"  {command:15} {description}")


def main():
    baseCommand = BaseCommand(__file__)
    button_Command = ButtonCommand()
    hook_Command = HookCommand()
    entity_metadata_Command = EntityMetadataCommand()
    entity_php_Command = EntityPHPCommand()
    service_Command = ServiceCommand()
    sync_Command = SyncCommand()
    action_Command = ActionCommand()
    controller_Command = ControllerCommand()

    while True:
        print("")
        usage()
        command = baseCommand.TerminalManager.get_choice_with_autocomplete(
            "Enter a command: ",
            list(COMMAND_DESCRIPTIONS.keys()),
            send_choices=False,
            validator=baseCommand.Validators.ChoiceValidator(list(COMMAND_DESCRIPTIONS.keys()))
        )

        match command:
            case "action":
                action_Command.run()
            case "button":
                button_Command.run()
            case "controller":
                controller_Command.run()
            case "entity":
                entity_metadata_Command.run()
            case "entityPHP":
                entity_php_Command.run()
            case "service":
                service_Command.run()
            case "hook":
                hook_Command.run()
            case "help":
                help_message()
            case "sync":
                sync_Command.run()
            case "exit":
                break
            case _:
                print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
