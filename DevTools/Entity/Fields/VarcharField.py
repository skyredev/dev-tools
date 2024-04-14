from DevTools.Entity.Fields.BaseField import BaseField
from DevTools.Utils.Validators import ValidationOptions


class VarcharField(BaseField):

    data = {
        "type": "varchar"
    }

    availableOptions = {
        "required": ValidationOptions.TrueFalse,
        "maxLength": ValidationOptions.Integer,
        "copyToClipboard": ValidationOptions.TrueFalse,
        "options": ValidationOptions.Array,
    }
