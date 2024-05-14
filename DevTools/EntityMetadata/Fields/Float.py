from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Float(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "notNull": False,
            "type": "float"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.Float,
        "min": ValidationOptions.Float,
        "max": ValidationOptions.Float,
        "decimalPlaces": ValidationOptions.Integer,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse

    }
