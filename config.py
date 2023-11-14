import os

import yaml


class Config:
    def __init__(self):
        self.slack_token = self._get_env_variable('SLACK_TOKEN')
        self.default_slack_email = self._get_env_variable('DEFAULT_SLACK_EMAIL')
        self.author_mapping = self._load_author_mapping('/config/author_mapping.yml')

    @staticmethod
    def _get_env_variable(name):
        value = os.environ.get(name)
        if not value:
            raise ValueError(f"{name} environment variable not set")
        return value

    @staticmethod
    def _load_author_mapping(file_path):
        with open(file_path, 'r') as mapping_file:
            return yaml.safe_load(mapping_file)
