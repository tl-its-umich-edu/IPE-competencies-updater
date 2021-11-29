from typing import List
import pytest
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from api_handler.api_calls import APIHandler
from gspread.models import Worksheet, Spreadsheet
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
    load_dotenv()
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
def worksheet():
    properties = {'sheetId': '12344', 'title': 'Offerings'}
    client = Client(None)
    spreadsheet = Spreadsheet(client, properties)
    return Worksheet(spreadsheet, properties)

@pytest.fixture
def api_handler(ipe_props):
    return APIHandler(ipe_props)
