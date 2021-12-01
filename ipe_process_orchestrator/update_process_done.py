import logging, time
from typing import Dict, List, Optional
import pandas as pd
from gspread.models import Worksheet, Cell
from gspread.exceptions import APIError
from constants import (COL_COURSE_ID)
from ipe_utils.df_utils import current_time
logger = logging.getLogger(__name__)

class UpdateProcessDone(object):
    def __init__(self, props: Dict[str, Optional[str]], course: pd.Series, worksheet: Worksheet, script_run_column_value: int):
      self.props = props
      self.course = course
      self.worksheet = worksheet
      self.script_run_column_value = script_run_column_value
    
    def update_process_run_finished(self):
      """
      This function updates google sheets Script Run? column once competencies assignment is done for a particulate course
      The step will include
      1. Search for the course in present context, get the Cell values of it
      2. Update the Script Run? column with the date and time
      """ 
      courses_to_update = list()
      run_loop_when_rate_limiting = True
      count = 1
      while run_loop_when_rate_limiting and count <= int(self.props.get('retry_attempts')):
        try:
        # if a course is entered in multiple rows, then update all the rows script run? column
          courses_list: List[Cell] = self.worksheet.findall(str(self.course[COL_COURSE_ID]))
          for course in courses_list:
            row = course.row
            courses_to_update.append(Cell(row=row, col=self.script_run_column_value, value=current_time()))
          
          self.worksheet.update_cells(courses_to_update)
          run_loop_when_rate_limiting = False
        except (APIError, Exception) as e:
          if isinstance(e, APIError):
            logger.error(f"Possibly hit the Google API rate limits when updating process finished for course {self.course[COL_COURSE_ID]}, more details {e}")
            count += 1
            time.sleep(int(self.props.get('wait_limit')))
          else:
            logger.error(f"Error updating process finished for for courses {self.course[COL_COURSE_ID]}, more details {e}")

      
