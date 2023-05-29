import yaml
from envyaml import EnvYAML

# read file db_config.yaml and parse config
db_config = EnvYAML('database/db_config.yml')

def generate_uri_from_file(config_file='database/db_config.yml'):
    with open(config_file, 'r') as f_handle:
        config = yaml.safe_load(f_handle)
    
    database = config.get('database')
    username = config.get('username')
    password = db_config['password']
    host = config.get('host')
    port = config.get('port')
    db_name = config.get('db_name')

    database_uri = f"{database}://{username}:{password}@{host}:{port}/{db_name}"

    return database_uri


def generate_uri2_from_file(config_file='database/db_config.yml'):
    with open(config_file, 'r') as f_handle:
        config = yaml.safe_load(f_handle)

    database = config.get('database')
    username = config.get('username')
    password = db_config['password']
    host = config.get('host')
    port = config.get('port')
    db_name = config.get('db_name')

    database2_uri = f"{database}://{username}:{password}@{host}:{port}/{db_name}"

    return database2_uri