from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Checklist(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "checklist",
            "storeArrayValues": True,
            "default": [],
            "options": ["Placeholder"]
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "options": ValidationOptions.Array,
        "optionsReference": ValidationOptions.String,
        "default": ValidationOptions.Array,
        "isSorted": ValidationOptions.TrueFalse,
        "translation": ValidationOptions.String,
        "maxCount": ValidationOptions.Integer,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "optionsPath": ValidationOptions.String

    }
