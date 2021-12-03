from typing import List
import pytest
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets
from api_handler.api_calls import APIHandler


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

@pytest.fixture(scope="module")
def ipe_workbook(ipe_props) -> List[List[str]]:
    """
    fixture for IPE workbook
    """
    GetIPEDataFromSheets(ipe_props)
    ws = GetIPEDataFromSheets(ipe_props).get_data().get_all_records()
    return ws

@pytest.fixture
def ipe_ws_df(worksheets_data) -> pd.DataFrame:
    """
    fixture for sample dataframe
    """
    df = pd.DataFrame(worksheets_data)
    return df


@pytest.fixture(scope="session")
def api_handler(ipe_props):
    return APIHandler(ipe_props)
