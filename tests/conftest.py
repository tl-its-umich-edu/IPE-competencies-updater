from typing import List
from unittest import mock
import pytest, os
import pandas as pd
from dotenv import load_dotenv
from unittest.mock import patch
from read_env_props import ReadEnvProps
from api_handler.api_calls import APIHandler
from gspread import Worksheet, Spreadsheet
from gspread.auth import Client

# These are test specific to a particular test module
pytest_plugins = [
    "tests.fixtures.worksheets_columns",
    "tests.fixtures.dataframe_fake",
    "tests.fixtures.rubric_simplified_obj",
    "tests.fixtures.competencies_data"
]


#  session scoped will be used for until the tear down of the test. Props, worksheets and dataframes common to all tests
@pytest.fixture(scope="session")
def ipe_props():
    """
    Fixture for Env properties
    """
    ENV_PATH: str = print('Please set set the Env file path') if os.getenv('IPE_ENV_FILE') is None else os.getenv('IPE_ENV_FILE') 
    load_dotenv(dotenv_path=ENV_PATH, verbose=True)
    # load_dotenv()
    envProps: ReadEnvProps = ReadEnvProps()
    return envProps.get_env_props()

@pytest.fixture
def ipe_ws_df(worksheets_data) -> pd.DataFrame:
    """
    fixture for sample dataframe
    """
    df = pd.DataFrame(worksheets_data)
    return df

@pytest.fixture
@mock.patch('gspread.Spreadsheet.fetch_sheet_metadata')
def spreadsheet(moch_ws):
    properties = {'sheetId': '12344', 'title': 'Offerings'}
    client = Client(None)
    moch_ws.return_value = {"properties": {'title': 'Master Spreadsheet', 'locale': 'en_US', 'autoRecalc': 'ON_CHANGE', 'timeZone': 'America/Detroit', 
    'defaultFormat': {'backgroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'padding': {'top': 2, 'right': 3, 'bottom': 2, 'left': 3}}}}
    return Spreadsheet(client, properties)
    
@pytest.fixture
def worksheet(spreadsheet):
    properties = {'id': '12344', 'title': 'Offerings'}
    return Worksheet(spreadsheet, properties)

@pytest.fixture
def api_handler(ipe_props):
    return APIHandler(ipe_props)
