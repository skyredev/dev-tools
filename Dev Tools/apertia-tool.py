from constants import (
    COMMAND_DESCRIPTIONS
)

from ButtonCommand.ButtonCommand import ButtonCommand
from communicator import TerminalCommunicator
from filegenerators import FileGenerator
from commandhandler import CommandHandler

def usage():
    print("Available commands:")
    for command, description in COMMAND_DESCRIPTIONS.items():
        print(f"  {command:10} {description}")


def main():
    communicator = TerminalCommunicator()
    file_generator = FileGenerator(communicator)
    command_handler = CommandHandler(communicator, file_generator)

    while True:
        print("")
        usage()
        command = input("Enter a command: ")

        if command in COMMAND_DESCRIPTIONS:
            if command == "button":
                ButtonCommand().run()
            elif command == "hook":
                command_handler.create_hook()
            elif command == "entity":
                command_handler.create_entity()
            elif command == "help":
                usage()
            elif command == "exit":
                print("Exiting the script.")
                break
        else:
            print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
