import logging, os
from typing import Dict, Optional
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from gspread import Worksheet
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets
from ipe_process_orchestrator.orchestrator import IPECompetenciesOrchestrator
from api_handler.api_calls import APIHandler

ENV_PATH: str = print('Please set set the Env file path') if os.getenv('IPE_ENV_FILE') is None else os.getenv('IPE_ENV_FILE') 
load_dotenv(dotenv_path=ENV_PATH, verbose=True)

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('LOG_LEVEL') if os.getenv('LOG_LEVEL') else 'INFO', format='%(name)s - %(levelname)s - %(message)s')

def main():
    logger.info("IPE Process Starting....")
    props: Dict[str, Optional[str]] =  ReadEnvProps().get_env_props()
    ipeData: GetIPEDataFromSheets = GetIPEDataFromSheets(props)
    worksheet: Worksheet = ipeData.get_worksheet_instance()
    api_handler: APIHandler = APIHandler(props)
    orchestrator: IPECompetenciesOrchestrator = IPECompetenciesOrchestrator(props, worksheet, api_handler)
    orchestrator.start_composing_process()
    logger.info("IPE Process Completed....")


if __name__ == '__main__':
    main()