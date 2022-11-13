import time

from src.Protocols.PacketAckProtocol import PacketAckProtocol
from src.Configuration import AppConfiguration
from src.Connections.SerialConn import SerialConn

debug = True


def to_bytes(string):
    if not isinstance(string, type(b'')):
        return str.encode(string)
    return string


def serial_wait(ser_con, in_recv):
    in_recv = to_bytes(in_recv)
    retry_count = 3
    retry = 0
    while retry < retry_count:
        lines = ser_con.readline()
        if debug and lines:
            print(lines)
        if in_recv in lines:
            return True
        retry += 1
    return False


def serial_writeln(ser_con, write):
    if write.endswith("\n") and len(write) > 1:
        write = write[:-1]
    ser_con.write(to_bytes(f'{write}\n'))


if __name__ == '__main__':
    config = AppConfiguration()

    packetComm = PacketAckProtocol(SerialConn, config.get_comm_config())
    print("holding for boot")
    time.sleep(5)  # boot time


    # connection sequence:
    #   arduino boots and start's listening for a wake signal
    #   monitor sends the wake signal and waits for the acknowledgment signal
    #   Arduino sends the ack and gets ready for commands
    #   monitor receives the ack and sends the load labels command
    #   Monitor sends the labels with the start string, packet, end string then waits for ack
    #   arduino processes the packet and sends the ack string
    #   Monitor receives the ack and starts to wait for polls to request data

    # send wake and wait for ack
    packetComm.start()

    # send the label command and the labels, then wait for the ack
    test_labels = "test 1,test 2,test 3,test 4"
    packetComm.transmit(test_labels, pre_payload="ld_lbls")
    found = packetComm.collect(is_ack=True)

    if found:
        # poll
        print("Done! waiting for poll...")
        while True:
            # found = serial_wait(serial_con, "polling")
            polled = packetComm.collect()
            if polled:
                print("Polled!")
            else:
                print("timed out!")

