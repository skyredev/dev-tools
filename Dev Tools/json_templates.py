def get_json_template(command, **kwargs):
    if command == "button":
        view = kwargs.get("view")
        button_type = kwargs.get("button_type")
        label = kwargs.get("label")
        name = kwargs.get("name")
        module = kwargs.get("module")
        entity = kwargs.get("entity")
        style = kwargs.get("style")

        if view == "detail" and button_type == "dropdown":
            return {
                "detailActionList": [
                    "__APPEND__",
                    {
                        "label": label,
                        "name": name,
                        "acl": "edit",
                        "data": {
                            "handler": f"{module}:{name}-handler"
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
                                    "handler": f"{module}:{name}-handler"
                                },
                                "initFunction": f"init{name.capitalize()}"
                            }
                        ]
                    }
                }
            }

    elif command == "entity":
        entity_name = kwargs.get("entity_name")
        entity_type = kwargs.get("entity_type")

        if entity_type == "Base":
            return {
                "fields": {
                    "assignedUser": {"type": "link", "label": "Přiřazený uživatel"},
                    "createdAt": {"type": "datetime", "label": "Vytvořeno"},
                    "createdBy": {"type": "link", "label": "Vytvořil"},
                    "description": {"type": "text", "label": "Popis"},
                    "modifiedAt": {"type": "datetime", "label": "Upraveno"},
                    "modifiedBy": {"type": "link", "label": "Upravil"},
                    "name": {"type": "varchar", "label": "Název"},
                    "teams": {"type": "linkMultiple", "label": "Týmy"}
                },
                "links": {}
            }
        elif entity_type == "BasePlus":
            return {
                "fields": {
                    "assignedUser": {"type": "link", "label": "Přiřazený uživatel"},
                    "createdAt": {"type": "datetime", "label": "Vytvořeno"},
                    "createdBy": {"type": "link", "label": "Vytvořil"},
                    "description": {"type": "text", "label": "Popis"},
                    "modifiedAt": {"type": "datetime", "label": "Upraveno"},
                    "modifiedBy": {"type": "link", "label": "Upravil"},
                    "name": {"type": "varchar", "label": "Název"},
                    "teams": {"type": "linkMultiple", "label": "Týmy"}
                },
                "links": {
                    "emails": {"type": "hasChildren", "entity": "Email"},
                    "tasks": {"type": "hasChildren", "entity": "Task"}
                }
            }
        elif entity_type == "Event":
            return {
                "fields": {
                    "assignedUser": {"type": "link", "label": "Přiřazený uživatel"},
                    "createdAt": {"type": "datetime", "label": "Vytvořeno"},
                    "createdBy": {"type": "link", "label": "Vytvořil"},
                    "dateEnd": {"type": "datetime", "label": "Date End"},
                    "dateEndDate": {"type": "date", "label": "Date End (all day)"},
                    "dateStart": {"type": "datetime", "label": "Date Start"},
                    "dateStartDate": {"type": "date", "label": "Date Start (all day)"},
                    "description": {"type": "text", "label": "Popis"},
                    "duration": {"type": "duration", "label": "Duration"},
                    "isAllDay": {"type": "bool", "label": "Is All-Day"},
                    "modifiedAt": {"type": "datetime", "label": "Upraveno"},
                    "modifiedBy": {"type": "link", "label": "Upravil"},
                    "name": {"type": "varchar", "label": "Název"},
                    "parent": {"type": "linkParent", "label": "Parent"},
                    "reminders": {"type": "jsonArray", "label": "Reminders"},
                    "status": {"type": "enum", "label": "Status"},
                    "teams": {"type": "linkMultiple", "label": "Týmy"}
                },
                "links": {
                    "parent": {"type": "belongsTo", "entity": "Event"}
                }
            }
        elif entity_type == "Person":
            return {
                "fields": {
                    "address": {"type": "address", "label": "Address"},
                    "addressCity": {"type": "varchar", "label": "Město"},
                    "addressCountry": {"type": "varchar", "label": "Země"},
                    "addressMap": {"type": "map", "label": "Mapa"},
                    "addressPostalCode": {"type": "varchar", "label": "PSČ"},
                    "addressState": {"type": "varchar", "label": "Kraj"},
                    "addressStreet": {"type": "text", "label": "Ulice"},
                    "assignedUser": {"type": "link", "label": "Přiřazený uživatel"},
                    "createdAt": {"type": "datetime", "label": "Vytvořeno"},
                    "createdBy": {"type": "link", "label": "Vytvořil"},
                    "description": {"type": "text", "label": "Popis"},
                    "emailAddress": {"type": "email", "label": "Email"},
                    "emailAddressIsInvalid": {"type": "bool", "label": "Email Address is Invalid"},
                    "emailAddressIsOptedOut": {"type": "bool", "label": "E-mailová adresa je odhlášena"},
                    "firstName": {"type": "varchar", "label": "Křestní jméno"},
                    "lastName": {"type": "varchar", "label": "Příjmení"},
                    "middleName": {"type": "varchar", "label": "Prostřední jméno"},
                    "modifiedAt": {"type": "datetime", "label": "Upraveno"},
                    "modifiedBy": {"type": "link", "label": "Upravil"},
                    "name": {"type": "personName", "label": "Název"},
                    "phoneNumber": {"type": "phone", "label": "Telefon"},
                    "phoneNumberIsInvalid": {"type": "bool", "label": "Phone Number is Invalid"},
                    "phoneNumberIsOptedOut": {"type": "bool", "label": "Telefonní číslo je odhlášené"},
                    "salutationName": {"type": "enum", "label": "Oslovení"},
                    "teams": {"type": "linkMultiple", "label": "Týmy"}
                },
                "links": {
                    "tasks": {"type": "hasChildren", "entity": "Task"}
                }
            }
        elif entity_type == "Company":
            return {
                "fields": {
                    "assignedUser": {"type": "link", "label": "Přiřazený uživatel"},
                    "billingAddress": {"type": "address", "label": "Billing Address"},
                    "billingAddressCity": {"type": "varchar", "label": "Město"},
                    "billingAddressCountry": {"type": "varchar", "label": "Země"},
                    "billingAddressMap": {"type": "map", "label": "Mapa"},
                    "billingAddressPostalCode": {"type": "varchar", "label": "PSČ"},
                    "billingAddressState": {"type": "varchar", "label": "Kraj"},
                    "billingAddressStreet": {"type": "text", "label": "Ulice"},
                    "createdAt": {"type": "datetime", "label": "Vytvořeno"},
                    "createdBy": {"type": "link", "label": "Vytvořil"},
                    "description": {"type": "text", "label": "Popis"},
                    "emailAddress": {"type": "email", "label": "Email"},
                    "emailAddressIsInvalid": {"type": "bool", "label": "Email Address is Invalid"},
                    "emailAddressIsOptedOut": {"type": "bool", "label": "E-mailová adresa je odhlášena"},
                    "modifiedAt": {"type": "datetime", "label": "Upraveno"},
                    "modifiedBy": {"type": "link", "label": "Upravil"},
                    "name": {"type": "varchar", "label": "Název"},
                    "phoneNumber": {"type": "phone", "label": "Telefon"},
                    "phoneNumberIsInvalid": {"type": "bool", "label": "Phone Number is Invalid"},
                    "phoneNumberIsOptedOut": {"type": "bool", "label": "Telefonní číslo je odhlášené"},
                    "shippingAddress": {"type": "address", "label": "Shipping Address"},
                    "shippingAddressCity": {"type": "varchar", "label": "Město (doručovací)"},
                    "shippingAddressCountry": {"type": "varchar", "label": "Země (doručovací)"},
                    "shippingAddressMap": {"type": "map", "label": "Map (Shipping)"},
                    "shippingAddressPostalCode": {"type": "varchar", "label": "PSČ (doručovací)"},
                    "shippingAddressState": {"type": "varchar", "label": "Kraj (doručovací)"},
                    "shippingAddressStreet": {"type": "text", "label": "Ulice (doručovací)"},
                    "teams": {"type": "linkMultiple", "label": "Týmy"},
                    "website": {"type": "url", "label": "Website"}
                },
                "links": {
                    "tasks": {"type": "hasChildren", "entity": "Task"}
                }
            }
        else:
            return {}

    elif command == "scope":
        entity_name = kwargs.get("entity_name")
        entity_type = kwargs.get("entity_type")
        module = kwargs.get("module")

        return {
            "entity": True,
            "layouts": True,
            "tab": True,
            "acl": True,
            "aclPortal": True,
            "aclPortalLevelList": [
                "all",
                "account",
                "contact",
                "own",
                "no"
            ],
            "customizable": True,
            "importable": True,
            "notifications": True,
            "stream": True,
            "disabled": False,
            "type": entity_type,
            "module": module,
            "object": True
        }

    else:
        return {}