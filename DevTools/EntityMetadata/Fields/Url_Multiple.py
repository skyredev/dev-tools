from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Url_Multiple(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "urlMultiple",
            "storeArrayValues": True
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "maxCount": ValidationOptions.Integer,
        "strip": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse
    }
