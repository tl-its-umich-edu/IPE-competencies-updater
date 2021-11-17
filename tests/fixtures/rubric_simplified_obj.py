import pytest


@pytest.fixture(scope="module")
def rubric_simple():
    """
    simplified rubric object
    """
    return {
        'Dosage (contact hours)': {'id': '_123', 'description': 'Dosage (contact hours)', 'ratings': [{'id': 'blank', 'points': 100.0, 'description': 'Full dose'}, {'id': 'blank_2', 'points': 0.0, 'description': 'No dose'}]},
        'Intercultural Humility': {'id': '456_345', 'description': 'Intercultural Humility', 'ratings': [{'id': '_2560', 'points': 5.0, 'description': 'Practice'}, {'id': '_2561', 'points': 3.0, 'description': 'Reinforce'}, {'id': '_2562', 'points': 1.0, 'description': 'Introduce'}, {'id': '_2563', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '_2564', 'points': 0.0, 'description': 'N/A'}]},
        'Interprofessional Communication': {'id': '456_678', 'description': 'Interprofessional Communication', 'ratings': [{'id': '_2565', 'points': 5.0, 'description': 'Practice'}, {'id': '_2566', 'points': 3.0, 'description': 'Reinforce'}, {'id': '_2567', 'points': 1.0, 'description': 'Introduce'}, {'id': '_2568', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '_2569', 'points': 0.0, 'description': 'N/A'}]},
        'Roles/Responsibilities': {'id': '456_901', 'description': 'Roles/Responsibilities', 'ratings': [{'id': '_2570', 'points': 5.0, 'description': 'Practice'}, {'id': '_2571', 'points': 3.0, 'description': 'Reinforce'}, {'id': '_2572', 'points': 1.0, 'description': 'Introduce'}, {'id': '_2573', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '_2574', 'points': 0.0, 'description': 'N/A'}]},
        'Team/Teamwork': {'id': '456_902', 'description': 'Team/Teamwork', 'ratings': [{'id': '_2575', 'points': 5.0, 'description': 'Practice'}, {'id': '_2576', 'points': 3.0, 'description': 'Reinforce'}, {'id': '_2577', 'points': 1.0, 'description': 'Introduce'}, {'id': '_2578', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '_2579', 'points': 0.0, 'description': 'N/A'}]},
        'Values/Ethics': {'id': '456_903', 'description': 'Values/Ethics', 'ratings': [{'id': '_2580', 'points': 5.0, 'description': 'Practice'}, {'id': '_2581', 'points': 3.0, 'description': 'Reinforce'}, {'id': '_2582', 'points': 1.0, 'description': 'Introduce'}, {'id': '_2583', 'points': 0.5, 'description': 'Does Not Meet Competency'}, {'id': '_2584', 'points': 0.0, 'description': 'N/A'}]}
    }
