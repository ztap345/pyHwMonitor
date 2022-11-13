import time
from typing import Type

from src.Configuration import AppConfiguration
from src.Connections.AbstractConnection import AbstractConnection
from src.Connections.SerialConn import SerialConn
from src.Protocols.AbstractProtocol import AbstractProtocol
from src.Protocols.PacketAckProtocol import PacketAckProtocol


class Communicator:
    # STOPPED = "stopped"
    # RUNNING = "running"

    def __init__(self, config: AppConfiguration, protocol: Type[AbstractProtocol], conn: Type[AbstractConnection]):
        self.is_running: bool = False
        self.config: AppConfiguration = config
        self.protocol: AbstractProtocol = protocol(conn, self.config.get_comm_config())
        print("holding for boot")
        time.sleep(2)  # boot time

        # add threading stuff

    def send_command(self, command: str, *data: str) -> bool:
        self.protocol.transmit(*data, pre_payload=command)
        return self.protocol.collect(is_ack=True)

    def start_communication(self):
        self.protocol.start()
        # start threading stuff here?
        self.is_running = True

    def stop_communication(self):
        self.protocol.stop()
        # join threading stuff here?
        self.is_running = False

    # thread "worker"
    def communicate(self):
        while self.is_running:
            polled = self.protocol.collect()
            if polled:
                print("Polled!")
            else:
                print("timed out, blinking")
                self.send_command("blink")


if __name__ == '__main__':
    cfg = AppConfiguration()

    input("press enter to create communications")

    coms = Communicator(cfg, PacketAckProtocol, SerialConn)

    input("press enter to start communications")

    coms.start_communication()

    input("press enter to send the load lables command")

    cmds = cfg.get("commands")
    lbl_cmd = cmds["ld_lbls_cmd"]
    # data_config = cfg.get("display")["data_config"]
    # load_labels = ",".join([data["label"] for data in data_config])
    load_labels = "test 1,test 2,test 3,test 4"
    ack_d = coms.send_command(lbl_cmd, load_labels)

    input("press enter to start waiting for a poll")

    if ack_d:
        try:
            coms.communicate()
        except KeyboardInterrupt:
            coms.stop_communication()
    else:
        print("ack failed")
