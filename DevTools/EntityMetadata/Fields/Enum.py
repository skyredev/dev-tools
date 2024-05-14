from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Enum(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "enum",
            "style": {}
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "options": ValidationOptions.Array,
        "default": ValidationOptions.String,
        "optionsReference": ValidationOptions.String,
        "isSorted": ValidationOptions.TrueFalse,
        "translation": ValidationOptions.String,
        "optionsPath": ValidationOptions.String,
        "style": ValidationOptions.JsonObject,
        "displayAsLabel": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse
    }
