from enum import Enum


class ConnectionState(Enum):
    NOT_INITIALIZED = 0
    CONNECTED = 1
    DISCONNECTED = 2
