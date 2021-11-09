import logging
import json
from typing import Any, Dict, List, Optional
from requests.models import Response
from api_handler.api_calls import APIHandler
from ipe_process_orchestrator.api_helper import response_none_check
from constants import (CANVAS_URL_BEGIN)

logger = logging.getLogger(__name__)


class IPERubricSimplified():
    def __init__(self, api_handler, rubric_account_id, rubric_id) -> None:
        self.api_handler:  APIHandler = api_handler
        self.rubric_account_id: str = rubric_account_id
        self.rubric_id: str = rubric_id

    def fetch_rubric_api(self) -> Dict[str, Any]:
        rubrics_api_url: str = f'{CANVAS_URL_BEGIN}/accounts/{self.rubric_account_id}/rubrics/{self.rubric_id}'
        rubrics_response: Optional[Response] = self.api_handler.api_call_with_retries(
            rubrics_api_url, 'GET')

        err_msg = f'Error fetching rubric id: {self.rubric_id} in account {self.rubric_account_id}'
        response_none_check(rubrics_response, err_msg) 

        rubrics_data = json.loads(rubrics_response.text) # type: ignore
        return self._get_rubric_data(rubrics_data)

    def _get_rubric_data(self, rubrics_data: Dict[str, Any]) -> Dict[str, Any]:
        simliplied_rubrics_data: Dict[str, Any] = dict()
        rubric_data: List[Dict[str, Any]] = rubrics_data['data']
        for criteria in rubric_data:
            criteria_id = criteria['id']
            criteria_rating = criteria['ratings']
            criteria_description = criteria['description']
            criteria_object = {
                'id': criteria_id,
                'description': criteria_description,
                'ratings': self._criteria_rating_simple(criteria_rating),
            }
            simliplied_rubrics_data[criteria_description] = criteria_object
        logger.debug(f'New rubric data: {simliplied_rubrics_data}')
        return simliplied_rubrics_data

    def _criteria_rating_simple(self, criteria_rating) -> List[Dict[str, Any]]:
        criteria_rating_simplied = list()
        for rating in criteria_rating:
            rating_description = rating['description'].strip(
                '/').replace('"', '') if 'dose' in rating['description'] else rating['description']
            rating_object = {}
            rating_object = {
                'id': rating['id'],
                'points': rating['points'],
                'description': rating_description
            }
            criteria_rating_simplied.append(rating_object)

        return criteria_rating_simplied
