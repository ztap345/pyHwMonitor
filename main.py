from src.Communicator import Communicator
from src.Configuration import AppConfiguration
from src.Connections.SerialConn import SerialConn
from src.Protocols.PacketAckProtocol import PacketAckProtocol
from src.hw_monitor import Monitor


class Listener:

    def __init__(self, monitor: Monitor, coms: Communicator, paths: list[str], cmd: str):
        self.monitor = monitor
        self.coms = coms
        self.paths = paths
        self.cmd = cmd

    def run(self):
        self.monitor.update()
        values = []
        for i, path in enumerate(self.paths):
            values.append(f"{self.monitor.get_value_from_path(path):.2f} C")
        success = self.coms.send_command(self.cmd, ",".join(values))
        if success:
            print("Sent values!")
        else:
            print("failed!")


if __name__ == '__main__':
    config = AppConfiguration()

    print("loading data")
    cmds = config.get("commands")
    data_config = config.get("display")["data_config"]

    lbl_list = []
    path_list = []
    for p in data_config:
        lbl_list.append(p['label'])
        path_list.append(p['path'])

    print("Starting Monitor")
    hw_monitor = Monitor()
    print("Starting Communicator")
    communicator = Communicator(config, PacketAckProtocol, SerialConn)

    print("Creating listener")
    listener = Listener(hw_monitor, communicator, path_list, cmds['ld_values_cmd'])
    communicator.set_poll_listener(listener)

    print("Connecting and waking")
    communicator.start_communication()

    print("Loading labels")
    labels = ",".join(lbl_list)
    ack_d = communicator.send_command(cmds['ld_lbls_cmd'], labels)

    listener.run()

    print("Waiting for poll")
    try:
        if ack_d:
            communicator._communicate(poll_listener=listener)
        else:
            print("ack failed!")
    except KeyError:
        communicator.stop_communication()

