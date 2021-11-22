import pandas as pd
from datetime import datetime
from constants import (WHEN_TO_RUN_SCRIPT, SCRIPT_RUN, COL_COURSE_ID)
import logging

logger = logging.getLogger(__name__)

def df_columns_strip(df_columns: pd.Index) -> pd.Index:
    """
    Strip whitespace from column names.
    """
    return df_columns.str.strip() #type: ignore

def df_remove_non_course_id(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Remove non canvas course IDs from a course ID column like Shell, empty space, n/a.
    """
    logging.info(f'{len(df)} rows before removing non course IDs')
    df_with_coursesId = df.loc[df['Canvas Course ID'].apply(
        pd.to_numeric, errors='coerce').notnull()]
    return df_with_coursesId

def df_filter_course_based_on_month(df: pd.DataFrame, month: str) -> pd.DataFrame:
    """
    Filter a dataframe based on given month value and script run column is empty .
    """
    return df.loc[(df[WHEN_TO_RUN_SCRIPT]== month ) & (df[SCRIPT_RUN] == '')]

def df_filter_course_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate course id's from a dataframe.
    """
    return df.drop_duplicates(subset=[COL_COURSE_ID])

def current_time()-> str:
    """
    Return current time in format: YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
