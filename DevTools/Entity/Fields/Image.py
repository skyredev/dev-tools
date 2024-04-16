from DevTools.Entity.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Image(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "image"
        }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "previewSize": ValidationOptions.Array,
        "listPreviewSize": ValidationOptions.Array,
        "maxFileSize": ValidationOptions.Float,
        "readOnly": ValidationOptions.TrueFalse,
        "readOnlyAfterCreate": ValidationOptions.TrueFalse,
        "audited": ValidationOptions.TrueFalse

    }
