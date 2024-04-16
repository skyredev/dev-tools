from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Wysiwyg(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "wysiwyg"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "default": ValidationOptions.String,
        "height": ValidationOptions.Integer,
        "minHeight": ValidationOptions.Integer,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "attachmentField": ValidationOptions.String,
        "useIframe": ValidationOptions.TrueFalse,
        "maxLength": ValidationOptions.Integer,
        "audited": ValidationOptions.TrueFalse

    }
