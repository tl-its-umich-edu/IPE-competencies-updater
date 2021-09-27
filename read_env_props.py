import os
import logging
logger = logging.getLogger(__name__)

class ReadEnvProps:
    def __init__(self):
        self.env_props: object = {}
        self._read_env_props()

    def _read_env_props(self) -> None:
        logger.debug("Reading environment properties")
        self.env_props['ipe_sheet_id'] = os.getenv('IPE_SHEET_ID')

    def get_env_props(self) -> object:
        return self.env_props