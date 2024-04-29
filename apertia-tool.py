from DevTools.Button.ButtonCommand import ButtonCommand
from DevTools.Hook.HookCommand import HookCommand
from DevTools.Entity.EntityCommand import EntityCommand
from DevTools.Base.BaseCommand import BaseCommand

COMMAND_DESCRIPTIONS = {
    "button": "Creates a new button",
    "hook": "Creates a new hook",
    "entity": "Creates a new entity",
    "help": "Displays help message",
    "exit": "Exit the script"
}


def help_message():
    print("\nNEJAKE KRATKE\nInstrukce k pouziti napr")


def usage():
    print("Available commands:")
    for command, description in COMMAND_DESCRIPTIONS.items():
        print(f"  {command:10} {description}")


def main():
    button_Command = ButtonCommand()
    hook_Command = HookCommand()
    entity_Command = EntityCommand()
    baseCommand = BaseCommand(__file__)

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
            case "button":
                button_Command.run()
            case "hook":
                hook_Command.run()
            case "entity":
                entity_Command.run()
            case "help":
                help_message()
            case "exit":
                break
            case _:
                print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
