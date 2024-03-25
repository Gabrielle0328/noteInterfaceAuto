from main import ENVIRON, Dir
import yaml


class YamlRead:
    @staticmethod
    def env_config():
        with open(file=f'{Dir}/envConfig/{ENVIRON}/config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def data_config():
        with open(file=f'{Dir}/data/interface_config.yml', mode='r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
