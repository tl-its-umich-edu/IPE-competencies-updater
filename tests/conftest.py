import pytest
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets

@pytest.fixture(scope="session")
def ipe_props():
    """
    Fixture for Env properties
    """
    load_dotenv()
    envProps: ReadEnvProps =  ReadEnvProps()
    return envProps.get_env_props()

@pytest.fixture(scope="session")
def ipe_workbook(ipe_props):
    """
    fixture for IPE workbook
    """
    GetIPEDataFromSheets(ipe_props)
    ws = GetIPEDataFromSheets(ipe_props).get_data().get_all_records()
    return ws

@pytest.fixture(scope="session")
def ipe_ws_df(ipe_workbook):
    """
    fixture for sample dataframe
    """
    df = pd.DataFrame(ipe_workbook)
    return df

@pytest.fixture(scope="session")
def worksheet_columns():
    """
    Sample worksheet columns with leading and trailing whitespaces
    """
    return ['Offering Name', 'Offering ID', 'Offering-instance ID', 'Year', 'Term',
       'UM Term Code', 'udp_term_name', 'Description', 'Lead Faculty Member 1',
       'Lead Faculty Member 2', 'Lead Faculty 1 School',
       'Lead Faculty 2 School', 'Lead Faculty 1 unique name',
       'Lead Faculty 2 unique name', 'Format',
       'Instructional Team (SEE LOOKUP TABLE)',
       'Program offering to students (SEE LOOKUP TABLE)',
       'Course #s (if applicable)', 'Window used', 'IPE Assessments',
       'Canvas Site or Shell Course', 'Canvas Course ID',
       'Roles/ Responsibilities', 'Interprofessional Communication',
       'Teams/Teamwork', 'Values/Ethics', 'Intercultural Humility',
       'Dosage (contact hours)', 'Criteria for Assigning Outcomes in Canvas',
       'Notes', 'When does script run? (Feb, June, Oct)', 'Script Run?']

@pytest.fixture(scope="session")
def worksheet_columns_with_whitespace():
    """
    This test make sure that ipe spread sheets columns whitespaces are trimmed
    """
    return pd.Index(['Offering Name', 'Offering ID', 'Offering-instance ID', 'Year', 'Term ',
       'UM Term Code', 'udp_term_name', 'Description', 'Lead Faculty Member 1',
       'Lead Faculty Member 2', 'Lead Faculty 1 School',
       'Lead Faculty 2 School', 'Lead Faculty 1 unique name',
       'Lead Faculty 2 unique name', 'Format',
       'Instructional Team (SEE LOOKUP TABLE)',
       'Program offering to students (SEE LOOKUP TABLE)',
       'Course #s (if applicable)', 'Window used', 'IPE Assessments',
       'Canvas Site or Shell Course', 'Canvas Course ID',
       'Roles/ Responsibilities ', 'Interprofessional Communication ',
       'Teams/Teamwork ', 'Values/Ethics ', 'Intercultural Humility',
       'Dosage (contact hours) ', 'Criteria for Assigning Outcomes in Canvas',
       'Notes', 'When does script run? (Feb, June, Oct)', 'Script Run?'])
    


    
   


