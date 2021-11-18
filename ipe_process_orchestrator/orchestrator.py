import logging
import sys
from typing import Any, Dict, NoReturn, Union
import pandas as pd
from ipe_utils.df_utils import df_columns_strip, df_remove_non_course_id
from ipe_process_orchestrator.assignment_flow import IPEAssignmentFlow
from ipe_process_orchestrator.rubric_data import IPERubricSimplified
from ipe_process_orchestrator.assign_competencies import IPECompetenciesAssigner
from api_handler.api_calls import APIHandler
from constants import (COL_COURSE_ID, COL_COMPETENCIES_RR, COL_COMPETENCIES_TTW, COL_COMPETENCIES_IC,
                       COL_COMPETENCIES_VE, COL_COMPETENCIES_IH, COL_DOSAGE)

logger = logging.getLogger(__name__)


class IPECompetenciesOrchestrator:
    def __init__(self, props, original_df, api_handler) -> None:
        """
        Initialize the orchestrator
        """
        self.orginal_df: pd.DataFrame = original_df
        self.props = props
        self.api_handler: APIHandler = api_handler
        self.filter_df_course_ids = pd.DataFrame()

    def _clean_up_ipe_dataframe(self) -> None:
        """
        Clean up the dataframe
        1. leading and trailing spaces df.columns
        2. only courses id list with values that are numbers. Removes Shell, shell, empty, n/a, shell(23333)
        3. the original dataframe will remain same and the filtered dataframe will be created with courseIds

        """
        try:
            self.orginal_df.columns = df_columns_strip(self.orginal_df.columns)
            cleaned_up_df = df_remove_non_course_id(self.orginal_df)
            self.filter_df_course_ids = cleaned_up_df
        except Exception as e:
            logger.error(f'Error in clean_up_ipe_dataframe: {e}')
            sys.exit(1)

    def _create_delete_assignment(self, course: pd.Series) -> Union[NoReturn, str]:
        """
        Create the new IPE assignment if such assignment does not exist or delete the existing one if it exists. This action
        is as a result of copied course and so delete the existing assignment is the best option.
        """
        course_id = course[COL_COURSE_ID]
        rubric_id = self.props['rubric_id']
        assignment_flow = IPEAssignmentFlow(
            self.api_handler, course_id, rubric_id)
        try:
            assignment_id: str = assignment_flow.start_assignment_flow()
            return assignment_id
        except Exception as e:
            raise e

    def getting_rubrics(self):
        """
        Get the rubric data from the API
        """
        try:
            rubric_account_id: int = self.props['rubric_account_id']
            rubric_id: int = self.props['rubric_id']
            rubric_data = IPERubricSimplified(
                self.api_handler, rubric_account_id, rubric_id).fetch_rubric_api()
            return rubric_data
        except Exception as e:
            logger.error(f'Error in getting_rubrics: {e}')
            sys.exit(1)

    def check_competencies_values_given_gsheet(self, course: pd.Series) -> None:
        """
        Check if the competencies values are given in the Google Sheet. If not, then exit the process.
        Not a real life usecase, just checking for sanity.
        """
        try:
            if(course[COL_COMPETENCIES_RR] and course[COL_COMPETENCIES_TTW] and course[COL_COMPETENCIES_IC] and
               course[COL_COMPETENCIES_VE] and course[COL_COMPETENCIES_IH] and course[COL_DOSAGE]):
                return True
            else: 
              logger.error(f'Competencies values some or all not given in the Google Sheet for course: {course[COL_COURSE_ID]}')
              return False
        except Exception as e:
            logger.error(f'Error in getting the ipe competencies values from Google Sheet for course {course[COL_COURSE_ID]}: {e}')
            return False

    def start_competencies_assigning_process(self, course: pd.Series, rubric_data) -> None:
        """
        First step in the assiging competencies process is to create the asssignment if it does not exist.
        Second step is to assign competencies to the assignment.
        Thrid step is to update the status in Google Sheets that the competencies are assigned.
        """
        try:
            if not self.check_competencies_values_given_gsheet(course):
              return
            assignment_id = self._create_delete_assignment(course)
            IPECompetenciesAssigner(
                self.api_handler, assignment_id, course, rubric_data).start_assigning_process()
        except Exception as e:
            logger.error(e)

    def start_composing_process(self):
        """
        This is the place where all the IPE process flow will be orchestrated.
        """
        self._clean_up_ipe_dataframe()
        rubric_data: Dict[str, Any] = self.getting_rubrics()
        logger.debug(f'Rubric data: {rubric_data}')
        self.filter_df_course_ids.apply(
            lambda course: self.start_competencies_assigning_process(course, rubric_data), axis=1)
