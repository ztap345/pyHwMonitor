import serial

from config import AppConfiguration

debug = True


def to_bytes(string):
    if not isinstance(string, type(b'')):
        return str.encode(string)
    return string


def serial_wait(ser_con, in_recv):
    in_recv = to_bytes(in_recv)

    while True:
        lines = ser_con.readline()
        if debug and lines:
            print(lines)
        if in_recv in lines:
            break


def serial_writeln(ser_con, write):
    if write.endswith("\n") and len(write) > 1:
        write = write[:-1]
    ser_con.write(to_bytes(f'{write}\n'))


if __name__ == '__main__':
    config = AppConfiguration()
    arduino_cfg = config.get_arduino_cfg()

    baud_rate = arduino_cfg['baud_rate']
    com_port = config.get('port')

    serial_con = serial.Serial(com_port, baud_rate)
    while True:
        print("Waiting for wake signal")
        serial_wait(serial_con, arduino_cfg['wait_text'])
        print("Wake signal found!")

        input("Press Enter to Start...")
        serial_writeln(serial_con, arduino_cfg['start_suffix'])
        serial_wait(serial_con, arduino_cfg['ready_char'])

        while (user := input("send a string to arduino: ")) != f"{arduino_cfg['stop_char']}":
            serial_writeln(serial_con, user)
            serial_wait(serial_con, arduino_cfg['ready_char'])

        if input("Would you like to listen again? (y/n)") not in ['n', 'N']:
            break

