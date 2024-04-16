from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Multi_Enum(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "multiEnum"
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
        "style": ValidationOptions.String,
        "displayAsLabel": ValidationOptions.TrueFalse,
        "displayAsList": ValidationOptions.TrueFalse,
        "pattern": ValidationOptions.String,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "optionsPath": ValidationOptions.String


    }
