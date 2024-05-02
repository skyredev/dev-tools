import json

from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Multi_Enum(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "multiEnum",
            "storeArrayValues": True,
            "default": [],
            "style": {},
        }
        self.initAvailableOptionsForTranslate()

    def initAvailableOptionsForTranslate(self):
        # vlevo availableOptions, vpravo je path v JSONu, vcetne tech hodnot,
        # meli by se dat generovat na zmenu, tim by se mel preklad zjednodusti a byt obecnejsi

        availableOptionsForTranslate = {
            #"options": "options:" + self.name + ":" + json.dump(self.availableOptions.get("options"))
        }

    availableOptionsAvailableValues = {

    }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "options": ValidationOptions.Array,
        "optionsReference": ValidationOptions.String,
        "default": ValidationOptions.Array,
        "isSorted": ValidationOptions.TrueFalse,
        "translation": ValidationOptions.String,
        "allowCustomOptions": ValidationOptions.TrueFalse,
        "maxCount": ValidationOptions.Integer,
        "style": ValidationOptions.JsonObject,
        "displayAsLabel": ValidationOptions.TrueFalse,
        "displayAsList": ValidationOptions.TrueFalse,
        "pattern": ValidationOptions.String,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "optionsPath": ValidationOptions.String
    }
