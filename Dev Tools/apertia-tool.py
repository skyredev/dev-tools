import os
import json
from json_templates import get_json_template
from js_templates import get_js_template
from php_templates import get_php_template

COMMAND_DESCRIPTIONS = {
    "button": "Creates a new button",
    "hook": "Creates a new hook",
    "entity": "Creates a new entity",
    "help": "Display this help message",
    "exit": "Exit the script"
}

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

HOOK_TYPES = {
    "1": "beforeSave",
    "2": "afterSave",
    "3": "beforeRemove",
    "4": "afterRemove",
    "5": "afterRelate",
    "6": "afterUnrelate",
    "7": "afterMassRelate"
}

ENTITY_TYPES = {
    "1": "Base",
    "2": "BasePlus",
    "3": "Event",
    "4": "Person",
    "5": "Company"
}


def usage():
    print("Available commands:")
    for command, description in COMMAND_DESCRIPTIONS.items():
        print(f"  {command:10} {description}")


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

    module_suggestion = get_module_suggestion(package_json_path)
    module = input(f"Enter the module name (default: {module_suggestion}): ") or module_suggestion
    entity = input("Enter the entity name: ")
    view_number = input("Select the view:\n1. Detail\n2. List\n3. Edit\nEnter the view number: ")

    view = BUTTON_VIEW_TYPES.get(view_number)
    if not view:
        print("Invalid view number")
        return

    if view == "detail":
        detail_button_type = input(
            "Select the button type for the detail view:\n1. Dropdown\n2. Top-right corner\nEnter the button type number: ")
        button_type = BUTTON_DETAIL_TYPES.get(detail_button_type)
        if not button_type:
            print("Invalid button type number")
            return
    elif view == "list":
        button_type = "mass-action"
    else:
        button_type = "top-right"

    name = input("Enter the button name: ")
    label = input("Enter the button label: ")
    style_number = input(
        "Select the button style (Optional):\n1. Default\n2. Success\n3. Danger\n4. Warning\nEnter the style number: ")
    style = BUTTON_STYLES.get(style_number, "default")

    create_button_files(root_dir, module, entity, view, button_type, label, name, style)


def create_hook():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    package_json_path = os.path.join(root_dir, "../package.json")

    module_suggestion = get_module_suggestion(package_json_path)
    module = input(f"Enter the module name (default: {module_suggestion}): ") or module_suggestion
    entity = input("Enter the entity name: ")
    hook_type_number = input(
        "Select the hook type:\n1. beforeSave\n2. afterSave\n3. beforeRemove\n4. afterRemove\n5. afterRelate\n6. afterUnrelate\n7. afterMassRelate\nEnter the hook type number: ")

    hook_type = HOOK_TYPES.get(hook_type_number)
    if not hook_type:
        print("Invalid hook type number")
        return

    name = input("Enter the hook name: ")
    create_hook_file(root_dir, module, hook_type, name, entity)


def create_entity():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    package_json_path = os.path.join(root_dir, "../package.json")

    module_suggestion = get_module_suggestion(package_json_path)
    module = input(f"Enter the module name (default: {module_suggestion}): ") or module_suggestion
    entity_type_number = input(
        "Select the entity type:\n1. Base\n2. Base Plus\n3. Event\n4. Person\n5. Company\nEnter the entity type number: ")

    entity_type = ENTITY_TYPES.get(entity_type_number)
    if not entity_type:
        print("Invalid entity type number")
        return

    entity_name = input("Enter the entity name: ")
    create_entity_files(root_dir, module, entity_name, entity_type)


def get_module_suggestion(package_json_path):
    if os.path.isfile(package_json_path):
        with open(package_json_path, "r") as file:
            package_data = json.load(file)
            return package_data.get("name", "")
    return ""


def create_button_files(root_dir, module, entity, view, button_type, label, name, style):
    # Generate the JSON file
    json_dir = os.path.join(root_dir, "../src/backend/Resources/metadata/clientDefs")
    json_file = os.path.join(json_dir, f"{entity}.json")
    create_directory(json_dir)

    new_json = get_json_template(command="button", view=view, button_type=button_type, label=label, name=name,
                                 module=module, entity=entity, style=style)
    merged_json = merge_json_file(json_file, new_json)
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


def create_hook_file(root_dir, module, hook_type, name, entity):
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


def create_entity_files(root_dir, module, entity_name, entity_type):
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


def merge_json_file(json_file, new_json):
    if os.path.isfile(json_file):
        with open(json_file, "r") as file:
            existing_json = json.load(file)
        return merge_json(existing_json, new_json)
    else:
        return new_json


# Main script loop
while True:
    print("")
    usage()
    command = input("Enter a command: ")

    if command in COMMAND_DESCRIPTIONS:
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
