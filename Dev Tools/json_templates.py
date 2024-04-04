def get_json_template(command, view, button_type, label, name, module, entity, style):
    if command == "button":
        if view == "detail" and button_type == "dropdown":
            return {
                "detailActionList": [
                    "__APPEND__",
                    {
                        "label": label,
                        "name": name,
                        "acl": "edit",
                        "data": {
                            "handler": f"{module}:my-action-handler"
                        },
                        "initFunction": f"init{name.capitalize()}"
                    }
                ]
            }
        elif view == "list" and button_type == "mass-action":
            return {
                "massActionList": [
                    "__APPEND__",
                    name
                ],
                "checkAllResultMassActionList": [
                    "__APPEND__",
                    name
                ],
                "massActionDefs": {
                    name: {
                        "handler": f"{module}:{name}-handler",
                        "initFunction": f"init{name.capitalize()}"
                    }
                }
            }
        else:
            return {
                "menu": {
                    view: {
                        "buttons": [
                            "__APPEND__",
                            {
                                "label": label,
                                "name": name,
                                "action": name,
                                "style": style,
                                "acl": "edit",
                                "aclScope": entity.capitalize(),
                                "data": {
                                    "handler": f"{module}:my-action-handler"
                                },
                                "initFunction": f"init{name.capitalize()}"
                            }
                        ]
                    }
                }
            }
    else:
        # Add templates for other commands here
        return {}