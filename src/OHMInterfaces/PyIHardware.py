
class PyIHardware:
    def __init__(self, hardware_class):
        self.Identifier = hardware_class.Identifier.ToString()
        self.Parent = hardware_class.Parent
        self.Name = hardware_class.Name

    def __str__(self):
        return f"Name: {self.Name}, Parent:{self.Parent}, Identifier:{self.Identifier}"
