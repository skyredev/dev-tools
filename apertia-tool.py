from DevTools.Button.ButtonCommand import ButtonCommand
from DevTools.Hook.HookCommand import HookCommand
from DevTools.Entity.EntityCommand import EntityCommand

COMMAND_DESCRIPTIONS = {
    "button": "Creates a new button",
    "hook": "Creates a new hook",
    "entity": "Creates a new entity",
    "help": "Display this help message",
    "exit": "Exit the script"
}


def usage():
    print("Available commands:")
    for command, description in COMMAND_DESCRIPTIONS.items():
        print(f"  {command:10} {description}")


def main():
    button_Command = ButtonCommand()
    hook_Command = HookCommand()
    entity_Command = EntityCommand()

    while True:
        print("")
        usage()
        command = input("Enter a command: ")

        if command in COMMAND_DESCRIPTIONS:
            if command == "button":
                button_Command.run()
            elif command == "hook":
                hook_Command.run()
            elif command == "help":
                usage()
            elif command == "entity":
                entity_Command.run()
            elif command == "exit":
                print("Exiting the script.")
                break
        else:
            print(f"Unknown command: {command}")






if __name__ == "__main__":
    main()
