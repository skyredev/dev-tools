from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Number(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "number",
            "len": 36,
            "notNull": False,
            "unique": False,
            "nextNumber": 1,
            "padLength": 5,
        }

    availableOptions = {
        "prefix": ValidationOptions.String,
        "nextNumber": ValidationOptions.Integer,
        "padLength": ValidationOptions.Integer,
        "copyToClipboard": ValidationOptions.TrueFalse,
    }
