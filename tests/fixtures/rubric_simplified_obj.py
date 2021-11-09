import pytest


@pytest.fixture(scope="module")
def rubric_simple():
    """
    simplified rubric object
    """
    return {
        'Dosage (contact hours)': {'id': '_3104', 'description': 'Dosage (contact hours)', 'ratings': [{'id': 'blank', 'points': 100.0, 'description': 'Full dose'}, {'id': 'blank_2', 'points': 0.0, 'description': 'No dose'}]},
        'Intercultural Humility': {'id': '76864_390', 'description': 'Intercultural Humility', 'ratings': [{'id': '76864_8410', 'points': 5.0, 'description': 'Practice'}, {'id': '76864_5864', 'points': 3.0, 'description': 'Reinforce'}, {'id': '76864_7608', 'points': 1.0, 'description': 'Introduce'}, {'id': '76864_3977', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '76864_5328', 'points': 0.0, 'description': 'N/A'}]},
        'Interprofessional Communication': {'id': '76864_6556', 'description': 'Interprofessional Communication', 'ratings': [{'id': '76864_1420', 'points': 5.0, 'description': 'Practice'}, {'id': '76864_7059', 'points': 3.0, 'description': 'Reinforce'}, {'id': '76864_8821', 'points': 1.0, 'description': 'Introduce'}, {'id': '76864_5932', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '76864_4759', 'points': 0.0, 'description': 'N/A'}]},
        'Roles/Responsibilities': {'id': '76864_8770', 'description': 'Roles/Responsibilities', 'ratings': [{'id': '76864_8566', 'points': 5.0, 'description': 'Practice'}, {'id': '76864_3364', 'points': 3.0, 'description': 'Reinforce'}, {'id': '76864_6479', 'points': 1.0, 'description': 'Introduce'}, {'id': '76864_3581', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '76864_799', 'points': 0.0, 'description': 'N/A'}]},
        'Team/Teamwork': {'id': '76864_2231', 'description': 'Team/Teamwork', 'ratings': [{'id': '76864_6030', 'points': 5.0, 'description': 'Practice'}, {'id': '76864_4355', 'points': 3.0, 'description': 'Reinforce'}, {'id': '76864_3528', 'points': 1.0, 'description': 'Introduce'}, {'id': '76864_2006', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '76864_5964', 'points': 0.0, 'description': 'N/A'}]},
        'Values/Ethics': {'id': '76864_7039', 'description': 'Values/Ethics', 'ratings': [{'id': '76864_3686', 'points': 5.0, 'description': 'Practice'}, {'id': '76864_4779', 'points': 3.0, 'description': 'Reinforce'}, {'id': '76864_3388', 'points': 1.0, 'description': 'Introduce'}, {'id': '76864_8567', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '76864_6509', 'points': 0.0, 'description': 'N/A'}]}
    }
