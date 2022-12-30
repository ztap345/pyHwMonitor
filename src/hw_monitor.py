import os
from functools import reduce

import clr

from src.OHMInterfaces.PyIHardware import PyIHardware
from src.OHMInterfaces.PyISensor import PyISensor
from src.utilities import get_nested_item

OHM_NAME = "OpenHardwareMonitorLib.dll"
OHM_PATH = os.path.join(os.getcwd(), OHM_NAME)
if os.path.exists(OHM_PATH):
    clr.AddReference(OHM_PATH)
    # noinspection PyUnresolvedReferences
    from OpenHardwareMonitor import Hardware
else:
    raise FileNotFoundError("Open Hardware Monitor dll was not found")


def convert_to_interface(obj: any) -> PyIHardware | PyISensor:
    if isinstance(obj, Hardware.IHardware):
        return PyIHardware(obj)
    elif isinstance(obj, Hardware.ISensor):
        return PyISensor(obj)


def try_convert_int(val: str) -> int | str:
    try:
        return int(val)
    except ValueError:
        return val


class Monitor:

    def __init__(self):
        self.hw_tree = None
        self.sensor_list = None
        self.computer = Monitor.init_hw_monitor()

        self.update()

    def update(self) -> None:
        self.__load_tree()

    def get_sensor_from_path(self, path: str) -> PyISensor:
        sensor_path = self.split_all_path(path)
        sensor_path.append("__obj__")
        return get_nested_item(self.hw_tree, sensor_path)

    @staticmethod
    def init_hw_monitor(settings: () = ("cpu", "gpu", "mobo", "ram", "storage")):
        # types = Hardware.HardwareType.__dict__
        comp = Hardware.Computer()
        comp.MainboardEnabled = "mobo" in settings
        comp.CPUEnabled = "cpu" in settings
        comp.GPUEnabled = "gpu" in settings
        comp.RAMEnabled = "ram" in settings
        comp.HDDEnabled = "storage" in settings
        comp.Open()
        return comp

    @staticmethod
    def split_path(path: str) -> ():
        if path.startswith("/"):
            path = path[1:]

        split = path.split("/", 1)
        return (try_convert_int(split[0]), split[1]) if len(split) > 1 else (path, None)

    @staticmethod
    def split_all_path(path):
        path_list = []
        branch, rem = Monitor.split_path(path)
        while True:
            path_list.append(branch)
            if rem is None:
                break
            branch, rem = Monitor.split_path(rem)
        return path_list

    @staticmethod
    def add_to_tree(current_branch: dict, obj: Hardware.IHardware | Hardware.ISensor, path: str = None) -> None:
        if path is None:
            path = obj.Identifier.ToString()

        branch, path_remainder = Monitor.split_path(path)
        if branch not in current_branch:
            current_branch[branch] = {}

        if path_remainder is None:
            current_branch[branch]["__obj__"] = convert_to_interface(obj)
        else:
            Monitor.add_to_tree(current_branch[branch], obj, path_remainder)

    def __load_tree(self):
        self.hw_tree = {}
        self.sensor_list = []
        for hw in self.computer.get_Hardware():
            hw.Update()
            # add the hardware
            self.add_to_tree(self.hw_tree, hw)
            # add the sub-hardware
            for sub_hw in hw.get_SubHardware():
                self.add_to_tree(self.hw_tree, sub_hw)
            # add the sensors
            for sensor in hw.get_Sensors():
                self.add_to_tree(self.hw_tree, sensor)
                self.sensor_list.append(sensor.Identifier.ToString())


if __name__ == '__main__':
    hw_monitor = Monitor()
    # print(hw_monitor.computer.GetReport())
    # print(hw_monitor.get_sensor_from_path("/nvidiagpu/0/temperature/0"))
    for sense_path in hw_monitor.sensor_list:
        s = hw_monitor.get_sensor_from_path(sense_path)
        # print(sensor)
        print(s.Hardware.Name, s.Name, s.SensorType)
        print(s.Max)
        print(s.Identifier)
        print()
    # read_times = []
    # data = []
    # num_reads = 10
    # for i in range(num_reads):
    #     start = time.perf_counter_ns()
    #     hw_monitor.update()
    #     data.append(hw_monitor.hw_dict)
    #     read_times.append(time.perf_counter_ns() - start)
    #     # time.sleep(1)
    #
    # total_time_ns = sum(read_times)
    # avg_time_ns = total_time_ns/num_reads
    #
    # print(f"Total time: {total_time_ns/1e9}s")
    # print(f"Avg time: {avg_time_ns/1e9}s")
    #
    # size = get_size(data[0])
    # total_storage = num_reads * size
    # measured_total = sum(map(get_size, data))
    # measured_size = measured_total/len(data)
    #
    # print(f"Singular size: {size} bytes")
    # print(f"{num_reads} object(s) take up: {total_storage} bytes")
    # print(f"measured size: {measured_size} bytes")
    # print(f"measured total: {measured_total} bytes")
    # with open("computer.json", "w+") as f:
    #     json.dump(data[0], f, indent=4)
    # print(json.dumps(data[0], indent=2))
    #
    # print(hw_monitor.get_value_from_path("computer_name"))
    # print(hw_monitor.get_value_from_path("hardware./amdcpu/0.sensors./amdcpu/0/temperature/0.Temperature.value"))
    # print(hw_monitor.get_value_from_path("hardware./nvidiagpu/0.sensors./nvidiagpu/0/temperature/0.Temperature.value"))
