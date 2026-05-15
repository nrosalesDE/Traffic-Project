import pandas as pd
import json
import os


def load_Local(data):
    File_Name = f"Test2.json"

    file_Path = "C:\GitRepos\Traffic-Project\Data\Raw"

    file_Path = os.path.join(file_Path, File_Name)
    with open(file_Path, "w") as file:
        json.dump(data, file, indent=4)
