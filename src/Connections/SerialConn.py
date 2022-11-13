import serial

from src.Connections.AbstractConnection import AbstractConnection


class SerialConn(AbstractConnection):
    def __init__(self):
        self.serial_conn = None
        self.com_port = None
        self.baud_rate = None
        self.timeout = None

    # set up the serial connection
    def setup(self, **kwargs: dict[str, any]):
        self.com_port = kwargs.get("com_port")
        self.baud_rate = kwargs.get("baud_rate")
        self.timeout = kwargs.get("timeout")
        self.serial_conn = serial.Serial(self.com_port, self.baud_rate, timeout=self.timeout)

    # start the serial connection
    def connect(self) -> bool:
        self.serial_conn.open()
        return self.serial_conn.is_open

    # close the serial connection
    def close(self) -> None:
        self.serial_conn.close()

    # check if the serial is connected
    def connected(self) -> bool:
        return self.serial_conn.is_open

    #  send data via serial
    def send(self, payload: str) -> any:
        print(f"sending: {payload}")
        self.serial_conn.write(self.to_bytes(payload + "\n"))  # tack on the newline to trigger the read

    # recv data via serial
    def recv(self) -> str:
        return self.from_bytes(self.serial_conn.readline())

    @staticmethod
    def to_bytes(out_string: str | bytes):
        if isinstance(out_string, str):
            return str.encode(out_string)
        return out_string

    @staticmethod
    def from_bytes(in_bytes: str | bytes):
        if isinstance(in_bytes, bytes):
            return bytes.decode(in_bytes, "utf8")
        return in_bytes
