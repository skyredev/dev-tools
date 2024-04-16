from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Email(Base):
    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "email"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,

    }
