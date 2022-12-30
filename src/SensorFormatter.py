from src.utilities import celsius_to_fahrenheit


class SensorFormatter:
    def __init__(self, sensor_type, fahrenheit=False):
        self.fahrenheit = fahrenheit  # temporary, need global type config
        self.sensor_type = sensor_type
        if self.sensor_type == "Voltage":
            self.format_str = "{:.3f} V"
        elif self.sensor_type == "Clock":
            self.format_str = "{:.1f} MHz"
        elif self.sensor_type == "Fan":
            self.format_str = "{:0f} RPM"
        elif self.sensor_type == "Flow":
            self.format_str = "{:.0f} L/h"
        elif self.sensor_type == "Factor":
            self.format_str = "{:.3f}"
        elif self.sensor_type == "Power":
            self.format_str = "{:.1f} W"
        elif self.sensor_type == "Data":
            self.format_str = "{:.1f} GB"
        elif self.sensor_type == "SmallData":
            self.format_str = "{:.1f} MB"
        elif self.sensor_type == "Load" or \
                self.sensor_type == "Control" or \
                self.sensor_type == "Level":
            self.format_str = "{:.2f} %"
        elif self.sensor_type == "Throughput" or self.sensor_type == "Temperature":
            self.format_str = ""  # format is dynamic
        else:
            self.format_str = "{:.2f}"

    def format(self, value: float):
        if self.sensor_type == "Temperature":  # dynamic temp format
            self.format_str = "{:.2f} °"
            if self.fahrenheit:
                self.format_str += "F"
                value = celsius_to_fahrenheit(value)
            else:
                self.format_str += "C"
        elif self.sensor_type == "Throughput":  # dynamic throughput format
            if value < 1:
                value *= 1024  # same as *= 0X400 to convert from MB to KB
                self.format_str = "{:.1f} KB/s"
            else:
                self.format_str = "{:.1f} MB/s"

        return self.format_str.format(value)
