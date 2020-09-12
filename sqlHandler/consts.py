import json
from abc import ABC, abstractmethod


class CONSTS(ABC):
    date_format = '%d.%m.%Y'
    time_format = '%H:%M:%S'
    first_name = 'first_name'
    last_name = 'last_name'
    username = 'username'
    info = 'info'
    status = 'status'
    id = 'id'
    is_blocked = 'blocked'

    change_status = 'change_status'
    block_user = 'block_user'
    number_info = 'number_info'

    command_first = 0
    command_second = 1

    @abstractmethod
    def do_not_inherit(self):
        pass


class TYPES(ABC):
    json_dict = json.dumps({})
    params_dict = {"country_code": 7}

    button_start = 'START🔴SPAM'
    button_info = 'INFOℹ'
    button_services_count = 'SERVICES📊COUNT'
    button_contact = 'CONTACT📲'
    button_private = 'PRIVATE⚜'

    button_status = 'STATUS🔋'
    button_stop = 'STOP⛔'

    callback_status = 'status'
    callback_stop = 'stop'

    @abstractmethod
    def do_not_inherit(self):
        pass


class STRINGS(ABC):
    info_string = '''
    this is sms spam bot'''
    contact_string = '''
    for any info, offers and sponsorship contact\n@finalllly'''
    private_string = '''...'''
