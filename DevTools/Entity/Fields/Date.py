from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Date(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "date"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.String,
        "after": ValidationOptions.String,
        "before": ValidationOptions.String,
        "useNumericFormat": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse
    }
