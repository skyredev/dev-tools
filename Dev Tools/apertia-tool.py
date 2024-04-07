import os
import json
from json_templates import get_json_template
from js_templates import get_js_template
from php_templates import get_php_template


def usage():
    print("Available commands:")
    print("  button           Creates a new button")
    print("  hook             Creates a new hook")
    print("  entity           Creates a new entity")
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

    styles = {
        "1": "default",
        "2": "success",
        "3": "danger",
        "4": "warning",
    }
    if style_number not in styles:
        print("Invalid style number")
        return

    style = styles[style_number]

    # Generate the JSON file
    json_dir = os.path.join(root_dir, "../src/backend/Resources/metadata/clientDefs")
    json_file = os.path.join(json_dir, f"{entity}.json")
    create_directory(json_dir)

    new_json = get_json_template(command="button", view=view, button_type=button_type, label=label, name=name, module=module, entity=entity, style=style)

    if os.path.isfile(json_file):
        with open(json_file, "r") as file:
            existing_json = json.load(file)
        merged_json = merge_json(existing_json, new_json)
    else:
        merged_json = new_json

    with open(json_file, "w", encoding='utf-8') as file:
        json.dump(merged_json, file, indent=2, ensure_ascii=False)
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


def create_hook():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    package_json_path = os.path.join(root_dir, "../package.json")

    module_suggestion = ""
    if os.path.isfile(package_json_path):
        with open(package_json_path, "r") as file:
            package_data = json.load(file)
            module_suggestion = package_data.get("name", "")

    module = input(f"Enter the module name (default: {module_suggestion}): ") or module_suggestion
    entity = input("Enter the entity name: ")

    print("Select the hook type:")
    print("1. beforeSave")
    print("2. afterSave")
    print("3. beforeRemove")
    print("4. afterRemove")
    print("5. afterRelate")
    print("6. afterUnrelate")
    print("7. afterMassRelate")
    hook_type_number = input("Enter the hook type number: ")

    hook_types = {
        "1": "beforeSave",
        "2": "afterSave",
        "3": "beforeRemove",
        "4": "afterRemove",
        "5": "afterRelate",
        "6": "afterUnrelate",
        "7": "afterMassRelate"
    }

    if hook_type_number not in hook_types:
        print("Invalid hook type number")
        return

    hook_type = hook_types[hook_type_number]

    name = input("Enter the hook name: ")

    # Generate the PHP file
    php_dir = os.path.join(root_dir, f"../src/backend/Hooks/{entity}")
    php_file = os.path.join(php_dir, f"{name}.php")
    create_directory(php_dir)

    if os.path.isfile(php_file):
        print(f"Error: PHP file already exists: {php_file}")
        return

    php_content = get_php_template(module, hook_type, name, entity)

    with open(php_file, "w") as file:
        file.write(php_content.strip())
    print(f"PHP file created: {php_file}")


def create_entity():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    package_json_path = os.path.join(root_dir, "../package.json")

    module_suggestion = ""
    if os.path.isfile(package_json_path):
        with open(package_json_path, "r") as file:
            package_data = json.load(file)
            module_suggestion = package_data.get("name", "")

    module = input(f"Enter the module name (default: {module_suggestion}): ") or module_suggestion

    print("Select the entity type:")
    print("1. Base")
    print("2. Base Plus")
    print("3. Event")
    print("4. Person")
    print("5. Company")
    entity_type_number = input("Enter the entity type number: ")

    entity_types = {
        "1": "Base",
        "2": "BasePlus",
        "3": "Event",
        "4": "Person",
        "5": "Company"
    }

    entity_type = entity_types.get(entity_type_number)
    if not entity_type:
        print("Invalid entity type number")
        return

    entity_name = input("Enter the entity name: ")

    # Generate the entityDefs JSON file
    entity_defs_dir = os.path.join(root_dir, "../src/backend/Resources/metadata/entityDefs")
    entity_defs_file = os.path.join(entity_defs_dir, f"{entity_name}.json")
    create_directory(entity_defs_dir)
    entity_defs_json = get_json_template(command="entity", entity_name=entity_name, entity_type=entity_type)
    with open(entity_defs_file, "w", encoding='utf-8') as file:
        json.dump(entity_defs_json, file, indent=2, ensure_ascii=False)
    print(f"entityDefs JSON file created: {entity_defs_file}")

    # Generate the scopes JSON file
    scopes_dir = os.path.join(root_dir, "../src/backend/Resources/metadata/scopes")
    scopes_file = os.path.join(scopes_dir, f"{entity_name}.json")
    create_directory(scopes_dir)
    scopes_json = get_json_template(command="scope", entity_name=entity_name, entity_type=entity_type, module=module)
    with open(scopes_file, "w", encoding='utf-8') as file:
        json.dump(scopes_json, file, indent=2, ensure_ascii=False)
    print(f"scopes JSON file created: {scopes_file}")


# Main script loop
while True:
    print("")
    usage()
    command = input("Enter a command: ")

    if command == "button":
        create_button()
    elif command == "hook":
        create_hook()
    elif command == "entity":
        create_entity()
    elif command == "help":
        usage()
    elif command == "exit":
        print("Exiting the script.")
        break
    else:
        print(f"Unknown command: {command}")