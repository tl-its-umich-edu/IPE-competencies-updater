import os, sys
import logging
from typing import Any, Dict, Optional, Union
logger = logging.getLogger(__name__)

class ReadEnvProps:
    def __init__(self):
        self.env_props: Dict[str, Optional[str]] = dict()
        self._read_env_props()

    def _read_env_props(self) -> None:
        logger.debug("Reading environment properties")
        self.env_props['sheet_id'] = os.environ.get('IPE_SHEET_ID')
        self.env_props['service_account_path'] = os.environ.get('GSERVICE_ACCOUNT_PATH')
        self.env_props['api_client'] = os.environ.get('API_DIRECTORY_CLIENT_ID')
        self.env_props['api_secret'] = os.environ.get('API_DIRECTORY_SECRET')
        self.env_props['api_url'] = os.environ.get('API_DIRECTORY_URL')
        self.env_props['rubric_id'] = os.environ.get('IPE_RUBRIC_ID')
        self.env_props['rubric_account_id'] = os.environ.get('IPE_RUBRICS_ACCOUNT')
        self.env_props['retry_attempts'] = os.environ.get('MAX_REQ_ATTEMPTS')
        self.env_props['script_run_month'] = os.environ.get('SCRIPT_RUN_MONTH')
        self.env_props['update_sheet'] = os.environ.get('UPDATE_SHEET')
        self.env_props['wait_limit'] = os.environ.get('WAIT_LIMIT')
    
    def get_env_props(self) -> Dict[str, Optional[str]]:
        logger.debug(self.env_props)
        is_missing_props: bool = False
        for key, value in self.env_props.items():
            if self.env_props[key] is None or self.env_props[key] == '':
                logger.error(f"the property {key} is not set as part of environment variable")
                is_missing_props = True
        if is_missing_props:
            logger.error("Missing few environment variables")
            sys.exit(1)
        return self.env_props