from typing import Dict
import pandas as pd
from typing import Dict
from gspread import Cell
from unittest import mock
from unittest.mock import  MagicMock, patch
from ipe_process_orchestrator.update_process_done import UpdateProcessDone
from requests import Response
from gspread.exceptions import APIError

@mock.patch('gspread.Worksheet.findall', side_effect=[[Cell(1, 28,'Script Run?')], [Cell(12, 28,'222222')]])
@mock.patch('gspread.Worksheet.update_cells', return_value={'spreadsheetId': '1tQoEdYt',
'updatedRange': 'Offerings!AF2:AF165','updatedRows': 1,'updatedColumns': 1,'updatedCells': 1})
def test_update_process_success_case(mock_uc: MagicMock, mock_fa: MagicMock, ipe_props,single_ipe_offering,worksheet):
  """
  This will test read/write operation on google sheets is successful
  """
  course = pd.Series(single_ipe_offering)
  UpdateProcessDone(ipe_props,course,worksheet, 20).update_process_run_finished()
  mock_fa.assert_called_once()
  mock_uc.assert_called_once()
 
def test_update_process_read_operation_google_sheet_failure_case(ipe_props: Dict,single_ipe_offering,worksheet):
  """
  This will test read operation to google sheets is failed
  """
  response: MagicMock = MagicMock(
        spec=Response,
        text='rate_limt_exceeded',
    )
  course = pd.Series(single_ipe_offering)
  ipe_props.update({'wait_limit': '1'})
  with patch('gspread.Worksheet.findall') as mock_find:
    mock_find.side_effect = [APIError(response), APIError(response), APIError(response)]
    UpdateProcessDone(ipe_props,course,worksheet, 20).update_process_run_finished()
  mock_find.call_count == 3

@mock.patch('gspread.Worksheet.findall', side_effect=[[Cell(1, 28,'Script Run?')], [Cell(12, 28,'222222')]])
def test_update_process_write_operation_google_sheet_failure_case(ipe_props: Dict, single_ipe_offering, worksheet):
    
  """
  This will test write operation to google sheets is failed
  """
  response: MagicMock = MagicMock(
        spec=Response,
        text='rate_limt_exceeded',
    )
  course = pd.Series(single_ipe_offering)
  ipe_props.update({'wait_limit': '1'})
  with patch('gspread.Worksheet.update_cells') as mock_write:
    mock_write.side_effect = [APIError(response), APIError(response), APIError(response)]
    UpdateProcessDone(ipe_props,course,worksheet, 20).update_process_run_finished()
  mock_write.call_count == 3

@mock.patch('gspread.Worksheet.findall', side_effect=[[Cell(1, 28,'Script Run?')], [Cell(12, 28,'222222')]])
@mock.patch('gspread.Worksheet.update_cells', return_value={'spreadsheetId': '1tQoEdYt',
'updatedRange': 'Offerings!AF2:AF165','updatedRows': 1,'updatedColumns': 1,'updatedCells': 1})
def test_script_run_column_value_not_given(mock_update: MagicMock, mock_findall: MagicMock, ipe_props: Dict, single_ipe_offering, worksheet):
  """
  This will test script run column value is not given
  """
  course = pd.Series(single_ipe_offering)
  ipe_props.update({'wait_limit': '1'})
  UpdateProcessDone(ipe_props,course,worksheet, None).update_process_run_finished()
  mock_findall.call_count == 2
  mock_update.assert_called_once()