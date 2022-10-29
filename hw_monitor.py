import copy
import json
import os
import pickle
import time

import clr

from UpdateHandler import PathUpdateHandler
from utilities import get_nested_item

OHM_NAME = "OpenHardwareMonitorLib.dll"
OHM_PATH = os.path.join(os.getcwd(), OHM_NAME)
if os.path.exists(OHM_PATH):
    clr.AddReference(OHM_PATH)
    # noinspection PyUnresolvedReferences
    from OpenHardwareMonitor import Hardware
else:
    raise FileNotFoundError("Open Hardware Monitor dll was not found")


# schema:
#   {
#       "computer_name": "my_pc",
#       "hardware":
#       {
#           "$hardware.Identifier"{
#               "name": "",
#               "type": "",
#               "sensors":{
#               "${sensor.Identifier}":{
#                   "name":"",
#                   "${sensor.Type}: {
#                       "min": "",
#                       "max": "",
#                       "value": ""
#                       }
#                   }
#               },
#               "hardware":{
#                   # this is the sub_hardware if it exists, pattern repeats here
#               }
#           },
#           ...
#       },
#       ...
#   }

def get_size(o):
    return len(pickle.dumps(o))


class Monitor:

    def __init__(self):
        self.computer = Monitor.init_hw_monitor()
        self.handlers = {}
        self.hw_dict = self.__load_hw_dict()

    def update(self):
        new_hw_dict = self.__load_hw_dict()
        if new_hw_dict == self.hw_dict:
            return

        self.hw_dict = new_hw_dict
        for path, handler in self.handlers.items():
            handler.update(self.get_value_from_path(path))

    def register(self, handler: PathUpdateHandler, path: str):
        self.handlers[path] = handler

    def get_value_from_path(self, path: str):
        path_list = Monitor.split_path(path)
        return get_nested_item(self.hw_dict, path_list)

    def __load_hw_dict(self):
        return Monitor.load_computer(self.computer.get_Hardware())

    @staticmethod
    def split_path(path: str):
        return path.split(".")

    @staticmethod
    def __get_copy(choice):
        if choice == "computer":
            return copy.deepcopy({"computer_name": os.environ['COMPUTERNAME'], "hardware": {}})  # computer_start_dict
        if choice == "hardware":
            return copy.deepcopy({"name": None, "type": None, "sensors": {}})  # hardware_start_dict
        if choice == "sensor":
            return copy.deepcopy({"name": None})  # sensor_start_dict
        if choice == "sensor_type":
            return copy.deepcopy({"min": None, "max": None, "value": None})  # sensor_type_start_dict

    @staticmethod
    def init_hw_monitor():
        comp = Hardware.Computer()
        comp.MainboardEnabled = True
        comp.CPUEnabled = True
        comp.GPUEnabled = True
        comp.RAMEnabled = True
        comp.HDDEnabled = True
        comp.Open()
        return comp

    @staticmethod
    def load_sensor_type(sensor):
        sensor_type = Monitor.__get_copy("sensor_type")
        sensor_type["min"] = sensor.Min
        sensor_type["max"] = sensor.Max
        sensor_type["value"] = sensor.Value
        return sensor_type

    @staticmethod
    def load_hardware(hw):
        hw_dict = Monitor.__get_copy("hardware")

        hw_dict["name"] = hw.Name
        hw_dict["type"] = str(hw.HardwareType)
        for sensor in hw.Sensors:
            s_id = str(sensor.Identifier)
            s_type = str(sensor.SensorType)
            if s_id not in hw_dict["sensors"]:
                new_sensor = Monitor.__get_copy("sensor")
                new_sensor["name"] = sensor.Name
                new_sensor[s_type] = Monitor.load_sensor_type(sensor)
                hw_dict["sensors"][s_id] = new_sensor
            else:
                hw_dict["sensors"][s_id][s_type] = Monitor.load_sensor_type(sensor)

        for sub_hw in hw.SubHardware:
            hw_dict[str(sub_hw.Identifier)] = Monitor.load_hardware(sub_hw)

        return hw_dict

    @staticmethod
    def load_computer(hw_list):
        comp_dict = Monitor.__get_copy("computer")

        for hw in hw_list:
            hw.Update()
            comp_dict['hardware'][str(hw.Identifier)] = Monitor.load_hardware(hw)

        return comp_dict


if __name__ == '__main__':
    hw_monitor = Monitor()
    read_times = []
    data = []
    num_reads = 10
    for i in range(num_reads):
        start = time.perf_counter_ns()
        hw_monitor.update()
        data.append(hw_monitor.hw_dict)
        read_times.append(time.perf_counter_ns() - start)
        # time.sleep(1)

    total_time_ns = sum(read_times)
    avg_time_ns = total_time_ns/num_reads

    print(f"Total time: {total_time_ns/1e9}s")
    print(f"Avg time: {avg_time_ns/1e9}s")

    size = get_size(data[0])
    total_storage = num_reads * size
    measured_total = sum(map(get_size, data))
    measured_size = measured_total/len(data)

    print(f"Singular size: {size} bytes")
    print(f"{num_reads} object(s) take up: {total_storage} bytes")
    print(f"measured size: {measured_size} bytes")
    print(f"measured total: {measured_total} bytes")
    with open("computer.json", "w+") as f:
        json.dump(data[0], f, indent=4)
    print(json.dumps(data[0], indent=2))

    print(hw_monitor.get_value_from_path("computer_name"))
    print(hw_monitor.get_value_from_path("hardware./amdcpu/0.sensors./amdcpu/0/temperature/0.Temperature.value"))
    print(hw_monitor.get_value_from_path("hardware./nvidiagpu/0.sensors./nvidiagpu/0/temperature/0.Temperature.value"))
