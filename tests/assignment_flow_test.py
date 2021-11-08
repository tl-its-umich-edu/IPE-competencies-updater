
import json
from ipe_process_orchestrator.assignment_flow import IPEAssignmentFlow
from unittest.mock import MagicMock, patch
from umich_api.api_utils import ApiUtil
from constants import CANVAS_URL_BEGIN
from api_handler.api_calls import APIHandler
from requests.models import Response 


def test_assignment_look_up(ipe_props, api_handler):
    """
    Test that the assignment lookup endpoint works.
    """
    assignment_flow: IPEAssignmentFlow = IPEAssignmentFlow(api_handler,12344, '345566')
    url_partial = f'{CANVAS_URL_BEGIN}/courses/403334/assignment_groups'
    full_url = '/'.join([ipe_props.get('api_url'), url_partial])

    with open('tests/fixtures/assignment_grp_resp.json','r') as f:
        response_json = json.loads(f.read())
    
    response: MagicMock = MagicMock(
        spec=Response,
        status_code=200,
        ok=True,
        text=json.dumps(response_json),
        url=full_url
    )
    
    with patch.object(APIHandler, 'api_call_with_retries', autospec=True) as mock_api_call:
        mock_api_call.return_value = response
        ag_list_value = assignment_flow._look_up_ipe_assignment()
    assert 476889 == ag_list_value
    
    