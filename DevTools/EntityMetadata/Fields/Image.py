from DevTools.EntityMetadata.Fields.Base import Base
from DevTools.Utils.Validators import ValidationOptions


class Image(Base):

    def __init__(self, name):
        super().__init__(name)
        self.data = {
            "type": "image",
            "previewSize": "small",
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

    linkDefs = {
        "type": "belongsTo",
        "entity": "Attachment",
        "skipOrmDefs": True,
        "utility": True,
    }
