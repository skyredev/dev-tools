from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class File(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "file"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "sourceList": ValidationOptions.Array,
        "maxFileSize": ValidationOptions.Float,
        "accept": ValidationOptions.Array,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse



    }
