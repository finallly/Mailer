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

    @abstractmethod
    def do_not_inherit(self):
        pass


class Types(ABC):
    json_dict = json.dumps({})

    @abstractmethod
    def do_not_inherit(self):
        pass
