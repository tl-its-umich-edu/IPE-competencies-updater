import logging, os, time, datetime
from typing import Dict, Optional
from dotenv import load_dotenv
from read_env_props import ReadEnvProps
from gspread import Worksheet
from ipe_course_data.get_ipe_data_from_gsheets import GetIPEDataFromSheets
from ipe_process_orchestrator.orchestrator import IPECompetenciesOrchestrator
from api_handler.api_calls import APIHandler

ENV_PATH: str =  os.getenv('IPE_ENV_FILE')
load_dotenv(dotenv_path=ENV_PATH, verbose=True) if ENV_PATH is not None else load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('LOG_LEVEL') if os.getenv('LOG_LEVEL') else 'INFO', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    logger.info("IPE Process Starting....")
    start = time.perf_counter()
    props: Dict[str, Optional[str]] =  ReadEnvProps().get_env_props()
    ipeData: GetIPEDataFromSheets = GetIPEDataFromSheets(props)
    worksheet: Worksheet = ipeData.get_worksheet_instance()
    api_handler: APIHandler = APIHandler(props)
    orchestrator: IPECompetenciesOrchestrator = IPECompetenciesOrchestrator(props, worksheet, api_handler)
    orchestrator.start_composing_process()
    end = time.perf_counter()
    logger.info(f"IPE Process Completed and took about {datetime.timedelta(seconds=(end - start))}")


if __name__ == '__main__':
    main()