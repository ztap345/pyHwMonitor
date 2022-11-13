from abc import ABC, abstractmethod
from typing import Type

from src.Connections.AbstractConnection import AbstractConnection


class AbstractProtocol(ABC):

    @abstractmethod
    def __init__(self, conn: Type[AbstractConnection], config: dict[str: any]):
        """
        Create the protocol with a connection methods and a configuration
        :param conn: connection to use
        :param config: configuration for the protocol and connection
        """
        pass

    @abstractmethod
    def start(self):
        """
        Start the protocol
        :return: implementation dependent
        """
        pass

    @abstractmethod
    def stop(self):
        """
        End the protocol
        :return: implementation dependent
        """
        pass

    @abstractmethod
    def transmit(self, *payload: str, pre_payload: str = None) -> any:
        """
        Send with the protocol
        :param payload: payload to send with the protocol
        :param pre_payload: send before the main payload
        :return: implementation dependent
        """
        pass

    @abstractmethod
    def collect(self, is_ack: bool = False) -> any:
        """
        Listen with the protocol
        :param is_ack allow listen for acknowledgment
        :return: what was listened to, type implementation dependent
        """
        pass

    @abstractmethod
    def available(self) -> bool:
        """
        Check if the protocol is available
        :return: true if the protocol is available, otherwise false
        """
        pass
