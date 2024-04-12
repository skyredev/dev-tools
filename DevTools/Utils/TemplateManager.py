from DevTools.Button.ButtonTemplates import ButtonTemplates
from DevTools.Hook.HookTemplates import HookTemplates
from DevTools.Entity.EntityTemplates import EntityTemplates


class TemplateManager:
    def __init__(self):
        self.templates = {
            'button': self.button_template,
            'hook': self.hook_template,
            'entity': self.entity_template
        }

    def get_template(self, template_type, **kwargs):
        return self.templates[template_type](**kwargs)

    @staticmethod
    def button_template(**kwargs):
        if kwargs["view"] == "detail" and kwargs["button_type"] == "dropdown":
            return ButtonTemplates.get_detail_dropdown(module=kwargs["module"], entity=kwargs["entity"], name=kwargs["name"], converted_name=kwargs["converted_name"])
        elif kwargs["list"] == "detail" and kwargs["button_type"] == "mass-action":
            return ButtonTemplates.get_list_mass_action(module=kwargs["module"], entity=kwargs["entity"], name=kwargs["name"], converted_name=kwargs["converted_name"])
        else:
            return ButtonTemplates.get_detail_top_right(module=kwargs["module"], entity=kwargs["entity"], name=kwargs["name"], converted_name=kwargs["converted_name"])

    @staticmethod
    def hook_template(**kwargs):
        return HookTemplates.get_hook(kwargs["module"], kwargs["hook_type"], kwargs["name"], kwargs["entity"])

    @staticmethod
    def entity_template(**kwargs):
        return ""
