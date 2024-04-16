from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Phone(Base):
    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "phone"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "typeList": ValidationOptions.Array,
        "defaultType": ValidationOptions.String,
        "audited": ValidationOptions.TrueFalse


    }
