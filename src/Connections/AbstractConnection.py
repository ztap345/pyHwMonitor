from abc import ABC, abstractmethod


# class that describes a connection to an external source
class AbstractConnection(ABC):
    @abstractmethod
    def setup(self, **kwargs) -> None:
        """
        Set up whatever communications protocol necessary
        :param kwargs: any key word args needed
        :return: None
        """
        pass

    @abstractmethod
    def connect(self) -> bool:
        """
        Initialize any connection
        :return: True if connection successful, otherwise False
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close the connection
        :return: None
        """
        pass

    @abstractmethod
    def connected(self) -> bool:
        """
        Check if connection is alive
        :return: True if the connection is alive, otherwise False
        """
        pass

    @abstractmethod
    def send(self, payload: str) -> any:
        """
        Send data using the connection
        :param payload: data to send
        :return: whatever needs to be returned
        """
        pass

    @abstractmethod
    def recv(self) -> str:
        """
        Receive data using the connection
        :return: result of the receipt
        """
        pass
