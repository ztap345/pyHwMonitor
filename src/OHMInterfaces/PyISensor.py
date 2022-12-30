from src.OHMInterfaces.PyIHardware import PyIHardware
from src.SensorFormatter import SensorFormatter


class PyISensor:
    def __init__(self, sensor_class):
        self.Hardware: PyIHardware = PyIHardware(sensor_class.get_Hardware())
        self.Identifier: str = sensor_class.Identifier.ToString()
        self.Name: str = sensor_class.get_Name()
        if self.Name != "Load" or self.Name != "Throughput" or not self.Name.__contains__("Data"):
            self.Name += "s"
        if self.Name == "SmallData":
            self.Name = "Data"
        self.Min: float = sensor_class.get_Min()
        self.Max: float = sensor_class.get_Max()
        self.Value: float = sensor_class.get_Value()
        self.SensorType: str = sensor_class.get_SensorType().ToString()
        self.formatter = SensorFormatter(self.SensorType)

    def __str__(self):
        return f"Name: {self.Name}, Identifier:{self.Identifier}, Hardware:({str(self.Hardware)}):" \
               f"\n\tMin:{self.Min}, Max:{self.Max}, Value:{self.Value}, " \
               f"Type:{self.SensorType}"

    def __apply(self, value):
        return self.formatter.format(value) if self.formatter is not None else value

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if isinstance(attr, float):
            return self.__apply(attr)
        return attr

    def get_raw(self, attr: str) -> any:
        return super().__getattribute__(attr)
