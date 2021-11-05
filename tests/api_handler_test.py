import json
from unittest.mock import MagicMock, patch
from requests import Response
from api_handler.api_calls import APIHandler
def test_check_if_response_successful_when_valid(ipe_props):
        """check_if_response_successful returns True with a valid Response."""
        response: MagicMock = MagicMock(
            spec=Response,
            status_code=200,
            text=json.dumps({'success': True}),
            url='http://httpbin.org/get'
        )
        result: bool = APIHandler(ipe_props).check_if_response_successful(response)
        assert result is True

def test_check_if_response_unsuccessful_when_valid(ipe_props):
        """check_if_response_successful returns True with a valid Response."""
        
        response: MagicMock = MagicMock(
            spec=Response,
            status_code=400,
            text=json.dumps({'success': False}),
            url='http://httpbin.org/get'
        )
        result: bool = APIHandler(ipe_props).check_if_response_successful(response)
        assert result is True

def test_check_if_response_successful_with_invalid_json(ipe_props):
        """check_if_response_successful returns False if Response has invalid JSON in text variable."""
        invalid_json_str: str = '{"success": True'
        response: MagicMock = MagicMock(
            spec=Response,
            status_code=200,
            text=invalid_json_str,  # invalid JSON
            url='http://httpbin.org/get'
        )
        result: bool = APIHandler(ipe_props).check_if_response_successful(response)
        assert result is False
