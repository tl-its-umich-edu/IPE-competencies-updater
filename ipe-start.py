import logging, os
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from gspread.models import Worksheet
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('LOG_LEVEL') if os.getenv('LOG_LEVEL') else 'INFO', format='%(name)s - %(levelname)s - %(message)s')
def main():
    logger.info("IPE Process Starting....")
    envProps: ReadEnvProps =  ReadEnvProps()
    logger.info(envProps.get_env_props())
    ipeData: GetIPEDataFromSheets=GetIPEDataFromSheets(envProps.get_env_props())
    worksheet: Worksheet = ipeData.get_data()
    df = pd.DataFrame(worksheet.get_all_records())
    logger.info(df.head())


if __name__ == '__main__':
    main()