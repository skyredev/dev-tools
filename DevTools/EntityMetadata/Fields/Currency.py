from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Currency(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "currency"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.Float,
        "min": ValidationOptions.Float,
        "max": ValidationOptions.Float,
        "onlyDefaultCurrency": ValidationOptions.TrueFalse,
        "conversionDisabled": ValidationOptions.TrueFalse,
        "decimal": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "precision": ValidationOptions.Integer,
        "scale": ValidationOptions.Integer

    }
