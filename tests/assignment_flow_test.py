import json
from ipe_process_orchestrator.assignment_flow import IPEAssignmentFlow
from unittest.mock import MagicMock, patch
from constants import CANVAS_URL_BEGIN
from api_handler.api_calls import APIHandler
from requests.models import Response 


def test_assign_look_up_with_one_record(ipe_props, api_handler):
    """
    Test that the assignment lookup endpoint works.
    """
    assignment_flow: IPEAssignmentFlow = IPEAssignmentFlow(api_handler,12344, '345566')
    url_partial = f'{CANVAS_URL_BEGIN}/courses/403334/assignment_groups'
    full_url = '/'.join([ipe_props.get('api_url'), url_partial])

    with open('tests/fixtures/json/assignment_grp_resp.json','r') as f:
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

def test_assign_look_up_with_no_record(ipe_props, api_handler):
    """
    this test when no existing IPE assignment group or assignment
    """
    assignment_flow: IPEAssignmentFlow = IPEAssignmentFlow(api_handler,12344, '345566')
    url_partial = f'{CANVAS_URL_BEGIN}/courses/403334/assignment_groups'
    full_url = '/'.join([ipe_props.get('api_url'), url_partial])

    with open('tests/fixtures/json/no_assign_grp_or_assignment.json','r') as f:
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
    assert [] == ag_list_value

def test_assignment_lookup_with_multiple_records(ipe_props, api_handler):
    """
    this test when multiple existing IPE assignment groups or assignments the return value will always 
    be the first item in the list
    """
    assignment_flow: IPEAssignmentFlow = IPEAssignmentFlow(api_handler,12344, '345566')
    url_partial = f'{CANVAS_URL_BEGIN}/courses/403334/assignment_groups'
    full_url = '/'.join([ipe_props.get('api_url'), url_partial])

    with open('tests/fixtures/json/assign_grp_with_multiple_assignments.json','r') as f:
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

def test_assignment_with_existing_assignment_grp(ipe_props, api_handler):
    """
    this test when an existing IPE assignment group is found
    """
    assignment_flow: IPEAssignmentFlow = IPEAssignmentFlow(api_handler,12344, '345566')
    url_partial = f'{CANVAS_URL_BEGIN}/courses/403334/assignment_groups/476889'
    full_url = '/'.join([ipe_props.get('api_url'), url_partial])

    with open('tests/fixtures/json/only_assign_grp_without_assignment.json','r') as f:
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

def test_empty_assign_grp(ipe_props, api_handler):
    """
    this is testing with empty assignment group case
    """

    assignment_flow: IPEAssignmentFlow = IPEAssignmentFlow(api_handler,12344, '345566')
    url_partial = f'{CANVAS_URL_BEGIN}/courses/403334/assignment_groups/476889'
    full_url = '/'.join([ipe_props.get('api_url'), url_partial])

    with open('tests/fixtures/json/empty_assign_grp.json','r') as f:
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
    