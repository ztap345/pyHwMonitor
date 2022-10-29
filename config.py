import json
import os.path
import re

VAR_REGEX = re.compile(r'\$\{(?P<var>[a-zA-Z_]+)_(?P<c_type>[a-z])}')


def ensure_file(file: str):
    if not os.path.exists(file):
        raise FileNotFoundError(f"File not found at {file}")


class AppConfiguration:

    def __init__(self, cfg_json="config.json"):
        ensure_file(cfg_json)

        with open(cfg_json, "r+") as cfg:
            self.config_dict = json.load(cfg)

    def get_arduino_cfg(self):
        return self.config_dict['arduino_config']

    def get(self, s: str):
        return self.config_dict.get(s)


def convert_type(var, c_type):
    if c_type == "c":
        return f"'{var}'"
    if c_type == "i":
        return int(var)
    if c_type == "s":
        return f'"{var}"'
    return var


def parse_line(line, arduino_cfg):
    for match in re.finditer(VAR_REGEX, line):
        try:
            var = arduino_cfg[match.group("var")]
            replacement = convert_type(var, match.group("c_type"))
            line = line.replace(match.group(), str(replacement))
        except KeyError as ke:
            raise KeyError(f"The key '{match.group('var')}' was missing from arduino_config in "
                           f"config.json, is it missing?") from ke
    return line


def populate_arduino_config(config: AppConfiguration):
    arduino_cfg = config.get_arduino_cfg()
    config_h_template = "Arduino/main/Resources/Config.template.h"
    output_config_h = "Arduino/main/src/ConfigConstants.h"

    ensure_file(config_h_template)

    parsed_lines = []
    with open(config_h_template, "r+") as template:
        while line := template.readline():
            parsed_line = parse_line(line, arduino_cfg)
            parsed_lines.append(parsed_line)

    with open(output_config_h, "w+") as h_file:
        h_file.writelines(parsed_lines)

    ensure_file(output_config_h)


if __name__ == '__main__':
    #TODO: write docs
    test_cfg = AppConfiguration()
    # this is a find_and_replace method
    populate_arduino_config(test_cfg)
