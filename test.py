import json
import sys
from z3 import *


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def build_constraints(json_data, s, parent_key=None):
    def add_constraints(key, value):
        full_key = f"{parent_key}_{key}" if parent_key else key

        if isinstance(value, int):
            var = Int(full_key)
            s.add(var == value)
        elif isinstance(value, str):
            var = String(full_key)
            s.add(var == StringVal(value))
        else:
            raise ValueError(f"Unsupported data type for key '{key}'")

        # Example constraints
        if full_key == "database_port":
            s.add(var >= 1024, var <= 65535)
        elif full_key == "api_version":
            s.add(var == StringVal("1.0"))
        elif full_key.endswith("rate_limit"):
            s.add(var > 0)

    for key, value in json_data.items():
        if isinstance(value, dict):
            build_constraints(value, s, parent_key=key)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                item_key = f"{key}_{index}"
                if isinstance(item, dict):
                    build_constraints(item, s, parent_key=item_key)
                else:
                    add_constraints(item_key, item)
        else:
            add_constraints(key, value)


def validate_json(json_data):
    s = Solver()
    build_constraints(json_data, s)
    if s.check() == sat:
        print("JSON validation succeeded")
        return True
    else:
        print("JSON validation failed")
        return False



		
def main():
    # Replace 'config.json' with the path to your JSON file
    json_file = 'config.json'
    json_data = load_json(json_file)

    if validate_json(json_data):
        print("The JSON file meets the specified constraints.")
    else:
        print("The JSON file does not meet the specified constraints.")

if __name__ == "__main__":
    main()
