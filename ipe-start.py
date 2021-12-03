import logging, os
from typing import Dict, Optional
import pandas as pd
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from gspread.models import Worksheet
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets
from ipe_process_orchestrator.orchestrator import IPECompetenciesOrchestrator
from api_handler.api_calls import APIHandler

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('LOG_LEVEL') if os.getenv('LOG_LEVEL') else 'INFO', format='%(name)s - %(levelname)s - %(message)s')

def main():
    logger.info("IPE Process Starting....")
    props: Dict[str, Optional[str]] =  ReadEnvProps().get_env_props()
    ipeData: GetIPEDataFromSheets = GetIPEDataFromSheets(props)
    worksheet: Worksheet = ipeData.get_data()
    worksheet_dataframe: pd.DataFrame  = pd.DataFrame(worksheet.get_all_records())
    api_handler: APIHandler = APIHandler(props)
    orchestrator: IPECompetenciesOrchestrator = IPECompetenciesOrchestrator(props, worksheet_dataframe, api_handler)
    orchestrator.start_composing_process()

    logger.info(worksheet_dataframe.head())

if __name__ == '__main__':
    main()