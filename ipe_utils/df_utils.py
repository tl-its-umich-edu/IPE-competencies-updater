import pandas as pd
import logging

logger = logging.getLogger(__name__)

def df_columns_strip(df_columns: pd.Index) -> pd.Index:
    """
    Strip whitespace from column names.
    """
    return df_columns.str.strip()

def df_remove_non_course_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove non canvas course IDs from a course ID column like Shell, empty space, n/a.
    """
    logging.info(f'{len(df)} rows before removing non course IDs')
    df_with_coursesId = df.loc[df['Canvas Course ID'].apply(pd.to_numeric, errors='coerce').notnull()]
    return df_with_coursesId