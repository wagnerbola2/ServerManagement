from enum import Enum

class Options(Enum):
    START_SERVICE = 0
    STOP_SERVICE = 1
    RESTART_SERVICE = 2
    START_ALL_SERVICES = 3
    STOP_ALL_SERVICES = 4
    RESTART_ALL_SERVICES = 5
    CHANGE_SERVER = 6
    EXIT = 7
