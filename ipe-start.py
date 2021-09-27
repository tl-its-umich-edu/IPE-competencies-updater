import logging, os
from dotenv import load_dotenv
from read_env_props import ReadEnvProps

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv('LOG_LEVEL') if os.getenv('LOG_LEVEL') else 'INFO', format='%(name)s - %(levelname)s - %(message)s')
def main():
    logger.info("IPE Process Starting....")
    endProps: ReadEnvProps =  ReadEnvProps()
    logger.info(endProps.get_env_props())


if __name__ == '__main__':
    main()