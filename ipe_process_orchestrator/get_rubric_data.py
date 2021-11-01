import logging, json
from typing import Any, Dict, List
from api_handler.api_calls import APIHandler
from ipe_process_orchestrator.api_helper import response_none_check
from constants import (CANVAS_URL_BEGIN, COL_COMPETENCIES_RR,COL_COMPETENCIES_TTW, COL_COMPETENCIES_IC, COL_COMPETENCIES_VE,COL_COMPETENCIES_IH, COL_DOSAGE)

logger = logging.getLogger(__name__)
class IPERubricDataMapping():
    def __init__(self, api_handler, rubric_account_id, rubric_id)-> None:
        self.api_handler:  APIHandler = api_handler
        self.rubric_account_id: int = rubric_account_id
        self.rubric_id: int= rubric_id

    def fetch_rubric_api(self) -> Dict[str, Any]:
        rubrics_api_url: str = f'{CANVAS_URL_BEGIN}/accounts/{self.rubric_account_id}/rubrics/{self.rubric_id}'
        rubrics_response = self.api_handler.api_call_with_retries(rubrics_api_url, 'GET')

        err_msg = f'Error fetching rubric id: {self.rubric_id} in account {self.rubric_account_id}'
        response_none_check(self, rubrics_response, err_msg)

        rubrics_data = json.loads(rubrics_response.text)
        return self._get_rubric_data(rubrics_data)
    
    @staticmethod
    def competencies_data_mapping()-> Dict[str, str]:
        return {
            'Roles/Responsibilities':  COL_COMPETENCIES_RR,
            'Team/Teamwork': COL_COMPETENCIES_TTW,
            'Interprofessional Communication': COL_COMPETENCIES_IC,
            'Values/Ethics': COL_COMPETENCIES_VE,
            'Intercultural Humility': COL_COMPETENCIES_IH,
            'Dosage (contact hours)': COL_DOSAGE
        }

    def _get_rubric_data(self, rubrics_data: Dict[str, Any])-> None:
        simliplied_rubrics_data = dict()
        rubric_data: List[Dict[str, Any]] = rubrics_data['data']
        for criteria in rubric_data:
            criteria_id = criteria['id']
            criteria_rating = criteria['ratings']
            criteria_description = criteria['description']
            gsheets_col_name = IPERubricDataMapping.competencies_data_mapping()[criteria_description]
            criteria_object = {
                'id': criteria_id,
                'description': criteria_description,
                'ratings': self.criteria_rating_simple(criteria_rating),
            }
            simliplied_rubrics_data[gsheets_col_name] = criteria_object
        logger.info(f'New rubric data: {simliplied_rubrics_data}')
        return simliplied_rubrics_data

    def criteria_rating_simple(self, criteria_rating) -> List[Dict[str, Any]]:
        criteria_rating_simplied = list()
        for rating in criteria_rating:
            rating_description = rating['description'].strip('/').replace('"', '') if 'dose' in rating['description'] else rating['description']
            rating_object= {}
            rating_object = {
                    'id' : rating['id'],
                    'points' : rating['points'],
                    'description': rating_description.replace('/', '')
            }
            criteria_rating_simplied.append(rating_object)
  
        return criteria_rating_simplied

