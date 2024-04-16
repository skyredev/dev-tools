from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Link_Parent(Base):
    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "linkParent"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "entityList": ValidationOptions.Array,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse


    }
