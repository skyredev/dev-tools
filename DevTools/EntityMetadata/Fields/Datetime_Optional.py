from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Datetime_Optional(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "datetimeOptional"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.String,
        "after": ValidationOptions.String,
        "before": ValidationOptions.String,
        "useNumericFormat": ValidationOptions.TrueFalse,
        "hasSeconds": ValidationOptions.TrueFalse,
        "minuteStep": ValidationOptions.Integer,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse
    }
