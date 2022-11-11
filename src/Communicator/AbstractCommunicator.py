from abc import ABC, abstractmethod


class AbstractCommunicator(ABC):

    @abstractmethod
    def start(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def stop(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def transmit(self, *payload: str, pre_payload: str = None) -> any:
        """

        :param payload:
        :param pre_payload:
        :return:
        """
        pass

    @abstractmethod
    def collect(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def available(self) -> bool:
        """

        :return:
        """
        pass
