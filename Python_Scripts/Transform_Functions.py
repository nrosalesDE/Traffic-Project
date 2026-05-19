import pandas as pd
import logging
import os

logging.basicConfig(
    filename='Transform.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)


def change_data_type(df):
    logging.info("Changing data types for numeric columns.")
    numeric_columns = ["Current_Speed", "Free_Flow_Speed",
                       "Current_Travel_Time", "Free_Flow_Travel_Time", "Confidence"]
    try:
        df[numeric_columns] = df[numeric_columns].apply(
            pd.to_numeric, errors='coerce')
        logging.info("Numeric columns converted successfully.")
    except Exception as e:
        logging.error(f"Error converting numeric columns: {e}")
    return df


def add_date_time_columns(df):
    logging.info("Adding date time columns to the dataframe.")
    df['Date_Time'] = pd.to_datetime(df['Time_ID'], format='%Y%m%d%H%M')
    df['Year'] = df['Date_Time'].dt.year
    logging.info("Year column added successfully.")
    df['Month'] = df['Date_Time'].dt.month
    logging.info("Month column added successfully.")
    df['Day'] = df['Date_Time'].dt.day
    logging.info("Day column added successfully.")
    df['Hour'] = df['Date_Time'].dt.hour
    logging.info("Hour column added successfully.")
    df['Minute'] = df['Date_Time'].dt.minute
    logging.info("Minute column added successfully.")
    return df


def check_for_nulls(df):
    required_columns = ["Point_ID", "Time_ID", "Current_Speed",
                        "Free_Flow_Speed", "Current_Travel_Time", "Free_Flow_Travel_Time",]
    logging.info("Checking for nulls in the dataframe.")
    try:
        invalid_rows = df[df[required_columns].isnull().any(axis=1)]
        logging.info(f" {len(invalid_rows)} nulls found in the dataframe.")
    except Exception as e:
        logging.error(f"Error checking for nulls: {e}")

    if not invalid_rows.empty:
        File_Name = f"{df['Corridor'].iloc[0]}_{df['Time_ID'].iloc[0]}_invalid_rows.csv"
        file_Path = "C:/GitRepos/Traffic-Project/Data/Errors"
        file_Path = os.path.join(file_Path, File_Name)
        invalid_rows.to_csv(file_Path, index=False)
        logging.info(f"Invalid rows saved to {file_Path}.")
    df = df.dropna()

    logging.info(f"{len(invalid_rows)} rows removed from the dataframe.")

    return df


def filter_out_of_bounds_rows(df):
    logging.info("Starting filter_out_of_bounds_rows function.")
    # Define bounds for each column
    bounds = {
        "Current_Speed": (0, 120),
        "Free_Flow_Speed": (0, 120),
        "Current_Travel_Time": (0, 300),
        "Free_Flow_Travel_Time": (0, 300),
        "Confidence": (0, 1)
    }

    invalid_rows = pd.DataFrame()
    df_filtered = df.copy()
    logging.info("Applying bounds to columns.")

    for col, (lower, upper) in bounds.items():
        logging.info(
            f"Checking column '{col}' for out-of-bounds values <{lower} or >{upper}.")
        # Identify invalid rows for this column
        invalid = df_filtered[(df_filtered[col] < lower) |
                              (df_filtered[col] > upper)]
        if not invalid.empty:
            logging.info(
                f"Found {len(invalid)} invalid rows in column '{col}'.")
            invalid_rows = pd.concat([invalid_rows, invalid])
        # Filter out invalid rows for this column
        df_filtered = df_filtered[(df_filtered[col] >= lower)
                                  & (df_filtered[col] <= upper)]
        logging.info(
            f"Filtered dataframe now has {len(df_filtered)} rows after checking '{col}'.")

    if not invalid_rows.empty:
        logging.info(
            f"Total invalid (out-of-bounds) rows found: {len(invalid_rows)}")
        corridor = df['Corridor'].iloc[0] if 'Corridor' in df.columns else 'UnknownCorridor'
        time_id = df['Time_ID'].iloc[0] if 'Time_ID' in df.columns else 'UnknownTime'
        file_name = f"{corridor}_{time_id}_out_of_bounds_rows.csv"
        error_path = os.path.join(
            "C:/GitRepos/Traffic-Project/Data/Errors", file_name)
        invalid_rows.to_csv(error_path, index=False)
        logging.info(f"Out-of-bounds rows saved to {error_path}")

        return df_filtered


def add_metrics(df):
    import logging
    logging.info("Starting add_metrics function.")
    before_cols = set(df.columns)
    df['Speed_Difference'] = df['Current_Speed'] - df['Free_Flow_Speed']
    logging.info("Calculated Speed_Difference column.")
    df['Travel_Time_Difference'] = df['Current_Travel_Time'] - \
        df['Free_Flow_Travel_Time']
    logging.info("Calculated Travel_Time_Difference column.")
    df['Congestion_Ratio'] = df['Speed_Difference'] / df['Free_Flow_Speed']
    logging.info("Calculated Congestion_Ratio column.")
    df['Rush_Hour'] = df['Hour'].isin([6, 7, 8, 9, 16, 17, 18])
    logging.info("Calculated Rush_Hour column.")
    df['Day_of_Week'] = df['Date_Time'].dt.day_name()
    logging.info("Added Day_of_Week column.")
    df['Weekend'] = df['Day_of_Week'].isin(['Saturday', 'Sunday'])
    logging.info("Added Weekend column.")
    after_cols = set(df.columns)
    new_metrics = list(after_cols - before_cols)
    logging.info(f"add_metrics added columns: {new_metrics}")
    return df


def add_congestion_category(df):
    import logging
    logging.info("Starting add_congestion_category function.")

    def categorize(row):
        if row["Road_Closure"] == True:
            return "Closure"
        elif row["Congestion_Ratio"] >= 1.5:
            return "Heavy"
        elif row["Congestion_Ratio"] >= 1.2:
            return "Moderate"
        else:
            return "Normal"

    df["Congestion_Category"] = df.apply(categorize, axis=1)
    logging.info(
        f"Added 'Congestion_Category' column to dataframe. Example categories: {df['Congestion_Category'].value_counts().to_dict()}")
    return df
