class TemplateManager:

    @staticmethod
    def set_template_values(content, values: dict):
        if isinstance(content, str):
            # Replace placeholders in string content
            for placeholder, value in values.items():
                content = content.replace(placeholder, str(value))
            return content
        elif isinstance(content, dict):
            # Recursively replace placeholders in dictionary keys and values
            new_content = {}
            for key, value in content.items():
                # Replace placeholders in the key
                new_key = key
                for placeholder, real_value in values.items():
                    new_key = new_key.replace(placeholder, str(real_value))

                # Process the value
                if isinstance(value, dict):
                    new_content[new_key] = TemplateManager.set_template_values(value, values)
                elif isinstance(value, list):
                    new_content[new_key] = [TemplateManager.set_template_values(item, values) if isinstance(item, (dict, str)) else item for item in value]
                elif isinstance(value, str):
                    new_content[new_key] = TemplateManager.set_template_values(value, values)
                else:
                    new_content[new_key] = value
            return new_content
        else:
            raise TypeError("Content must be a string or a dictionary")