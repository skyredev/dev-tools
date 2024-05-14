from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Int(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "int"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.Integer,
        "min": ValidationOptions.Integer,
        "max": ValidationOptions.Integer,
        "disableFormatting": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse

    }
