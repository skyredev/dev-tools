from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Url(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "url",
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.String,
        "maxLength": ValidationOptions.Integer,
        "strip": ValidationOptions.TrueFalse,
        "copyToClipboard": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse


    }
