import logging
from typing import List
import pandas as pd
from gspread.models import Worksheet, Cell
from constants import (COL_COURSE_ID)
from ipe_utils.df_utils import current_time
logger = logging.getLogger(__name__)
class UpdateProcessRun(object):
    def __init__(self, course: pd.Series, worksheet: Worksheet, script_run_column_value: int):
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
      try:
      # if a course is entered in multiple rows, then update all the rows script run? column
        courses_list: List[Cell] = self.worksheet.findall(str(self.course[COL_COURSE_ID]))
        for course in courses_list:
          row = course.row
          courses_to_update.append(Cell(row=row, col=self.script_run_column_value, value=current_time()))
        
        a = self.worksheet.update_cells(courses_to_update)
        logger.info(a)
      except Exception as e:
        logger.error(f"Error in updating the Script Run? column for course {self.course[COL_COURSE_ID]}")

      
