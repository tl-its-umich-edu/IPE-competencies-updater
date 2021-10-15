import pandas as pd
import logging

logger = logging.getLogger(__name__)

def df_columns_strip(df_columns: pd.Index) -> pd.Index:
    """
    Strip whitespace from column names.
    """
    return df_columns.str.strip()

def df_remove_non_course_id(df_course_id: pd.Series) -> pd.Series:
    """
    Remove irrelevant course IDs from a course ID column.
    """
    return df_course_id.str.replace('-', '')