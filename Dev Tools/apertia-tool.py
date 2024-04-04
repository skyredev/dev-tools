import os
import json
from json_templates import get_json_template
from js_templates import get_js_template


def usage():
    print("Available commands:")
    print("  button           Creates a new button")
    print("  <command2>       Description of command2")
    print("  <command3>       Description of command3")
    print("  help             Display this help message")
    print("  exit             Exit the script")


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def merge_json(existing_json, new_json):
    merged_json = existing_json.copy()
    for key, value in new_json.items():
        if key in merged_json:
            if isinstance(value, dict):
                merged_json[key] = merge_json(merged_json[key], value)
            elif isinstance(value, list):
                if value[0] == "__APPEND__":
                    merged_json[key].extend(value[1:])
                else:
                    merged_json[key] = value
            else:
                merged_json[key] = value
        else:
            merged_json[key] = value
    return merged_json


def create_button():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    package_json_path = os.path.join(root_dir, "../package.json")

    module_suggestion = ""
    if os.path.isfile(package_json_path):
        with open(package_json_path, "r") as file:
            package_data = json.load(file)
            module_suggestion = package_data.get("name", "")

    module = input(f"Enter the module name (default: {module_suggestion}): ") or module_suggestion
    entity = input("Enter the entity name: ")

    print("Select the view:")
    print("1. Detail")
    print("2. List")
    print("3. Edit")
    view_number = input("Enter the view number: ")

    if view_number == "1":
        view = "detail"
        print("Select the button type for the detail view:")
        print("1. Dropdown")
        print("2. Top-right corner")
        detail_button_type = input("Enter the button type number: ")
        if detail_button_type == "1":
            button_type = "dropdown"
        elif detail_button_type == "2":
            button_type = "top-right"
        else:
            print("Invalid button type number")
            return
    elif view_number == "2":
        view = "list"
        button_type = "mass-action"
    elif view_number == "3":
        view = "edit"
        button_type = "top-right"
    else:
        print("Invalid view number")
        return

    name = input("Enter the button name: ")

    label = input("Enter the button label: ")

    print("Select the button style (Optional):")
    print("1. Default")
    print("2. Success")
    print("3. Danger")
    print("4. Warning")
    style_number = input("Enter the style number: ")

    if style_number == "1":
        style = "default"
    elif style_number == "2":
        style = "success"
    elif style_number == "3":
        style = "danger"
    elif style_number == "4":
        style = "warning"
    else:
        print("Invalid style number")
        return

    # Generate the JSON file
    json_dir = os.path.join(root_dir, "../src/backend/Resources/metadata/clientDefs")
    json_file = os.path.join(json_dir, f"{entity}.json")
    create_directory(json_dir)

    new_json = get_json_template("button", view, button_type, label, name, module, entity, style)

    if os.path.isfile(json_file):
        with open(json_file, "r") as file:
            existing_json = json.load(file)
        merged_json = merge_json(existing_json, new_json)
    else:
        merged_json = new_json

    with open(json_file, "w") as file:
        json.dump(merged_json, file, indent=2)
    print(f"JSON file created/updated: {json_file}")

    # Generate the JS file
    js_dir = os.path.join(root_dir, "../src/client/src/handlers")
    js_file = os.path.join(js_dir, f"{entity}.js")

    if os.path.isfile(js_file):
        print(f"Error: JS file already exists: {js_file}")
        return

    create_directory(js_dir)

    js_content = get_js_template("button", view, button_type, module, name, entity)

    with open(js_file, "w") as file:
        file.write(js_content.strip())
    print(f"JS file created: {js_file}")


def command2():
    # Implement the logic for command2
    print("Executing command2")


def command3():
    # Implement the logic for command3
    print("Executing command3")


# Main script loop
while True:
    print("")
    usage()
    command = input("Enter a command: ")

    if command == "button":
        create_button()
    elif command == "command2":
        command2()
    elif command == "command3":
        command3()
    elif command == "help":
        usage()
    elif command == "exit":
        print("Exiting the script.")
        break
    else:
        print(f"Unknown command: {command}")