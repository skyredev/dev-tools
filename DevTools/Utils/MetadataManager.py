import json


class MetadataManager:
    @staticmethod
    def get(filepath, section_path=None):
        if section_path:
            data = MetadataManager.get(filepath)
            for section in section_path:
                data = data.get(section, {})
            return data
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def list(section_path, filepath):
        data = MetadataManager.get(filepath)
        for section in section_path:
            data = data.get(section, {})
        return list(data.keys()) if data else []

    @staticmethod
    def set(section_path, key, value, filepath):
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            # Navigate/create the path in the data
            current_section = data
            for section in section_path:
                if section not in current_section:
                    current_section[section] = {}
                current_section = current_section[section]

            # Set the value at the final section
            current_section[key] = value

            file.seek(0)
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
            file.truncate()

    @staticmethod
    def set_array(section_path, index, value, filepath):
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            current_section = data
            for section in section_path:
                if section not in current_section:
                    current_section[section] = []
                current_section = current_section[section]

            if not isinstance(current_section, list):
                print(f"Error: Expected a list at {section_path}, found {type(current_section).__name__}.")
                return

            if len(current_section) <= index:
                current_section.extend([None] * (index + 1 - len(current_section)))

            current_section[index] = value

            file.seek(0)
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
            file.truncate()

    @staticmethod
    def delete(section_path, key, filepath):
        with open(filepath, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            # Navigate to the correct section
            current_section = data
            for section in section_path:
                if section in current_section:
                    current_section = current_section[section]
                else:
                    return  # If the section path does not exist, exit the function

            # Remove the key if it exists
            if key in current_section:
                del current_section[key]

            file.seek(0)
            file.write(json.dumps(data, indent=4, ensure_ascii=False))
            file.truncate()
