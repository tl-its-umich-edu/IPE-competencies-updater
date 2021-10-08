import os, logging, sys
import gspread as gs
from typing import Union, NoReturn

from gspread.exceptions import APIError, WorksheetNotFound
from ipe_course_data.get_ipe_data import GetIPEData
from gspread.models import Worksheet
logger = logging.getLogger(__name__)

class GetIPEDataFromSheets(GetIPEData):
    """
    Class to get data from Google Sheets
    """
    GOOGLE_SHEETS_URL = 'https://docs.google.com/spreadsheets/d/'
    def __init__(self, ipe_props):
        """
        Initialize the class
        """
        self.sheet_id = ipe_props.get('sheet_id')
        self.sheet_name = ipe_props.get('sheet_name')
        self.service_account_path = ipe_props.get('service_account_path')
        self.is_docker_run = ipe_props.get('is_docker_run')

    def get_data(self)-> Union[Worksheet, NoReturn]:
        """
        Get all data from Google Sheets, even if filters applied to the sheet.

        """
        logger.debug('Getting data from IPE Google Sheets')
        google_service_account_path: str = self._get_google_service_account_path()
        logger.info(f"Path to service account: {google_service_account_path}")
        if not os.path.exists(google_service_account_path):
            logger.error(f'Service account file not found: {google_service_account_path}')
            sys.exit(1)
        try:
            credentials = gs.service_account(google_service_account_path)
            sheets = credentials.open_by_url(f'{self.GOOGLE_SHEETS_URL}{self.sheet_id}')
            worksheet = sheets.worksheet(self.sheet_name)
            return worksheet
        except (APIError, WorksheetNotFound, Exception) as e:
            if isinstance(e, WorksheetNotFound):
                logger.error(f'Worksheet not found: {self.sheet_name}')
            elif isinstance(e, APIError):
                logger.error(f'No Google sheet found, due to {e}')
            else:
                logger.error(f'Trouble connecting a Google Sheet using service account, due to {e}')
            
            sys.exit(1)
    
    def _get_google_service_account_path(self)-> str:
        """
        Get the path to the Google service account file
        """
        local_run_path: str = os.path.join(os.environ['HOME'], self.service_account_path)
        docker_run_path: str = os.path.join(os.path.sep, self.service_account_path)
        service_account_path: str = docker_run_path if eval(self.is_docker_run) else local_run_path
        return service_account_path