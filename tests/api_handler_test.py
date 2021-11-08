import json
from typing import List
from unittest.mock import MagicMock, patch
from requests import Response
from api_handler.api_calls import APIHandler
from umich_api.api_utils import ApiUtil
from constants import CANVAS_URL_BEGIN


def test_check_if_response_successful_when_valid(api_handler: APIHandler):
    """check_if_response_successful returns True with a valid Response."""
    response: MagicMock = MagicMock(
        spec=Response,
        status_code=200,
        ok=True,
        text=json.dumps({'success': True}),
        url='http://httpbin.org/get'
    )
    result: bool = api_handler.check_if_response_successful(response)
    assert result is True


def test_check_if_response_unsuccessful_when_valid(api_handler: APIHandler):
    """check_if_response_successful returns True with a valid Response."""

    response: MagicMock = MagicMock(
        spec=Response,
        status_code=400,
        ok=False,
        text=json.dumps({'success': False}),
        url='http://httpbin.org/get'
    )
    result: bool = api_handler.check_if_response_successful(response)
    assert result is False


def test_check_if_response_successful_with_invalid_json(api_handler: APIHandler):
    """check_if_response_successful returns False if Response has invalid JSON in text variable."""
    invalid_json_str: str = '{"success": True'
    response: MagicMock = MagicMock(
        spec=Response,
        status_code=200,
        ok=True,
        text=invalid_json_str,  # invalid JSON
        url='http://httpbin.org/get'
    )
    result: bool = api_handler.check_if_response_successful(response)
    assert result is False


def test_api_with_no_errors(ipe_props, api_handler: APIHandler):
    """api_call_with_retries returns Response object when a valid Response is found."""
    url_partial = f'{CANVAS_URL_BEGIN}/courses/11111/assignment_groups'
    full_url = '/'.join([ipe_props.get('api_url'), url_partial])
    mock_resp: MagicMock = MagicMock(
        spec=Response,
        status_code=201,
        ok=True,
        text=json.dumps({'success': True}),
        url=full_url
    )
    with patch.object(ApiUtil, 'api_call', autospec=True) as mock_api_call:
        mock_api_call.return_value = mock_resp
        response = api_handler.api_call_with_retries(
            url_partial, 'GET', {})
    assert response.status_code == 201
    assert response.text == mock_resp.text
    assert mock_api_call.call_count == 1

def test_api_retry_if_failure(ipe_props, api_handler: APIHandler):
  url_partial = f'{CANVAS_URL_BEGIN}/courses/11111/assignment_groups'
  full_url = '/'.join([ipe_props.get('api_url'), url_partial])

  resp_mocks: List[MagicMock] = [
            MagicMock(
                spec=Response, status_code=504, ok=False, text=json.dumps({'message': 'Gateway Timeout'}), url=full_url
            )
            for i in range(3)
        ]
  with patch.object(ApiUtil, 'api_call', autospec=True) as mock_api_call:
      mock_api_call.side_effect = resp_mocks
      response = api_handler.api_call_with_retries(
          url_partial, 'GET', {})
  assert mock_api_call.call_count == 3
  assert response == None

  


