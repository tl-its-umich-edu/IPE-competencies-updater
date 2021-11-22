import logging, pytest
from typing import List
import pandas as pd
from ipe_utils.df_utils import df_columns_strip, df_remove_non_course_id, df_filter_course_based_on_month, current_time, df_filter_course_duplicates
from constants import(COL_COURSE_ID, SCRIPT_RUN)
from read_env_props import ReadEnvProps
from ipe_process_orchestrator.orchestrator import IPECompetenciesOrchestrator

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


def test_get_courses_with_month_value_in_when_to_run_column(ipe_ws_df: pd.DataFrame, ipe_props: ReadEnvProps):
    """
    Test to ensure the original and filtered dataframe courses what we expect. The original dataframe has a lot of empty values and we want to ensure that 
    the cleaned up dataframe has no empty values. still should hold all the gsheets data.
    Script run column is not updated
    """
    orc = IPECompetenciesOrchestrator(ipe_props, ipe_ws_df, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.original_df.shape[0] == 16
    assert orc.filter_df_course_ids.shape[0] == 5

def test_get_courses_with_month_value_in_when_to_run_column_and_no_value_script_run(ipe_ws_df: pd.DataFrame, ipe_props: ReadEnvProps):
    """
    Test to ensure the original and filtered dataframe courses what we expect. The original dataframe has a lot of empty values and we want to ensure that 
    the cleaned up dataframe has no empty values. still should hold all the gsheets data.
    Script run column is updated
    """
    now = current_time()
    ipe_ws_df.at[2, SCRIPT_RUN] = now
    ipe_ws_df.at[4, SCRIPT_RUN] = now
    ipe_ws_df.at[6, SCRIPT_RUN] = now
    orc = IPECompetenciesOrchestrator(ipe_props, ipe_ws_df, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.original_df.shape[0] == 16
    assert orc.filter_df_course_ids.shape[0] == 3

def test_courses_qualified_to_run_has_no_duplicate_course_ids(ipe_ws_df: pd.DataFrame, ipe_props: ReadEnvProps):
    """
    This test is to ensure that the courses qualified(based on when to run and script run columns) to run has no duplicate course ids
    """
    now = current_time()
    ipe_ws_df.at[2, SCRIPT_RUN] = now
    ipe_ws_df.at[4, SCRIPT_RUN] = now
    ipe_ws_df.at[6, SCRIPT_RUN] = now
    ipe_ws_df.at[1, COL_COURSE_ID] = 67833444 # assigning duplicate course id from row 0 to row 1 in the dataframe
    orc = IPECompetenciesOrchestrator(ipe_props, ipe_ws_df, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.original_df.shape[0] == 16
    assert orc.filter_df_course_ids.shape[0] == 2

def test_trigger_exception_when_filterning_courses(ipe_props):
    """
    this test will trigger an exception when filtering courses
    """
    with pytest.raises(SystemExit) as e:
        IPECompetenciesOrchestrator(ipe_props, None, None).filter_course_list_to_run_and_cleanup()
    assert e.type == SystemExit
    assert e.value.code == 1

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
    