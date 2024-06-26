import json
from DevTools.Utils.Validators import ValidationOptions


class Base:
    name = "BaseLink"

    data = {
        "type": "baseLink"
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
