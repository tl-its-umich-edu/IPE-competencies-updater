import logging
import sys
from typing import Any, Dict, Literal, NoReturn, Union
import pandas as pd
from ipe_utils.df_utils import df_columns_strip, df_remove_non_course_id, df_filter_course_based_on_month, df_filter_course_duplicates
from ipe_process_orchestrator.assignment_flow import IPEAssignmentFlow
from ipe_process_orchestrator.rubric_data import IPERubricSimplified
from ipe_process_orchestrator.assign_competencies import IPECompetenciesAssigner
from ipe_process_orchestrator.update_process_run import UpdateProcessRun
from gspread.models import Worksheet, Cell
from api_handler.api_calls import APIHandler
from constants import (COL_COURSE_ID, COL_COMPETENCIES_RR, COL_COMPETENCIES_TTW, COL_COMPETENCIES_IC,
                       COL_COMPETENCIES_VE, COL_COMPETENCIES_IH, COL_DOSAGE, COL_ASSIGNING_LO_CRITERIA,
                       SCRIPT_RUN)

logger = logging.getLogger(__name__)


class IPECompetenciesOrchestrator:
    def __init__(self, props, worksheet: Worksheet, api_handler) -> None:
        """
        Initialize the orchestrator
        """
        self.worksheet: Worksheet = worksheet
        self.original_df: pd.DataFrame = pd.DataFrame(worksheet.get_all_records())
        self.props = props
        self.api_handler: APIHandler = api_handler
        self.filter_df_course_ids = pd.DataFrame()

    def filter_course_list_to_run_and_cleanup(self) -> None:
        """
        1. this filter the courses that need to be run based on the 'Script Run?' and 'When does script run? (Feb, June, Oct) columns
        2. cleaning leading and trailing spaces df.columns
        3. only courses id list with values that are numbers. Removes Shell, shell, empty, n/a, shell(23333)
        4. drop the duplicates courses id's after the filtering 
        5. the original dataframe will remain same and the filtered dataframe will be created with courseIds
        """
        try:
            self.original_df.columns = df_columns_strip(self.original_df.columns)
            courses_to_run_df = df_filter_course_based_on_month(self.original_df, self.props['script_run_month'])
            cleaned_up_with_courses_df = df_remove_non_course_id(courses_to_run_df)
            pure_df_with_no_course_duplicates = df_filter_course_duplicates(cleaned_up_with_courses_df)
            self.filter_df_course_ids = pure_df_with_no_course_duplicates
            logger.info(f'{len(self.filter_df_course_ids[COL_COURSE_ID].tolist())} courses to run the IPE process: {self.filter_df_course_ids[COL_COURSE_ID].tolist()}')
        except Exception as e:
            logger.error(f'Error in when getting the courses based on the scrip run and when to run script columns: {e}')
            sys.exit(1)

    def _create_delete_assignment(self, course: pd.Series) -> Union[NoReturn, int]:
        """
        Create the new IPE assignment if such assignment does not exist or delete the existing one if it exists. This action
        is as a result of copied course and so delete the existing assignment is the best option.
        """
        course_id = course[COL_COURSE_ID]
        rubric_id = self.props['rubric_id']
        assignment_flow = IPEAssignmentFlow(
            self.api_handler, course_id, rubric_id)
        try:
            assignment_id: int = assignment_flow.start_assignment_flow()
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
    
    def get_script_run_column_value(self)-> int:
        single_cell_value: Cell = self.worksheet.findall(SCRIPT_RUN)[0]
        return single_cell_value.col

    def check_competencies_values_given_gsheet(self, course: pd.Series) -> Union[Literal[True], Literal[False]]:
        """
        Check if the competencies values are given in the Google Sheet. If not, then exit the process.
        Not a real life usecase, just checking for sanity.
        """
        try:
            if(course[COL_COMPETENCIES_RR] and course[COL_COMPETENCIES_TTW] and course[COL_COMPETENCIES_IC] and
               course[COL_COMPETENCIES_VE] and course[COL_COMPETENCIES_IH] and course[COL_DOSAGE] and course[COL_ASSIGNING_LO_CRITERIA]):
                return True
            else: 
              logger.error(f'Not all required competencies values are provided in the Google Sheet so skipping competency process for course: {course[COL_COURSE_ID]}')
              return False
        except Exception as e:
            logger.error(f'Error in getting the ipe competencies values from Google Sheet so skipping competency process for course {course[COL_COURSE_ID]}: {e}')
            return False

    def start_competencies_assigning_process(self, course: pd.Series, rubric_data: Dict[str, Any], script_run_column_value: int) -> None:
        """
        First step in the assiging competencies process is to create the asssignment if it does not exist.
        Second step is to assign competencies to the assignment.
        Third step is to update the status in Google Sheets that the competencies are assigned.
        """
        if not self.check_competencies_values_given_gsheet(course):
            return
        
        try:
            # if not self.check_competencies_values_given_gsheet(course):
            #   return
            # assignment_id: int = self._create_delete_assignment(course)
            # IPECompetenciesAssigner(
            #     self.api_handler, assignment_id, course, rubric_data).start_assigning_process()
            UpdateProcessRun(course, self.worksheet, script_run_column_value).update_process_run_finished()
            
        except Exception as e:
            logger.error(e)

    def start_composing_process(self):
        """
        This is the place where all the IPE process flow will be orchestrated.
        """
        self.filter_course_list_to_run_and_cleanup()
        if self.filter_df_course_ids.empty:
            return
        rubric_data: Dict[str, Any] = self.getting_rubrics()
        logger.debug(f'Rubric data: {rubric_data}')
        script_run_column_value: int = self.get_script_run_column_value()
        self.filter_df_course_ids.apply(
            lambda course: self.start_competencies_assigning_process(course, rubric_data, script_run_column_value), axis=1)
