from typing import List
import pytest
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets



pytest_plugins = [
    "tests.fixtures.worksheets_columns"
]

@pytest.fixture(scope="session", autouse=True)
def ipe_props():
    """
    Fixture for Env properties
    """
    load_dotenv()
    envProps: ReadEnvProps =  ReadEnvProps()
    return envProps.get_env_props()

@pytest.fixture(scope="session", autouse=True)
def ipe_workbook(ipe_props)->List[List[str]]:
    """
    fixture for IPE workbook
    """
    GetIPEDataFromSheets(ipe_props)
    ws = GetIPEDataFromSheets(ipe_props).get_data().get_all_records()
    return ws

@pytest.fixture(scope="session", autouse=True)
def ipe_ws_df(ipe_workbook)->pd.DataFrame:
    """
    fixture for sample dataframe
    """
    df = pd.DataFrame(ipe_workbook)
    return df

    


    
   


