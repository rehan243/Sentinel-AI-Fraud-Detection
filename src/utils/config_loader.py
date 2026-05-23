import json
import os

class ConfigLoader:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config_data = {}

    def load_config(self) -> None:
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file {self.config_file} not found")
        with open(self.config_file, 'r') as file:
            self.config_data = json.load(file)

    def get(self, key: str, default=None):
        return self.config_data.get(key, default)

    def __getitem__(self, key: str):
        return self.get(key)

    def __repr__(self):
        return f"<ConfigLoader config_file='{self.config_file}'>"

# example usage
if __name__ == "__main__":
    # TODO: update with actual config file path
    config_loader = ConfigLoader('path/to/config.json')
    try:
        config_loader.load_config()
        print(config_loader['some_key'])  # replace with real key
    except Exception as e:
        print(f"Error loading config: {e}")