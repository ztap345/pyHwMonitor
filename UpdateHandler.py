from abc import ABC, abstractmethod


class AbstractHandler(ABC):

    @abstractmethod
    def handle_update(self, value):
        pass


class ValueUpdateHandler(AbstractHandler):

    def __init__(self, label: str, value: any):
        self.label = label
        self.value = value

    def handle_update(self, value: any):
        self.value = value
        # send to arduino?
