import csv
import json
import os


def json_from_file(path):
    if os.path.exists(path) and os.path.isfile(path) and os.path.getsize(path) > 0:
        with open(path, "r") as data_file:
            return json.load(data_file)
    else:
        raise FileNotFoundError


def csv_from_file(path):
    if os.path.exists(path) and os.path.isfile(path) and os.path.getsize(path) > 0:
        with open(path, "r") as data_file:
            return list(csv.reader(data_file))
    else:
        raise FileNotFoundError
