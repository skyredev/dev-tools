from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Array(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "array",
            "storeArrayValues": True,
            "noEmptyString": True,
            "default": []
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "options": ValidationOptions.Array,
        "optionsReference": ValidationOptions.String,
        "default": ValidationOptions.Array,
        "translation": ValidationOptions.String,
        "allowCustomOptions": ValidationOptions.TrueFalse,
        "noEmptyString": ValidationOptions.TrueFalse,
        "displayAsList": ValidationOptions.TrueFalse,
        "maxCount": ValidationOptions.Integer,
        "pattern": ValidationOptions.String,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "optionsPath": ValidationOptions.String

    }
