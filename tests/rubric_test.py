import json
from ipe_process_orchestrator.rubric_data import IPERubricSimplified

def test_rubric_object(api_handler, rubric_simple):
  
  with open('tests/fixtures/rubrics_api_response.json','r') as f:
        response_json = json.loads(f.read())
  
  rubric= IPERubricSimplified(api_handler, '222222', '334444333')
  simple_rubric_actual = rubric._get_rubric_data(response_json)
  assert simple_rubric_actual == rubric_simple
  