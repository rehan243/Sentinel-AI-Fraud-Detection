import json
import os

class ConfigLoader:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at: {self.config_path}")
        
        with open(self.config_path, 'r') as config_file:
            try:
                return json.load(config_file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON: {e}")

    def get(self, key: str, default=None):
        return self.config_data.get(key, default)

    def set(self, key: str, value):
        self.config_data[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_path, 'w') as config_file:
            json.dump(self.config_data, config_file, indent=4)

# usage example
if __name__ == "__main__":
    config_loader = ConfigLoader("config.json")
    print(config_loader.get("some_setting", "default_value"))
    # TODO: add more error handling and logging if necessary