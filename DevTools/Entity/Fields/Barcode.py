from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Barcode(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "barcode",
            "len": 255
        }

    availableOptionsForTranslate = {

    }

    availableOptionsAvailableValues = {
        "codeType": {
            "CODE128", "CODE128A", "CODE128B", "CODE128C",
            "EAN13", "EAN8", "EAN5", "EAN2", "UPC", "UPCE",
            "ITF14", "pharmacode", "QRcode"
        }
    }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "codeType": ValidationOptions.Array,
        "lastChar": ValidationOptions.String,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse

    }
