from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Barcode(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "barcode",
            "len": 255
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "codeType": ValidationOptions.Array,
        "lastChar": ValidationOptions.String,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse

    }
