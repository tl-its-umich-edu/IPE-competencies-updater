import pytest, json

@pytest.fixture
def single_ipe_offering():
  return {'Offering Name': 'Teams & Teamwork Module', 'Offering ID': '2018-017', 'Offering-instance ID': '2018-017-05-W21', 
  'udp_term_name': 'Winter 2021', 'Year': 2021, 'Term': 'Winter', 'UM Term Code': 'WN 2021', 
  'Description': 'The module is structured so that students will complete online reading/self-assessment in week 1.', 
  'Lead Faculty Member 1': 'Jane Doe', 'Lead Faculty Member 2': 'JohnDoe', 'Lead Faculty 1 School': 'Dentistry', 'Lead Faculty 2 School': 'Public Health', 
  'Lead Faculty 1 unique name': 'JaDoe', 'Lead Faculty 2 unique name': 'Jdoe', 
  'Format': 'Online', 'Instructional Team\\n(SEE LOOKUP TABLE)': '', 'Program offering to students\\n(SEE LOOKUP TABLE)': '', 
  'Course #s (if applicable)': '', 'Window used': 'None', 'IPE Assessments': 'SPICE-R2 ', 'Canvas Site or Shell Course': '', 'Canvas Course ID': '448447',
  'Roles/Responsibilities': 'N/A', 'Interprofessional Communication': 'N/A', 'Team/Teamwork': 'Introduce', 'Values/Ethics': 'N/A', 'Intercultural Humility': 'N/A', 
  'Dosage (contact hours)': 4, 'Criteria for Assigning Outcomes in Canvas': 'Passing - 70% or Higher', 'Notes': '', 
  'When does script run? (Feb, June, Oct)': 'June', 'Script Run?': ''}

@pytest.fixture
def student_data():
  return [{'student_canvas_id': 136949, 'student_name': 'Student User5', 'grade': 50.59},
  {'student_canvas_id': 136950, 'student_name': 'Student User6', 'grade': 60.59},
  {'student_canvas_id': 136945, 'student_name': 'Student User1', 'grade': 62.59},
  {'student_canvas_id': 136947, 'student_name': 'Student User3', 'grade': 69.99},
  {'student_canvas_id': 136946, 'student_name': 'Student User2', 'grade': 70.00},
  {'student_canvas_id': 136948, 'student_name': 'Student User4', 'grade': 80.59},
  {'student_canvas_id': 136951, 'student_name': 'Student User7', 'grade': 70.59},
  {'student_canvas_id': 136952, 'student_name': 'Student User8', 'grade': 90.10},
  {'student_canvas_id': 136953, 'student_name': 'Student User9', 'grade': 100.59},
  {'student_canvas_id': 136954, 'student_name': 'Student User10', 'grade': 200.59}]

@pytest.fixture
def competencies_payload():
  return {
    'rubric_assessment[_3104][rating_id]': 'blank',  #Dosage
    'rubric_assessment[_3104][points]': 4.0, 
    'rubric_assessment[76864_390][rating_id]': '76864_5328', #Intercultural Humility
    'rubric_assessment[76864_390][points]': 0.0, 
    'rubric_assessment[76864_6556][rating_id]': '76864_4759', #Interprofessional Communication
    'rubric_assessment[76864_6556][points]': 0.0, 
    'rubric_assessment[76864_8770][rating_id]': '76864_799', #Roles/Responsibilities
    'rubric_assessment[76864_8770][points]': 0.0, 
    'rubric_assessment[76864_2231][rating_id]': '76864_3528', #Team/Teamwork
    'rubric_assessment[76864_2231][points]': 1.0, 
    'rubric_assessment[76864_7039][rating_id]': '76864_6509', #Values/Ethics
    'rubric_assessment[76864_7039][points]': 0.0}

@pytest.fixture
def competencies_payload2():
  return {
    'rubric_assessment[_3104][rating_id]': 'blank_2',  #Dosage
    'rubric_assessment[_3104][points]': 0, 
    'rubric_assessment[76864_390][rating_id]': '76864_8410', #Intercultural Humility
    'rubric_assessment[76864_390][points]': 5.0, 
    'rubric_assessment[76864_6556][rating_id]': '76864_7059', #Interprofessional Communication
    'rubric_assessment[76864_6556][points]': 3.0, 
    'rubric_assessment[76864_8770][rating_id]': '76864_8566', #Roles/Responsibilities
    'rubric_assessment[76864_8770][points]': 5.0, 
    'rubric_assessment[76864_2231][rating_id]': '76864_3528', #Team/Teamwork
    'rubric_assessment[76864_2231][points]': 1.0, 
    'rubric_assessment[76864_7039][rating_id]': '76864_6509', #Values/Ethics
    'rubric_assessment[76864_7039][points]': 0.0}
  
@pytest.fixture
def enrollment_response():
  with open('tests/fixtures/enrollment_response.json','r') as f:
        enrollment_json = json.loads(f.read())
  return enrollment_json