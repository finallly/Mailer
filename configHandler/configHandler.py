import ast
import configparser
from abc import ABC, abstractmethod

config = configparser.ConfigParser()
config.read('config.ini')


class ConfigHandler(ABC):
    csv_file_name = config['DATA']['file_name']
    reading_mode = config['DATA']['mode']
    csv_delimiter = config['DATA']['delimiter']
    server_address = config['DATA']['server']
    csv_encoding = config['DATA']['encoding']

    database_host = config['DATABASE']['db_host']
    database_user = config['DATABASE']['db_user']
    database_pass = config['DATABASE']['db_pass']
    database_name = config['DATABASE']['db_name']
    table_name = config['DATABASE']['table_name']
    auth_plugin = config['DATABASE']['auth_plugin']

    api_host = config['API']['api_host']
    api_port = config['API']['api_port']
    api_protocol = config['API']['api_protocol']
    attack_start = config['API']['api_attack_start']
    attack_status = config['API']['api_attack_status']
    mod_status = config['API']['api_status_postfix']
    mod_stop = config['API']['api_stop_postfix']
    count_info = config['API']['api_count_info']
    api_number = config['API']['api_number']
    api_phone = config['API']['api_phone']

    mail_password_index = int(config['DATA']['password_index'])
    mail_address_index = int(config['DATA']['mail_index'])

    token = config['TOKEN']['token']

    admins = config['ADMIN']['list_id']

    attack_link = f"{api_protocol}://{api_host}:{api_port}/{attack_start}"
    attack_mod_link = f"{api_protocol}://{api_host}:{api_port}/{attack_status}"
    count_link = f"{api_protocol}://{api_host}:{api_port}/{count_info}"

    pattern_list = [rf'[7|8]\D?{number[1:4]}\D*{number[4:7]}\D?{number[7:9]}\D?{number[9:]}' for number in
                    ast.literal_eval(config['ADMIN']['block_list'])]

    @abstractmethod
    def do_not_inherit(self):
        pass
