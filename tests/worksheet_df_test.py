import logging, pytest
from typing import List
import pandas as pd
from ipe_utils.df_utils import (df_columns_strip, df_remove_non_course_id, df_filter_course_based_on_month, 
current_time, df_filter_course_duplicates, df_dosage_clean_up, df_filter_courses_no_competencies_dosage_criteria_values)
from constants import(COL_COURSE_ID, SCRIPT_RUN, WHEN_TO_RUN_SCRIPT ,COL_DOSAGE,
COL_COMPETENCIES_IC, COL_COMPETENCIES_VE, COL_COMPETENCIES_IH, COL_COMPETENCIES_RR, 
COL_COMPETENCIES_TTW, COL_ASSIGNING_LO_CRITERIA)

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

    ipe_ws_df.at[2, WHEN_TO_RUN_SCRIPT] = 'JUNE'
    ipe_ws_df.at[4, WHEN_TO_RUN_SCRIPT] = 'june'
    ipe_ws_df.at[6, WHEN_TO_RUN_SCRIPT] = 'JUne'
    df_actual = df_filter_course_based_on_month(ipe_ws_df, 'JuNe')
    assert df_actual.shape[0] == 7

def test_filter_courses_with_few_script_run_values(ipe_ws_df: pd.DataFrame):
    """
    courses are filtered based on Month and Script run column updated. this test is making sure that the courses already ran is not picked up 
    """
    now = current_time()
    ipe_ws_df.at[2, SCRIPT_RUN] = 'JUNE'
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
    assert df_actual.shape[0] == 6

def test_filter_course_based_on_month_with_extra_spaces(ipe_ws_df: pd.DataFrame):
    """
    test for filtering courses based on month value with extra spaces
    """
    ipe_ws_df.at[2, WHEN_TO_RUN_SCRIPT] = ' JUNE '
    ipe_ws_df.at[4, WHEN_TO_RUN_SCRIPT] = '  june'
    ipe_ws_df.at[6, WHEN_TO_RUN_SCRIPT] = 'JUne  '
    df_actual = df_filter_course_based_on_month(ipe_ws_df, '  june  ')
    assert df_actual.shape[0] == 7

def test_dosage_correct_values(ipe_ws_comp_df: pd.DataFrame):
    """
    This is testing dosage is picking up only numeric values and inbetween 0 and 100
    """
    ipe_ws_comp_df.at[3, COL_DOSAGE] = 100
    ipe_ws_comp_df.at[4, COL_DOSAGE] = 0
    ipe_ws_comp_df.at[5, COL_DOSAGE] = 200.7
    ipe_ws_comp_df.at[6, COL_DOSAGE] = 400
    ipe_ws_comp_df.at[7, COL_DOSAGE] = 'don not pick up'
    ipe_ws_comp_df.at[8, COL_DOSAGE] = 'n/a'
    df_actual_non_number_filter = df_dosage_clean_up(ipe_ws_comp_df)
    assert df_actual_non_number_filter.shape[0] == 11

def test_competencies_criteria_lo_assigning_correctness(ipe_ws_comp_df: pd.DataFrame):
    """
    This is testing competencies, criteria assigning, dosage values are as expected
    """
    ipe_ws_comp_df.at[3, COL_COMPETENCIES_IC] = 'happy'
    ipe_ws_comp_df.at[4, COL_COMPETENCIES_VE] = ''
    ipe_ws_comp_df.at[5, COL_COMPETENCIES_IH] = 'do not run'
    ipe_ws_comp_df.at[6, COL_COMPETENCIES_RR] = 'master'
    ipe_ws_comp_df.at[7, COL_COMPETENCIES_TTW] = 'wrong'
    ipe_ws_comp_df.at[8, COL_ASSIGNING_LO_CRITERIA] = 'do not Run'
    ipe_ws_comp_df.at[9, COL_DOSAGE] = 500

    df_actual = df_filter_courses_no_competencies_dosage_criteria_values(ipe_ws_comp_df)
    assert df_actual.shape[0] == 8

    