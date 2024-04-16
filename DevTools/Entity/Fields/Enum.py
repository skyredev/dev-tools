from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Enum(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "enum"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "options": ValidationOptions.Array,
        "default": ValidationOptions.String,
        "optionsReference": ValidationOptions.String,
        "isSorted": ValidationOptions.TrueFalse,
        "translation": ValidationOptions.String,
        "optionsPath": ValidationOptions.String,
        "style": ValidationOptions.String,
        "displayAsLabel": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse
    }
