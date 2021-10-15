import pytest, logging
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets
from ipe_utils.df_utils import df_columns_strip

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def ipe_props():
    load_dotenv()
    envProps: ReadEnvProps =  ReadEnvProps()
    return envProps.get_env_props()

@pytest.fixture
def ipe_workbook(ipe_props):
    GetIPEDataFromSheets(ipe_props)
    return GetIPEDataFromSheets(ipe_props).get_data().get_all_records()
@pytest.fixture
def worksheet_columns():
    return ['Offering Name', 'Offering ID', 'Offering-instance ID', 'Canvas Course ID', 'Year', 'Term', 'UM Term Code', 'udp_term_name', 'Description', 'Lead Faculty Member 1', 'Lead Faculty Member 2', 'Lead Faculty 1 School', 'Lead Faculty 2 School', 'Lead Faculty 1 unique name', 'Lead Faculty 2 unique name', 'Format', 'Instructional Team\n(SEE LOOKUP TABLE)', 'Program offering to students\n(SEE LOOKUP TABLE)', 'Course #s (if applicable)', 'Window used', 'Roles & Responsibilities', 'Interprofessional Communication', 'Teams/Teamwork', 'Values/Ethics', 'Intercultural Humility', 'IPE competency dosage/ Contact Hours', 'Criteria for Assigning Outcomes in Canvas', 'IPE Assessments', 'Notes', 'When does script run? (Feb, June)', 'Script Run?']

def test_worksheet(ipe_workbook):
    assert len(ipe_workbook) == 167

def test_df_column_whitespaces(ipe_workbook, worksheet_columns):
    df = pd.DataFrame(ipe_workbook)
    df_cols_stripped = df_columns_strip(df.columns)
    df.columns = df_cols_stripped
    logging.debug(f'Columns values after stripping: {df.columns}')
    assert list(df.columns) == worksheet_columns
    



