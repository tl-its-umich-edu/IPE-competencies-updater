import json, random
from typing import List
import pandas as pd
from unittest.mock import MagicMock, patch
from requests import Response
from api_handler.api_calls import APIHandler
from ipe_process_orchestrator.assign_competencies import IPECompetenciesAssigner
from constants import COL_ASSIGNING_LO_CRITERIA, AC_ALL_ENROLLED, CANVAS_URL_BEGIN

def test_student_data_with_70_percent_grade(api_handler, single_ipe_offering, student_data):
  """
  This should return only the students with a grade of 70% or higher
  
  params are pytest fixtures taken from fixtures folder and from these file under it competencies_data.py. 
  api_handler from  conftest.py
  """
  course = pd.Series(single_ipe_offering)
  comp_assigner = IPECompetenciesAssigner(api_handler, '448447', course, {})
  students_grades_actual= comp_assigner.get_student_list_to_receive_competencies(student_data)
  assert 5 == len(students_grades_actual)

def test_student_data_with_all_enrolled(api_handler, single_ipe_offering, student_data):
  """
  This should return all the students in the course
  
  params are pytest fixtures taken from fixtures folder and from these file under it competencies_data.py. 
  api_handler from  conftest.py
  """
  single_ipe_offering[COL_ASSIGNING_LO_CRITERIA] = AC_ALL_ENROLLED
  course = pd.Series(single_ipe_offering)
  comp_assigner = IPECompetenciesAssigner(api_handler, '448447', course, {})
  students_grades_actual= comp_assigner.get_student_list_to_receive_competencies(student_data)
  assert 10 == len(students_grades_actual)

def test_competencies_payload_based_according_to_course(api_handler, single_ipe_offering, rubric_simple, competencies_payload):
  """
  Correct competencies should be returned based on the course and assigned to the students
  
  params are pytest fixtures taken from fixtures folder and from these file under it competencies_data.py, rubric_simplified_obj.py. 
  api_handler from  conftest.py
  """
  course = pd.Series(single_ipe_offering)
  comp_assigner = IPECompetenciesAssigner(api_handler, '448447122', course, rubric_simple)
  payload_actual = comp_assigner.get_competency_payload()
  assert payload_actual == competencies_payload

def test_competencies_payload_with_no_dosage(api_handler, single_ipe_offering, rubric_simple, competencies_payload2):
  """
  This tests when doasage is not given then the payload will return no dose values
  
  params are pytest fixtures taken from fixtures folder and from these file under it competencies_data.py, rubric_simplified_obj.py. 
  api_handler from  conftest.py
  """
  single_ipe_offering['Dosage (contact hours)'] = ''
  single_ipe_offering['Intercultural Humility'] = 'Practice'
  single_ipe_offering['Interprofessional Communication'] = 'Reinforce'
  single_ipe_offering['Roles/Responsibilities'] = 'Practice'
  single_ipe_offering['Team/Teamwork'] = 'Introduce'
  single_ipe_offering['Values/Ethics'] = 'N/A'

  course = pd.Series(single_ipe_offering)
  comp_assigner = IPECompetenciesAssigner(api_handler, '448447122', course, rubric_simple)
  payload_actual = comp_assigner.get_competency_payload()
  assert payload_actual == competencies_payload2

def test_competencies_payload_with_zero_dosage(api_handler, single_ipe_offering, rubric_simple, competencies_payload2):
  """
  This tests when doasage is zero hours given then the payload will return no dose values
  """
  single_ipe_offering['Dosage (contact hours)'] = 0
  single_ipe_offering['Intercultural Humility'] = 'Practice'
  single_ipe_offering['Interprofessional Communication'] = 'Reinforce'
  single_ipe_offering['Roles/Responsibilities'] = 'Practice'
  single_ipe_offering['Team/Teamwork'] = 'Introduce'
  single_ipe_offering['Values/Ethics'] = 'N/A'

  course = pd.Series(single_ipe_offering)
  comp_assigner = IPECompetenciesAssigner(api_handler, '448447122', course, rubric_simple)
  payload_actual = comp_assigner.get_competency_payload()
  assert payload_actual == competencies_payload2

