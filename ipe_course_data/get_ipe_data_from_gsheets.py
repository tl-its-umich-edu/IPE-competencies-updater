import os
import logging
import sys
import gspread as gs
from typing import Union, NoReturn

from gspread.exceptions import APIError, WorksheetNotFound
from ipe_course_data.get_ipe_data import GetIPEData
from gspread.models import Worksheet
from constants import (SHEET_NAME)
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
        self.service_account_path = ipe_props.get('service_account_path')

    def get_data(self) -> Union[Worksheet, NoReturn]:
        """
        Get all data from Google Sheets, even if filters applied to the sheet.

        """
        logger.debug('Getting data from IPE Google Sheets')
        logger.info(f"Path to service account: {self.service_account_path}")
        if not os.path.exists(self.service_account_path):
            logger.error(
                f'Service account file not found: {self.service_account_path}')
            sys.exit(1)
        try:
            credentials = gs.service_account(self.service_account_path)
            sheets = credentials.open_by_url(
                f'{self.GOOGLE_SHEETS_URL}{self.sheet_id}')
            worksheet = sheets.worksheet(SHEET_NAME)
            return worksheet
        except (APIError, WorksheetNotFound, Exception) as e:
            if isinstance(e, WorksheetNotFound):
                logger.error(f'Worksheet not found: {SHEET_NAME}')
            elif isinstance(e, APIError):
                logger.error(f'No Google sheet found, due to {e}')
            else:
                logger.error(
                    f'Trouble connecting a Google Sheet using service account, due to {e}')

            sys.exit(1)
