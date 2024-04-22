from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Boolean(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "notNull": True,
            "type": "bool"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse
    }
