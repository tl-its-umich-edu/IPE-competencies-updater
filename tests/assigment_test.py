# import pytest, logging
# from dotenv import load_dotenv
# from read_env_props import ReadEnvProps
# from umich_api.api_utils import ApiUtil
# from ipe_process_orchestrator.assignment_flow import IPEAssignmentFlow

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

# @pytest.fixture
# def props():
#     """
#     Fixture for Env properties
#     """
#     load_dotenv()
#     envProps: ReadEnvProps =  ReadEnvProps()
#     return envProps.get_env_props()

# @pytest.fixture
# def api_handler(props):
#     api_handler: ApiUtil = ApiUtil(props.get('api_url'), props.get('api_key'), props.get('api_secret'))
#     return api_handler

# def test_assignment_group_creation(api_handler):
#     """
#     Test to create a new assignment group
#     """
#     assign_flow = IPEAssignmentFlow(props, api_handler,403334)
#     assign_flow._create_assignment_group()
