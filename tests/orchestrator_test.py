import pandas as pd
from ipe_process_orchestrator.orchestrator import IPECompetenciesOrchestrator

def test_competancies_values_not_empty(single_ipe_offering, ipe_props, api_handler):
    """
    This tests if the competancies values are not empty
    """
    single_ipe_offering['Dosage (contact hours)'] = ''
    single_ipe_offering['Intercultural Humility'] = ''
    single_ipe_offering['Interprofessional Communication'] = ''
    single_ipe_offering['Roles/Responsibilities'] = ''
    single_ipe_offering['Team/Teamwork'] = 'Introduce'
    single_ipe_offering['Values/Ethics'] = ''
    single_ipe_offering['COL_ASSIGNING_LO_CRITERIA'] = ''
    course = pd.Series(single_ipe_offering)
    check_status = IPECompetenciesOrchestrator(ipe_props, pd.DataFrame(), api_handler).check_competencies_values_given_gsheet(course)
    assert check_status == False