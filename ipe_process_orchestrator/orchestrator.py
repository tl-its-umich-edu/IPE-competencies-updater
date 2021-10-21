import logging, sys
import pandas as pd
from ipe_utils.df_utils import df_columns_strip, df_remove_non_course_id
from ipe_process_orchestrator.assignment_flow import IPEAssignmentFlow
from umich_api.api_utils import ApiUtil


logger = logging.getLogger(__name__)
class IPECompetenciesOrchestrator:
    CANVAS_COURSE_ID_COLUMN = 'Canvas Course ID'
    
    def __init__(self, original_df, props) -> None:
        """
        Initialize the orchestrator
        """
        self.orginal_df: pd.DataFrame = original_df
        self.props = props
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
    
    def _create_delete_assignment(self, course_id):
        """
        Create the new IPE assignment with name 
        """
        IPEAssignmentFlow(self.props, course_id)
        pass
    
    def _assign_IPE_competencies(self):
        pass
        


    
    def start_composing_process(self):
        """
        This is the place where all the IPE process flow will be orchestrated.
        """
        self._clean_up_ipe_dataframe()
        