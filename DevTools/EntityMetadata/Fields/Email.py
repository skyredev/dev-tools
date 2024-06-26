from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Email(Base):
    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "email",
            "notStorable": True
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,

    }
