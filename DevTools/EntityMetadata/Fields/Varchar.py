from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Varchar(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "varchar",
            "maxLength": 150,
            "options": [],
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.String,
        "maxLength": ValidationOptions.Integer,
        "copyToClipboard": ValidationOptions.TrueFalse,
        "options": ValidationOptions.Array,
        "pattern": ValidationOptions.String,
        "trim": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "noSpellCheck": ValidationOptions.TrueFalse,
        "optionsPath": ValidationOptions.String
    }
