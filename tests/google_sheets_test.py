import pytest, json
from unittest.mock import MagicMock, patch
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets 
from gspread.auth import Client
from gspread import Spreadsheet, Worksheet
from gspread.exceptions import APIError
from requests import Response

def test_check_google_service_account_path(ipe_props):
  """
  This tests to check if the google service account path is valid
  """

  with patch('os.path.exists',autospec=True ) as mock_os_path_exist:
    mock_os_path_exist.return_value = False
    with pytest.raises(SystemExit) as pytest_wrapped_e:
      GetIPEDataFromSheets(ipe_props).get_worksheet_instance()
  assert pytest_wrapped_e.type == SystemExit
  assert pytest_wrapped_e.value.code == 1

def test_get_worksheet_data_success_case(ipe_props,spreadsheet, worksheet):
  """
  This tests the success case of getting the worksheet data
  """
  with patch('os.path.exists',autospec=True ) as mock_os_path_exist:
    with patch('gspread.service_account', autospec=True) as mock_gspred_service_account:
      with patch.object(Client, 'open_by_url', autospec=True ) as mock_credentials_open_by_url:
        with patch.object(Spreadsheet, 'worksheet', autospec=True) as mock_gspread_models_worksheet:
            mock_os_path_exist.return_value = True
            mock_gspred_service_account.return_value = Client(None)
            mock_credentials_open_by_url.return_value = spreadsheet
            mock_gspread_models_worksheet.return_value = worksheet
      
            worksheet_data: Worksheet = GetIPEDataFromSheets(ipe_props).get_worksheet_instance()
  assert worksheet_data.title == 'Offerings'

def test_get_worksheet_data_failure_case(ipe_props, spreadsheet):
  """
  This tests the failure case of getting the worksheet data
  """
  response: MagicMock = MagicMock(
        spec=Response,
        status_code=200,
        ok=True,
        text=json.dumps({'success': True}),
        url='http://httpbin.org/get'
    )
  with patch('os.path.exists',autospec=True ) as mock_os_path_exist:
    with patch('gspread.service_account', autospec=True) as mock_gspred_service_account:
      with patch.object(Client, 'open_by_url', autospec=True ) as mock_credentials_open_by_url:
        with patch.object(Spreadsheet, 'worksheet', autospec=True) as mock_gspread_models_worksheet:
            mock_os_path_exist.return_value = True
            mock_gspred_service_account.return_value =  Client(None)
            mock_credentials_open_by_url.return_value = spreadsheet
            mock_gspread_models_worksheet.side_effect = APIError(response)
      
            with pytest.raises(SystemExit) as pytest_wrapped_e:
              GetIPEDataFromSheets(ipe_props).get_worksheet_instance()
  assert pytest_wrapped_e.type == SystemExit
  assert pytest_wrapped_e.value.code == 1
      
      
      
      
      
  


