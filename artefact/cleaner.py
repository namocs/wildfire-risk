"""
File: cleaner.py

About: This code will clean all the data inside the json files  and csv files stored in the 
       data folder this is primarly used when I'm debugging.
"""
import os
import json
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, "data/csv")
JSON_DIR = os.path.join(BASE_DIR, "data/json")


def reset_csv(path):
    with open(path, "r") as f:
        header = f.readline()
    with open(path, "w") as f:
        f.write(header)
    print(f"Reset: Cleared {os.path.basename(path)}")


def reset_json(path):
    with open(path, "w") as f:
        json.dump([], f)
    print(f"Reset: Cleared {os.path.basename(path)}")


def run():
    print("Cleaning Data!!!!!")

    # Clear all CSVs
    for path in glob.glob(os.path.join(CSV_DIR, "*.csv")):
        reset_csv(path)

    # Clear all JSONs
    for path in glob.glob(os.path.join(JSON_DIR, "*.json")):
        reset_json(path)

    print("DONE")


if __name__ == "__main__":
    run()