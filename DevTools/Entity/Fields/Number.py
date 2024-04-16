from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Number(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "number"
        }

    availableOptions = {
        "prefix": ValidationOptions.String,
        "nextNumber": ValidationOptions.Integer,
        "padLength": ValidationOptions.Integer,
        "copyToClipboard": ValidationOptions.TrueFalse,

    }
