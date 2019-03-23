import configparser
from pathlib import Path

config = configparser.ConfigParser()

config_path = Path('config.ini')
if config_path.exists():
    config.read(config_path)
else:
    config['database'] = {'location': 'image-database.db'}
    config['images'] = {'extensions': '.jpeg,.jpg,.png,.gif'}
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    config.read(config_path)
