import logging, pytest
from typing import List
import pandas as pd
from ipe_utils.df_utils import df_columns_strip, df_remove_non_course_id, df_filter_course_based_on_month, current_time, df_filter_course_duplicates
from constants import(COL_COURSE_ID, SCRIPT_RUN)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def test_df_column_whitespaces(worksheet_columns_with_whitespace: pd.Index, worksheet_columns: List):
    """
    Testing dataframe columns will always be no leading and trailing whitespaces
    """
    df_cols_stripped: pd.Index = df_columns_strip(
        worksheet_columns_with_whitespace)
    assert list(df_cols_stripped) == worksheet_columns


def test_non_course_id_clean_up(ipe_ws_df: pd.DataFrame):
    """
    Test for removing non course id values like Shell, shell, empty string and n/a courses are only id's
    """
    df_after: pd.DataFrame = df_remove_non_course_id(ipe_ws_df)
    course_list_after_clean_up: List = list(df_after[COL_COURSE_ID])
    assert(all(isinstance(x, int) for x in course_list_after_clean_up))

def test_filter_courses_to_run(ipe_ws_df: pd.DataFrame):
    """
    this will get courses to run for a given month and Script run column not updated
    """
    df_actual = df_filter_course_based_on_month(ipe_ws_df, 'June')
    assert df_actual.shape[0] == 7

def test_filter_courses_with_few_script_run_values(ipe_ws_df: pd.DataFrame):
    """
    courses are filtered based on Month and Script run column updated. this test is making sure that the courses already ran is not picked up 
    """
    now = current_time()
    ipe_ws_df.at[2, SCRIPT_RUN] = now
    ipe_ws_df.at[4, SCRIPT_RUN] = now
    ipe_ws_df.at[6, SCRIPT_RUN] = now
    df_actual = df_filter_course_based_on_month(ipe_ws_df, 'June')
    assert df_actual.shape[0] == 4

def test_duplicate_course_ids_removed(dummy_df: pd.DataFrame):
    """
    duplicate course ids are removed from the dataframe
    """
    df_actual = df_filter_course_duplicates(dummy_df)
    assert df_actual.shape[0] == 7
    