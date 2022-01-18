from typing import Any, Dict
from unittest import mock
import pytest
import pandas as pd
from unittest.mock import patch
from ipe_utils.df_utils import current_time
from constants import(COL_COURSE_ID, SCRIPT_RUN, WHEN_TO_RUN_SCRIPT ,COL_DOSAGE,
COL_COMPETENCIES_IC, COL_COMPETENCIES_VE, COL_COMPETENCIES_IH, COL_COMPETENCIES_RR, 
COL_COMPETENCIES_TTW, COL_ASSIGNING_LO_CRITERIA)
from read_env_props import ReadEnvProps
from gspread import Worksheet
from ipe_process_orchestrator.orchestrator import IPECompetenciesOrchestrator

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_get_courses_with_month_value_in_when_to_run_column(mock_ws, worksheet: Worksheet, ipe_props: ReadEnvProps, ipe_ws_df: pd.DataFrame):
    """
    Test to ensure the original and filtered dataframe courses what we expect. The original dataframe has a lot of empty values and we want to ensure that 
    the cleaned up dataframe has no empty values. still should hold all the gsheets data.
    Script run column is not updated
    """
    mock_ws.return_value =ipe_ws_df
    orc = IPECompetenciesOrchestrator(ipe_props, worksheet, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.original_df.shape[0] == 16
    assert orc.courses_to_run.shape[0] == 5

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_get_courses_with_month_value_in_when_to_run_column_and_no_value_script_run(mock_ws, worksheet: Worksheet, ipe_ws_df: pd.DataFrame, ipe_props: ReadEnvProps):
    """
    Test to ensure the original and filtered dataframe courses what we expect. The original dataframe has a lot of empty values and we want to ensure that 
    the cleaned up dataframe has no empty values. still should hold all the gsheets data.
    Script run column is updated
    """
    mock_ws.return_value =ipe_ws_df
    now = current_time()
    ipe_ws_df.at[2, SCRIPT_RUN] = now
    ipe_ws_df.at[4, SCRIPT_RUN] = now
    ipe_ws_df.at[6, SCRIPT_RUN] = now
    orc = IPECompetenciesOrchestrator(ipe_props, worksheet, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.original_df.shape[0] == 16
    assert orc.courses_to_run.shape[0] == 3

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_trigger_exception_when_filterning_courses(mock_ws, worksheet: Worksheet, ipe_props):
    """
    this test will trigger an exception when filtering courses
    """
    mock_ws.return_value = None
    with pytest.raises(SystemExit) as e:
        IPECompetenciesOrchestrator(ipe_props, worksheet, None).filter_course_list_to_run_and_cleanup()
    assert e.type == SystemExit
    assert e.value.code == 1

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_no_courses_to_run(mock_ws, worksheet: Worksheet,ipe_ws_df: pd.DataFrame, ipe_props: ReadEnvProps, rubric_simple: Dict[str, Any]):
    """
    This test will ensure that if no courses found/filtered to run based on the script run column logic don't proceed to the next step
    """
    mock_ws.return_value = ipe_ws_df
    with patch.object(IPECompetenciesOrchestrator, 'filter_course_list_to_run_and_cleanup', autospec=True) as mock_empty_filter_df_course_ids:
        with patch.object(IPECompetenciesOrchestrator, 'getting_rubrics', autospec=True) as mock_rubric:
            mock_empty_filter_df_course_ids.return_value = pd.DataFrame()
            mock_rubric.return_value = rubric_simple
            IPECompetenciesOrchestrator(ipe_props, worksheet, None).start_composing_process()
    assert mock_rubric.called == False
    assert mock_empty_filter_df_course_ids.called == True

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_invalid_values_courses_dosage_competencies_criteria(mock_ws, worksheet: Worksheet, 
ipe_props: ReadEnvProps, ipe_ws_comp_df: pd.DataFrame):
    """
    This is testing 
    1. essentials column values for IPE process are there for course id, dosage, competencienc, criteria for assigning
    2. Duplicate course id's are dropped

    """
    mock_ws.return_value = ipe_ws_comp_df
    ipe_ws_comp_df.at[3, COL_COMPETENCIES_IC] = 'happy'
    ipe_ws_comp_df.at[4, COL_COMPETENCIES_VE] = ''
    ipe_ws_comp_df.at[5, COL_COMPETENCIES_IH] = 'do not run'
    ipe_ws_comp_df.at[6, COL_COMPETENCIES_RR] = 'master'
    ipe_ws_comp_df.at[7, COL_COMPETENCIES_TTW] = 'wrong'
    ipe_ws_comp_df.at[8, COL_ASSIGNING_LO_CRITERIA] = 'do not Run'
    ipe_ws_comp_df.at[9, COL_DOSAGE] = 500
    ipe_ws_comp_df.at[10, COL_COURSE_ID] = 12

    orc = IPECompetenciesOrchestrator(ipe_props, worksheet, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.courses_to_run.shape[0] == 6

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_no_courses_to_run_competencies_dosage_course_filtering_works(mock_ws, worksheet: Worksheet, 
ipe_props: ReadEnvProps, ipe_ws_comp_df: pd.DataFrame):
    """
    This is testing when no courses to run all the filtering with invalid values for competencies, dosage and criteria code gracefully handled
    """
    mock_ws.return_value = ipe_ws_comp_df
    ipe_props['script_run_month'] = 'May'
    orc = IPECompetenciesOrchestrator(ipe_props, worksheet, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.courses_to_run.shape[0] == 0
    ipe_props['script_run_month'] = 'June'

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_criteria_to_assign_lo(mock_ws, worksheet: Worksheet, 
ipe_props: ReadEnvProps, ipe_ws_comp_df: pd.DataFrame):
    """
    This is testing when criteria to assign LO is other than 70% and greater or all enrolled those courses are filtered out
    """
    mock_ws.return_value = ipe_ws_comp_df
    ipe_ws_comp_df.at[3, COL_ASSIGNING_LO_CRITERIA] = 'do not run'
    ipe_ws_comp_df.at[5, COL_ASSIGNING_LO_CRITERIA] = 'another random'
    ipe_ws_comp_df.at[7, COL_ASSIGNING_LO_CRITERIA] = 'goal'
    ipe_ws_comp_df.at[6, COL_COMPETENCIES_TTW] = 'wrong'
    orc = IPECompetenciesOrchestrator(ipe_props, worksheet, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.courses_to_run.shape[0] == 11

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_duplicate_rows_with_courses(mock_ws, worksheet: Worksheet, 
ipe_props: ReadEnvProps, ipe_ws_dup_df: pd.DataFrame):
    """
    This is testing when criteria to assign LO is other than 70% and greater or all enrolled those courses are filtered out
    """
    mock_ws.return_value = ipe_ws_dup_df
    orc = IPECompetenciesOrchestrator(ipe_props, worksheet, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.courses_to_run.shape[0] == 3


