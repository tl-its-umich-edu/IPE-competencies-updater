import pytest, logging
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture
def ipe_props():
    load_dotenv()
    envProps: ReadEnvProps =  ReadEnvProps()
    return envProps

def test_worksheet(ipe_props):
    data = GetIPEDataFromSheets(ipe_props.get_env_props())
    assert data.get_data() is not None
    ws = data.get_data()
    assert len(ws.get_all_values()) == 168

