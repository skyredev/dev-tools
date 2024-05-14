from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Address(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "address"
        }

    availableOptions = {
        "viewMap": ValidationOptions.TrueFalse,

    }
