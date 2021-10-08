import os
import logging
from typing import DefaultDict
logger = logging.getLogger(__name__)

class ReadEnvProps:
    def __init__(self):
        self.env_props: DefaultDict = {}
        self._read_env_props()

    def _read_env_props(self) -> None:
        logger.debug("Reading environment properties")
        self.env_props['sheet_id'] = os.environ.get('IPE_SHEET_ID', '1fvYhtxlu3pa8vNBjOVzp1hwNBsv823mTD3uP6l5_WuI')
        self.env_props['sheet_name'] = os.environ.get('IPE_SHEET_NAME', 'Offerings')
        self.env_props['service_account_path'] = os.environ.get('GSERVICE_ACCOUNT_PATH', 'secrets/ipe_gserviceaccount.json')
        self.env_props['is_docker_run'] = os.environ.get('IS_DOCKER_RUN', True)



    def get_env_props(self) -> DefaultDict[str, str]:
        return self.env_props