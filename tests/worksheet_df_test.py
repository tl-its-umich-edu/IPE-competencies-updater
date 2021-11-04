import logging
from typing import List
import pandas as pd
from ipe_utils.df_utils import df_columns_strip, df_remove_non_course_id
from constants import(COL_COURSE_ID)
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


def test_clean_up_df(dummy_df: pd.DataFrame, ipe_props: ReadEnvProps):
    """
    Test to ensure the original and cleaned up dataframe what we expect. The original dataframe has a lot of empty values and we want to ensure that 
    the cleaned up dataframe has no empty values. still should hold all the gsheets data
    """
    orc = IPECompetenciesOrchestrator(ipe_props, dummy_df, None)
    orc._clean_up_ipe_dataframe()
    assert orc.orginal_df.shape[0] == 7
    assert orc.filter_df_course_ids.shape[0] == 5