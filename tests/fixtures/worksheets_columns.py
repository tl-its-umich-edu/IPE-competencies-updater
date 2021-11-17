from typing import List
import pytest
import pandas as pd


@pytest.fixture(scope="module")
def worksheet_columns() -> List[str]:
    """
    Sample worksheet columns
    """
    return ['Offering Name', 'Offering ID', 'Offering-instance ID', 'Year', 'Term',
            'UM Term Code', 'udp_term_name', 'Description', 'Lead Faculty Member 1',
            'Lead Faculty Member 2', 'Lead Faculty 1 School',
            'Lead Faculty 2 School', 'Lead Faculty 1 unique name',
            'Lead Faculty 2 unique name', 'Format',
            'Instructional Team (SEE LOOKUP TABLE)',
            'Program offering to students (SEE LOOKUP TABLE)',
            'Course #s (if applicable)', 'Window used', 'IPE Assessments',
            'Canvas Site or Shell Course', 'Canvas Course ID',
            'Roles/ Responsibilities', 'Interprofessional Communication',
            'Teams/Teamwork', 'Values/Ethics', 'Intercultural Humility',
            'Dosage (contact hours)', 'Criteria for Assigning Outcomes in Canvas',
            'Notes', 'When does script run? (Feb, June, Oct)', 'Script Run?']


@pytest.fixture(scope="module")
def worksheet_columns_with_whitespace() -> pd.Index:
    """
    This test make sure that ipe spread sheets columns whitespaces are trimmed
    """
    return pd.Index(['Offering Name', 'Offering ID', 'Offering-instance ID', 'Year', 'Term ',
                     'UM Term Code', 'udp_term_name', 'Description', 'Lead Faculty Member 1',
                     'Lead Faculty Member 2', 'Lead Faculty 1 School',
                     'Lead Faculty 2 School', 'Lead Faculty 1 unique name',
                     'Lead Faculty 2 unique name', 'Format',
                     'Instructional Team (SEE LOOKUP TABLE)',
                     'Program offering to students (SEE LOOKUP TABLE)',
                     'Course #s (if applicable)', 'Window used', 'IPE Assessments',
                     'Canvas Site or Shell Course', 'Canvas Course ID',
                     'Roles/ Responsibilities ', 'Interprofessional Communication ',
                     'Teams/Teamwork ', 'Values/Ethics ', 'Intercultural Humility',
                     'Dosage (contact hours) ', 'Criteria for Assigning Outcomes in Canvas',
                     'Notes', 'When does script run? (Feb, June, Oct)', 'Script Run?'])
