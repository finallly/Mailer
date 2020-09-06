import configparser

config = configparser.ConfigParser()
config.read('config.ini')


class ConfigHandler:
    csv_file_name = config['DATA']['file_name']
    reading_mode = config['DATA']['mode']
    csv_delimiter = config['DATA']['delimiter']
    server_address = config['DATA']['server']
    csv_encoding = config['DATA']['encoding']

    database_host = config['DATA']['db_host']
    database_user = config['DATA']['db_user']
    database_pass = config['DATA']['db_pass']
    database_name = config['DATA']['db_name']
    table_name = config['DATA']['table_name']
    auth_plugin = config['DATA']['auth_plugin']

    mail_password_index = int(config['DATA']['password_index'])
    mail_address_index = int(config['DATA']['mail_index'])

    token = config['TOKEN']['token']
