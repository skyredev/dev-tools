
class Base:
    name = "BaseField"

    data = {
        "type": "baseField"
    }

    linkDefs = {

    }

    availableOptionsForTranslate = [
        "options"
    ]

    availableOptionsAvailableValues = {
        "codeType": [
            "CODE128", "CODE128A", "CODE128B", "CODE128C",
            "EAN13", "EAN8", "EAN5", "EAN2", "UPC", "UPCE",
            "ITF14", "pharmacode", "QRcode"
        ],
        "style": [
            "Default",
            "Success",
            "Danger",
            "Warning",
            "Info",
            "Primary"
        ]
    }

    availableOptions = {

    }

    def __init__(self, name):
        self.name = name

    def set_name(self, new_name):
        self.name = new_name

    def get_name(self):
        return self.name

    def set_value(self, key, value):
        self.data[key] = value

    def remove_value(self, key):
        self.data.pop(key)

    def get_data(self):
        return self.data

    def get_link_defs(self):
        return self.linkDefs
