from typing import Type

from src.Protocols.AbstractProtocol import AbstractProtocol
from src.Connections.AbstractConnection import AbstractConnection


# packet/acknowledgement connection.
# Commands sent in "packets" in the form start_string \n data\n...\n end_string\n
# then an acknowledgement packet is sent
class PacketAckProtocol(AbstractProtocol):

    def __init__(self, connection: Type[AbstractConnection], comm_config: dict):
        """
        A protocol connection that sends packets denoted by a start and end string
        and waits for an acknowledgment string
        Configure the packet acknowledgment protocol with a connection type.
        :param connection: Connection backend to use for communication
        :param comm_config: Configuration for the protocol.
            connection_config: configuration for the specific connection being used
            monitor_config: overall configuration relating to the hw monitor
                retries: how many retries to attempt before failing
                wake_string: string used to start the communication
                start_string: the beginning of a packet
                end_string: the end of a packet
                ack_string: string to listen for
                poll_string: interrupt string used to poll data
        """
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
        self.close_string: str = monitor_config["close_string"]

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
        self.connection.send(self.close_string)
        self.connection.close()

    # see if the connection is up
    def available(self) -> bool:
        return self.connection.connected()

    # send the start and end strings as well as the payload
    def transmit(self, *payload: str, pre_payload: str = None) -> any:
        if pre_payload:
            self.connection.send(pre_payload)
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
