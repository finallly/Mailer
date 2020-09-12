import json
from abc import ABC, abstractmethod


class Consts(ABC):
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


class Types(ABC):
    json_dict = json.dumps({})

    button_start = 'START🔴SPAM'
    button_info = 'INFOℹ'
    button_services_count = 'SERVICES📊COUNT'
    button_contact = 'CONTACT📲'
    button_private = 'PRIVATE☸'

    @abstractmethod
    def do_not_inherit(self):
        pass
