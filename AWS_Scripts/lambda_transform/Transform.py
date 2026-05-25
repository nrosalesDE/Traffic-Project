import pandas as pd
import json
import os
import Transform_Functions as tf
import S3_Functions_transform
from pathlib import Path
import logging
import shutil


def Transform_Data(df):
    df = tf.change_data_type(df)
    df = tf.add_date_time_columns(df)
    df = tf.check_for_nulls(df)
    df = tf.filter_out_of_bounds_rows(df)
    df = tf.add_metrics(df)
    df = tf.add_congestion_category(df)
    return df
