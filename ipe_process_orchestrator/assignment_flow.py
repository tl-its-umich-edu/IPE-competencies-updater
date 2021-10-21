from umich_api.api_utils import ApiUtil
import logging

logger = logging.getLogger(__name__)
class IPEAssignmentFlow:
    ASSIGNMENT_NAME = 'IPE Competencies Attained'
    ASSIGNMENT_GROUP_NAME ='IPE Competencies'
    
    def __init__(self, props, course_id) -> None:
        self.props = props
        self.course_id = course_id
    
    def _look_up_assignment_by_name(self):
        pass
    def _create_assignment(self):

       

        pass
    def _delete_assignment(self):
        pass
    def _assign_ipe_rubrics(self):
        pass
    
    def start_assignment_flow(self):
        self._look_up_assignment_by_name()
        self._delete_assignment()
        self._create_assignment()
        self._assign_ipe_rubrics()
    