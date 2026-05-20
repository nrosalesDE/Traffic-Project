import pandas as pd
import json
import os


def load_Local_raw_json(data, corridor, Time_ID):

    File_Name = f"{corridor}_{Time_ID}.json"

    file_Path = "C:\GitRepos\Traffic-Project\Data\Raw"

    file_Path = os.path.join(file_Path, File_Name)

    with open(file_Path, "w") as file:
        json.dump(data, file, indent=4)


def load_Local_transformed_Parquet(df, corridor, Time_ID):

    File_Name = f"{corridor}_{Time_ID}.parquet"

    file_Path = "C:\GitRepos\Traffic-Project\Data\Transformed"

    file_Path = os.path.join(file_Path, File_Name)

    df.to_parquet(file_Path, index=False)