def test_more_enrollments_are_fetched(api_handler, ipe_props, enrollment_response, single_ipe_offering):
  """
  This tests make sure the pagination works as expected when fetching more enrollments
  The Real API will return 100 for first call and paged after. Test is written to mimic paging workflow but actually returing
  4 enrollments in first call and 6 in next page.
  
  params are pytest fixtures taken from fixtures folder and from these file under it competencies_data.py. 
  api_handler from  conftest.py
   
  """
  url_partial = f'{CANVAS_URL_BEGIN}/courses/11111/enrollments'
  full_url = '/'.join([ipe_props.get('api_url'), url_partial])
  enrollment_resp1: MagicMock = MagicMock(
        spec=Response,
        status_code=200,
        ok=True,
        text=json.dumps(enrollment_response[:4]),
        url=full_url
    )
  enrollment_resp2: MagicMock = MagicMock(
    spec=Response,
    status_code=200,
    ok=True,
    text=json.dumps(enrollment_response[4:10]),
    url=full_url
  )
  next_page1_response = {'state[]': ['active'], 'type[]': ['StudentEnrollment'], 'page': ['bookmark:WyJTd'], 'per_page': ['100']}
  next_page2_response = None

  with patch.object(APIHandler, 'api_call_with_retries',autospec=True) as mock_enrollment:
    with patch.object(APIHandler, 'get_next_page',autospec=True) as mock_next_page:
      mock_enrollment.side_effect = [enrollment_resp1, enrollment_resp2]
      mock_next_page.side_effect = [next_page1_response, next_page2_response]
      course = pd.Series(single_ipe_offering)
      students_grades_actual = IPECompetenciesAssigner(api_handler, '448447122', course, {}).get_student_list_with_course_grades()
  assert len(students_grades_actual) == 10
  assert mock_enrollment.call_count == 2
  assert mock_next_page.call_count == 2

def test_competencies_assigned_to_students_with_all_success(ipe_props, student_data, api_handler, single_ipe_offering, rubric_simple):
  """
  This tests that the competencies are assigned to the students
  
  params are pytest fixtures taken from fixtures folder and from these file under it competencies_data.py, rubric_simplified_obj.py. 
  api_handler from  conftest.py
  """
  url_partial = f'{CANVAS_URL_BEGIN}/courses/11111/enrollments'
  full_url = '/'.join([ipe_props.get('api_url'), url_partial])
  course = pd.Series(single_ipe_offering)
  comp_assigner = IPECompetenciesAssigner(api_handler, '448447122', course, rubric_simple)
  student_data_receiving = comp_assigner.get_student_list_to_receive_competencies(student_data)
  resp_mocks: List[MagicMock] = [
          MagicMock(
              spec=Response, status_code=200, ok=True, text=json.dumps({'success': True}), url=full_url
          )
          for i in range(len(student_data_receiving))
      ]

  with patch.object(APIHandler, 'api_call_with_retries', autospec=True) as mock_competencies_assigning:
    mock_competencies_assigning.side_effect = resp_mocks
    comp_assigner.assign_competancies(student_data_receiving)
  # since the criteria for competencies assigned is 70% or greater so the only 6 api call are made snce student_data has 6 students > than 70%
  assert mock_competencies_assigning.call_count == 5

def test_competencies_assigned_to_students_with_few_failures(ipe_props, student_data, api_handler, single_ipe_offering, rubric_simple):
  """
  This tests that the competencies loop for assigning to the students continues even if some competencies are not assigned. 
  We don't want to stop the loop if one competency fails to assign. 
  
  params are pytest fixtures taken from fixtures folder and from these file under it competencies_data.py, rubric_simplified_obj.py. 
  api_handler from  conftest.py
  """
  url_partial = f'{CANVAS_URL_BEGIN}/courses/11111/enrollments'
  full_url = '/'.join([ipe_props.get('api_url'), url_partial])
  single_ipe_offering[COL_ASSIGNING_LO_CRITERIA] = AC_ALL_ENROLLED
  course = pd.Series(single_ipe_offering)
  comp_assigner = IPECompetenciesAssigner(api_handler, '448447122', course, rubric_simple)
  resp_mocks: List[MagicMock] = [
          MagicMock(
              spec=Response, status_code=200, ok=True, text=json.dumps({'success': True}), url=full_url
          )
          for i in range(len(student_data)-3)
      ]
  resp_mocks.extend([None,None,None])
  
  random.shuffle(resp_mocks)

  with patch.object(APIHandler, 'api_call_with_retries', autospec=True) as mock_competencies_assigning:
    mock_competencies_assigning.side_effect = resp_mocks
    comp_assigner.assign_competancies(student_data)
  assert mock_competencies_assigning.call_count == 10

    






