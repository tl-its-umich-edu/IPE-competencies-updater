import logging, sys
from typing import Any, Dict
import pandas as pd
from ipe_utils.df_utils import df_columns_strip, df_remove_non_course_id
from ipe_process_orchestrator.assignment_flow import IPEAssignmentFlow
from ipe_process_orchestrator.get_rubric_data import IPERubricDataMapping
from ipe_process_orchestrator.assigning_competencies import IPECompetenciesEntruster
from api_handler.api_calls import APIHandler
from constants import ( 
    COL_COURSE_ID, COL_ASSIGNING_LO_CRITERIA, AC_DO_NOT_RUN
    )


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
    
    
    def _clean_up_ipe_dataframe(self):
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
    
    def _create_delete_assignment(self, course) -> str:
        """
        Create the new IPE assignment if such assignment does not exist or delete the existing one if it exists. This action
        is as a result of copied course and so delete the existing assignment is the best option.
        """
        course_id = course[COL_COURSE_ID]
        rubric_id = self.props['rubric_id']
        assignment_flow = IPEAssignmentFlow(self.api_handler, course_id, rubric_id)
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
            rubric_data = IPERubricDataMapping(self.api_handler, rubric_account_id, rubric_id).fetch_rubric_api()
            return rubric_data
        except Exception as e:
            logger.error(f'Error in getting_rubrics: {e}')
            sys.exit(1)
            
    
    def start_competencies_assigning_process(self, course, rubric_data):
        try:
            if course[COL_ASSIGNING_LO_CRITERIA] == AC_DO_NOT_RUN:
                logger.info(f'Course {course[COL_COURSE_ID]} is not eligible for competencies assigning process')
                return
            # assignment_id = self._create_delete_assignment(course)
            # if course[COL_COURSE_ID] == 249168 or course[COL_COURSE_ID] == 307473 or course[COL_COURSE_ID] == 176535:
            if course[COL_COURSE_ID] == 307473:
                IPECompetenciesEntruster(self.api_handler, 1538154, course, rubric_data).start_assigning_process()
        except Exception as e:
            logger.error(e)
    
    def start_composing_process(self):
        """
        This is the place where all the IPE process flow will be orchestrated.
        """
        self._clean_up_ipe_dataframe()
        print(list(self.filter_df_course_ids['Canvas Course ID']))
        rubrics_data: Dict[str, Any] = self.getting_rubrics()
        self.filter_df_course_ids.apply(lambda course: self.start_competencies_assigning_process(course, rubrics_data), axis=1)
        