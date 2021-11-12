import pytest, json
import pandas as pd
from ipe_process_orchestrator.assign_competencies import IPECompetenciesAssigner

@pytest.fixture
def ipe_assigner_class(api_handler):
  with open('tests/fixtures/rubrics_api_response.json','r') as f:
        response_json = json.loads(f.read())
  
  course = {'Offering Name': 'Teams & Teamwork Module', 'Offering ID': '2018-017', 'Offering-instance ID': '2018-017-05-W21', 
  'udp_term_name': 'Winter 2021', 'Year': 2021, 'Term': 'Winter', 'UM Term Code': 'WN 2021', 
  'Description': 'The module is structured so that students will complete online reading/self-assessment in week 1.', 
  'Lead Faculty Member 1': 'Jane Doe', 'Lead Faculty Member 2': 'JohnDoe', 'Lead Faculty 1 School': 'Dentistry', 'Lead Faculty 2 School': 'Public Health', 
  'Lead Faculty 1 unique name': 'JaDoe', 'Lead Faculty 2 unique name': 'Jdoe', 
  'Format': 'Online', 'Instructional Team\\n(SEE LOOKUP TABLE)': '', 'Program offering to students\\n(SEE LOOKUP TABLE)': '', 
  'Course #s (if applicable)': '', 'Window used': 'None', 'IPE Assessments': 'SPICE-R2 ', 'Canvas Site or Shell Course': '', 
  'Canvas Course ID': 448447, 'Roles/Responsibilities': 'N/A', 'Interprofessional Communication': 'N/A', 'Team/Teamwork': 'Introduce', 'Values/Ethics': 'N/A', 'Intercultural Humility': 'N/A', 'Dosage (contact hours)': 4, 
  'Criteria for Assigning Outcomes in Canvas': 'Passing - 70% or Higher', 'Notes': '', 'When does script run? (Feb, June, Oct)': 'June', 'Script Run?': ''}
  course_series = pd.Series(course)
  
  return IPECompetenciesAssigner(api_handler, '12345', course_series, response_json)

def test_right_student_list_returned_based_assignment_criteria(ipe_assigner_class):
  pass


