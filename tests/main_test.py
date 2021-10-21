import pytest, logging, collections
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets
from ipe_utils.df_utils import df_columns_strip, df_remove_non_course_id
from ipe_process_orchestrator.orchestrator import IPECompetenciesOrchestrator

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
    GetIPEDataFromSheets(ipe_props)
    return GetIPEDataFromSheets(ipe_props).get_data().get_all_records()

def test_df_column_whitespaces(ipe_ws_df, worksheet_columns):
    """
    Testing dataframe columns will always be no leading and trailing whitespaces
    """
    df_cols_stripped = df_columns_strip(ipe_ws_df.columns)
    ipe_ws_df.columns = df_cols_stripped
    logging.debug(f'Columns values after stripping: {ipe_ws_df.columns}')
    assert list(ipe_ws_df.columns) == worksheet_columns

def test_non_course_id_clean_up(ipe_ws_df):
    """
    Test for removing non course id values like Shell, shell, empty string and n/a
    """
    df_after = df_remove_non_course_id(ipe_ws_df)
    course_list_after_clean_up = list(df_after['Canvas Course ID'])
    expected_courses_list_from_clean_up = [354704, 409794, 164232, 249168, 307473, 428719, 436654, 400814, 380026, 380026, 185879, 245116, 320842, 388752, 446527, 259583, 330055, 429486, 302940, 374660, 429487, 142196, 188778, 259583, 330055, 454941, 213167, 258607, 327745, 398001, 153241, 260986, 332108, 352746, 353302, 387122, 321392, 387126, 321395, 16031, 91667, 168143, 244067, 306548, 46007, 128102, 189933, 264044, 342599, 208, 151399, 190685, 269623, 368445, 447150, 429488, 215658, 301269, 374394, 448447, 324934, 302743, 296609, 338775, 414909, 398919, 397302]
    assert 67 == df_after.shape[0]
    assert collections.Counter(expected_courses_list_from_clean_up) == collections.Counter(course_list_after_clean_up)

def test_clean_up_df(ipe_ws_df, ipe_props):
    """
    Test to ensure the original and cleaned up dataframe what we expect. The original dataframe has a lot of empty values and we want to ensure that the cleaned up dataframe has no empty values. still should hold all the gsheets data
    """
    orc = IPECompetenciesOrchestrator(ipe_ws_df, ipe_props)
    orc._clean_up_ipe_dataframe()
    assert orc.orginal_df.shape[0] == 167
    assert orc.filter_df_course_ids.shape[0] == 67
    
   



