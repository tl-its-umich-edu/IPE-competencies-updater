import pytest, logging, collections
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def ipe_props():
    """
    Fixture for Env properties
    """
    load_dotenv()
    envProps: ReadEnvProps =  ReadEnvProps()
    return envProps.get_env_props()

@pytest.fixture
def ipe_workbook(ipe_props):
    """
    fixture for IPE workbook
    """
    GetIPEDataFromSheets(ipe_props)
    ws = GetIPEDataFromSheets(ipe_props).get_data().get_all_records()
    return ws

@pytest.fixture
def ipe_ws_df(ipe_workbook):
    """
    fixture for sample dataframe
    """
    df = pd.DataFrame(ipe_workbook)
    return df

@pytest.fixture
def worksheet_columns():
    """
    Sample worksheet columns with leading and trailing whitespaces
    """
    return ['Offering Name', 'Offering ID', 'Offering-instance ID', 'Canvas Course ID', 'Year', 'Term', 'UM Term Code', 'udp_term_name', 'Description', 'Lead Faculty Member 1', 'Lead Faculty Member 2', 'Lead Faculty 1 School', 'Lead Faculty 2 School', 'Lead Faculty 1 unique name', 'Lead Faculty 2 unique name', 'Format', 'Instructional Team\n(SEE LOOKUP TABLE)', 'Program offering to students\n(SEE LOOKUP TABLE)', 'Course #s (if applicable)', 'Window used', 'Roles & Responsibilities', 'Interprofessional Communication', 'Teams/Teamwork', 'Values/Ethics', 'Intercultural Humility', 'IPE competency dosage/ Contact Hours', 'Criteria for Assigning Outcomes in Canvas', 'IPE Assessments', 'Notes', 'When does script run? (Feb, June)', 'Script Run?']

def test_worksheet(ipe_workbook):
    """
    Tesing the worksheet return will correct rows
    """
    assert len(ipe_workbook) == 167

    
   



