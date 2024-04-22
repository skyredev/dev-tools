from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Text(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "text",
            "rowsMin": 2,
            "cutHeight": 200,
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.String,
        "maxLength": ValidationOptions.Integer,
        "seeMoreDisabled": ValidationOptions.TrueFalse,
        "rows": ValidationOptions.Integer,
        "rowsMin": ValidationOptions.Integer,
        "cutHeight": ValidationOptions.Integer,
        "displayRawText": ValidationOptions.TrueFalse,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse
    }
