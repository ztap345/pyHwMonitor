from typing import Type

from src.Communicator.AbstractCommunicator import AbstractCommunicator
from src.Connections.AbstractConnection import AbstractConnection


# packet/acknowledgement connection.
# Commands sent in "packets" in the form start_string \n data\n...\n end_string\n
# then an acknowledgement packet is sent
class PacketAckComm(AbstractCommunicator):

    def __init__(self, connection: Type[AbstractConnection], comm_config: dict):
        self.comm_config: dict = comm_config

        self.connection: AbstractConnection = connection()
        self.connection.setup(**comm_config["connection_config"])

        monitor_config: dict = comm_config["monitor_config"]
        self.retires: int = monitor_config["retries"]
        self.wake_string: str = monitor_config["wake_string"]
        self.start_string: str = monitor_config["start_string"]
        self.end_string: str = monitor_config["end_string"]
        self.ack_string: str = monitor_config["ack_string"]
        self.poll_string: str = monitor_config["poll_string"]

    # wake string
    def start(self):
        while True:
            print(f"Sending wake signal: {self.wake_string}")
            self.connection.send(self.wake_string)
            print("Waiting for wake signal ack")
            found = self.collect(is_ack=True)
            if found:
                break

    # stop the connection
    def stop(self):
        self.connection.close()

    # see if the connection is up
    def available(self) -> bool:
        return self.connection.connected()

    # send the start and end strings as well as the payload
    def transmit(self, *payload: str, command: str = None) -> any:
        if command:
            self.connection.send(command)
        self.connection.send(self.start_string)
        for data in payload:
            self.connection.send(data)
        self.connection.send(self.end_string)

    # method to wait. True is wait for the ack string else wait for end_string
    def collect(self, is_ack: bool = False) -> bool:
        # retry and fail here
        find_me = self.ack_string if is_ack else self.poll_string
        retry_count = 0
        while True:
            received_line = self.connection.recv()
            if received_line:
                print(received_line)
            if find_me in received_line:
                return True
            if retry_count == self.retires:
                return False

            retry_count += 1
