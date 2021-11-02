import os, sys
import logging
from typing import DefaultDict
logger = logging.getLogger(__name__)

class ReadEnvProps:
    def __init__(self):
        self.env_props: DefaultDict = {}
        self._read_env_props()

    def _read_env_props(self) -> None:
        logger.debug("Reading environment properties")
        self.env_props['sheet_id'] = os.environ.get('IPE_SHEET_ID')
        self.env_props['sheet_name'] = os.environ.get('IPE_SHEET_NAME')
        self.env_props['service_account_path'] = os.environ.get('GSERVICE_ACCOUNT_PATH')



    def get_env_props(self) -> DefaultDict[str, str]:
        logger.info(self.env_props)
        is_missing_props: bool = False
        for key, value in self.env_props.items():
            if self.env_props[key] is None or self.env_props[key] == '':
                logger.error(f"the property {key} is not set as part of environment variable")
                is_missing_props = True
        if is_missing_props:
            logger.error("Missing few environment variables")
            sys.exit(1)
        return self.env_props