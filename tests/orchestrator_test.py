from typing import Any, Dict
from unittest import mock
import pytest
import pandas as pd
from unittest.mock import patch
from ipe_utils.df_utils import current_time
from constants import(COL_COURSE_ID, SCRIPT_RUN)
from read_env_props import ReadEnvProps
from gspread import Worksheet, Spreadsheet
from gspread.auth import Client
from ipe_process_orchestrator.orchestrator import IPECompetenciesOrchestrator

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_competancies_values_not_empty(mock_ws, single_ipe_offering, ipe_props, api_handler, ipe_ws_df, worksheet):
    """
    This tests if the competancies values are not empty
    """
    single_ipe_offering['Dosage (contact hours)'] = ''
    single_ipe_offering['Intercultural Humility'] = ''
    single_ipe_offering['Interprofessional Communication'] = ''
    single_ipe_offering['Roles/Responsibilities'] = ''
    single_ipe_offering['Team/Teamwork'] = 'Introduce'
    single_ipe_offering['Values/Ethics'] = ''
    single_ipe_offering['COL_ASSIGNING_LO_CRITERIA'] = ''
    course = pd.Series(single_ipe_offering)
    mock_ws.return_value =ipe_ws_df
    check_status = IPECompetenciesOrchestrator(ipe_props, worksheet, api_handler).check_competencies_values_given_gsheet(course)
    assert check_status == False

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
    assert orc.filter_df_course_ids.shape[0] == 5

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
    assert orc.filter_df_course_ids.shape[0] == 3

@mock.patch('gspread.Worksheet.get_all_records', autospec=True)
def test_courses_qualified_to_run_has_no_duplicate_course_ids(mock_ws, worksheet: Worksheet, ipe_ws_df: pd.DataFrame, ipe_props: ReadEnvProps):
    """
    This test is to ensure that the courses qualified(based on when to run and script run columns) to run has no duplicate course ids
    """
    mock_ws.return_value = ipe_ws_df
    now = current_time()
    ipe_ws_df.at[2, SCRIPT_RUN] = now
    ipe_ws_df.at[4, SCRIPT_RUN] = now
    ipe_ws_df.at[6, SCRIPT_RUN] = now
    ipe_ws_df.at[1, COL_COURSE_ID] = 67833444 # assigning duplicate course id from row 0 to row 1 in the dataframe
    orc = IPECompetenciesOrchestrator(ipe_props, worksheet, None)
    orc.filter_course_list_to_run_and_cleanup()
    assert orc.original_df.shape[0] == 16
    assert orc.filter_df_course_ids.shape[0] == 2

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
