import pytest, json
import pandas as pd
from ipe_process_orchestrator.assign_competencies import IPECompetenciesAssigner

@pytest.fixture
def single_ipe_offering_with_all_enrolled_criteria():
  course = {'Offering Name': 'Teams & Teamwork Module', 'Offering ID': '2018-017', 'Offering-instance ID': '2018-017-05-W21', 
  'udp_term_name': 'Winter 2021', 'Year': 2021, 'Term': 'Winter', 'UM Term Code': 'WN 2021', 
  'Description': 'The module is structured so that students will complete online reading/self-assessment in week 1.', 
  'Lead Faculty Member 1': 'Jane Doe', 'Lead Faculty Member 2': 'JohnDoe', 'Lead Faculty 1 School': 'Dentistry', 'Lead Faculty 2 School': 'Public Health', 
  'Lead Faculty 1 unique name': 'JaDoe', 'Lead Faculty 2 unique name': 'Jdoe', 
  'Format': 'Online', 'Instructional Team\\n(SEE LOOKUP TABLE)': '', 'Program offering to students\\n(SEE LOOKUP TABLE)': '', 
  'Course #s (if applicable)': '', 'Window used': 'None', 'IPE Assessments': 'SPICE-R2 ', 'Canvas Site or Shell Course': '', 
  'Canvas Course ID': 448447, 'Roles/Responsibilities': 'N/A', 'Interprofessional Communication': 'N/A', 'Team/Teamwork': 'Introduce', 'Values/Ethics': 'N/A', 'Intercultural Humility': 'N/A', 'Dosage (contact hours)': 4, 
  'Criteria for Assigning Outcomes in Canvas': 'Passing - 70% or Higher', 'Notes': '', 'When does script run? (Feb, June, Oct)': 'June', 'Script Run?': ''}
  return course

@pytest.fixture
def ipe_assigner_class(api_handler, single_ipe_offering_with_all_enrolled_criteria) -> IPECompetenciesAssigner:
  with open('tests/fixtures/rubrics_api_response.json','r') as f:
        response_json = json.loads(f.read())
  course_series = pd.Series(single_ipe_offering_with_all_enrolled_criteria)
  return IPECompetenciesAssigner(api_handler, '12345', course_series, response_json)

@pytest.fixture
def student_data():
  students_grades = [{'student_canvas_id': 136945, 'student_name': 'Student User1', 'grade': 62.59},
  {'student_canvas_id': 136946, 'student_name': 'Student User2', 'grade': 70.00},
  {'student_canvas_id': 136947, 'student_name': 'Student User3', 'grade': 69.99},
  {'student_canvas_id': 136948, 'student_name': 'Student User4', 'grade': 80.59},
  {'student_canvas_id': 136949, 'student_name': 'Student User5', 'grade': 50.59},
  {'student_canvas_id': 136950, 'student_name': 'Student User6', 'grade': 60.59},
  {'student_canvas_id': 136951, 'student_name': 'Student User7', 'grade': 70.59},
  {'student_canvas_id': 136952, 'student_name': 'Student User8', 'grade': 90.10},
  {'student_canvas_id': 136953, 'student_name': 'Student User9', 'grade': 100.59},
  {'student_canvas_id': 136954, 'student_name': 'Student User10', 'grade': 200.59}]
  return students_grades


def test_right_student_list_returned_based_assignment_criteria(api_handler, rubric_simple, student_data):
  course = pd.Series({'term': 1234, 'course': 'somethig', 'instructor': 'somebody'})
  comp_assigner = IPECompetenciesAssigner(api_handler, '12345', course, rubric_simple)
  students_grades_actual= comp_assigner.get_student_list_to_receive_competencies(student_data)
  assert 7 == len(students_grades_actual)


