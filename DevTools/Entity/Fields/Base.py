import json
from DevTools.Utils.Validators import ValidationOptions


class Base:
    name = "BaseField"

    data = {
        "type": "baseField"
    }

    availableOptions = {

    }

    def __init__(self, name):
        self.name = name

    def set_name(self, new_name):
        self.name = new_name

    def set_value(self, key, value):
        self.data[key] = value

    def remove_value(self, key):
        self.data.pop(key)

    def generate_json(self):
        return json.dumps({self.name: self.data}, indent=4)
