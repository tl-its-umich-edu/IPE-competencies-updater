import logging, json, pandas as pd
from typing import Any, Dict, List, Tuple, Union
from requests import Response
from dataclasses import dataclass, fields
from api_handler.api_calls import APIHandler
from ipe_process_orchestrator.api_helper import response_none_check
from constants import (
  CANVAS_URL_BEGIN, COL_COURSE_ID, COL_DOSAGE,FULL_DOSE, NO_DOSE, COL_ASSIGNING_LO_CRITERIA, AC_70_PERCENT_GRADE, AC_ALL_ENROLLED, COMPETENCY_ASSIGNING_COURSE_GRADE)
logger = logging.getLogger(__name__)


@dataclass
class IPECompetenciesAssigner:
    api_handler: APIHandler 
    assignment_id: int
    course: pd.Series
    rubric_data: Dict[str, Any]

    
    def get_student_list_with_course_grades(self) -> List[Dict[str, Any]]:
      more_pages: bool = True
      page_num: int = 1
      students_with_grades: List[Dict[str, Any]] = list()
      course_id = self.course[COL_COURSE_ID]
      student_data_url = f'{CANVAS_URL_BEGIN}/courses/{course_id}/enrollments'
      student_list_payload = {'type[]':'StudentEnrollment', 'state[]': 'active','per_page': 100}
      
      while more_pages:
        logging.debug(f'Page number {page_num}')
        student_data_resp: Response = self.api_handler.api_call_with_retries(student_data_url, 'GET',student_list_payload)
        err_msg:str =  f'Error in getting the student enrollment with grades for course {course_id}'
        response_none_check(student_data_resp, err_msg)
        
        student_response_json = json.loads(student_data_resp.text)
        logger.info(f'Student response json is {student_response_json}')
        
        for student in student_response_json:
          student_obj = {
            'student_canvas_id': student['user_id'], 
            'student_name':student['user']['name'],
            'grade': student['grades']['final_score']
            }
          students_with_grades.append(student_obj)
        
        page_info: Union[None, Dict[str, Any]] = self.api_handler.get_next_page(student_data_resp)
        logging.debug(f'Next Page URL params: {page_info}')
        
        if not page_info:
            more_pages = False
        else:
            logging.debug(f'Params for next page: {page_info}')
            student_list_payload = page_info
            page_num += 1
        
      logging.info(f'Students with grades for course {course_id} are {len(students_with_grades)}')
      return students_with_grades
      
    def get_competency_payload(self) -> Dict[str, Any]:
      competency_payload: Dict[str, Any] = dict()
      for rubric_key, rubric_value in self.rubric_data.items():
        competency_asignment_value = self.course[rubric_key]
        logger.info(f'Competency assignment value is {competency_asignment_value} for competencies {rubric_key}')
        competency_id = rubric_value['id']
        competency_ratings = rubric_value['ratings']
        if not rubric_key == COL_DOSAGE:
          for rating in competency_ratings:
            if rating['description'] == competency_asignment_value:
              competency_payload[f"rubric_assessment[{competency_id}][rating_id]"] = rating['id']
              competency_payload[f"rubric_assessment[{competency_id}][points]"] = rating['points']
              break
        else:
          # this is the case for the dosage
            if competency_asignment_value:
              rating = next(rating for rating in competency_ratings if rating['description'] == FULL_DOSE)
              competency_payload[f"rubric_assessment[{competency_id}][rating_id]"] = rating['id']
              competency_payload[f"rubric_assessment[{competency_id}][points]"] = competency_asignment_value
            else:
              rating = next(rating for rating in competency_ratings if rating['description'] == NO_DOSE)
              competency_payload[f"rubric_assessment[{competency_id}][rating_id]"] = rating['id']
              competency_payload[f"rubric_assessment[{competency_id}][points]"] = 0
      logger.info(f'Competency payload is {competency_payload}')
      return competency_payload

    def get_student_list_to_receive_competencies(self, student_grades) -> List[Dict[str, Any]]:
      """
      returns the list of students who will receive competencies. If the Criteria is All Enrolled, then all the students will be returned. 
      If the criteria is 70% grade, then only the students with 70% grade will be returned.
      """
      assignment_criteria = self.course[COL_ASSIGNING_LO_CRITERIA]
      if assignment_criteria == AC_ALL_ENROLLED:
        logger.info(f'Assigning competencies to all students {len(student_grades)} in course {self.course[COL_COURSE_ID]}')
        return student_grades
      elif assignment_criteria == AC_70_PERCENT_GRADE:
        students_greater_than_70_percent_grade = [student for student in student_grades if student['grade'] >= COMPETENCY_ASSIGNING_COURSE_GRADE]
        logger.info(f'Assigning competencies to students with 70 percent grade {len(students_greater_than_70_percent_grade)} in course {self.course[COL_COURSE_ID]}')
        return students_greater_than_70_percent_grade
      
    def assign_competancies(self, students_grades) -> None:
      course_id = self.course[COL_COURSE_ID]
      competency_assign_payload = self.get_competency_payload()
      students_for_assigning_competencies: List[Dict[str, Any]] = self.get_student_list_to_receive_competencies(students_grades)
      
      for student in students_for_assigning_competencies:
        student_id = student['student_canvas_id']
        student_name = student['student_name']
        
        assigning_rubrics_url= f'{CANVAS_URL_BEGIN}/courses/{course_id}/assignments/{self.assignment_id}/submissions/{student_id}'
        resp = self.api_handler.api_call_with_retries(assigning_rubrics_url, 'PUT', competency_assign_payload)
        err_msg = f'Error assigning competancies for student {student_name} id: {student_id} assignment: {self.assignment_id} course {course_id}'
        if resp is None:
          logger.error(err_msg)
          continue

        logger.info(f'Assigned competancies for student: {student_name} id: {student_id} assignment: {self.assignment_id} course {course_id}')

    
    def start_assigning_process(self) -> None:
      
      student_grades: List[Dict[str, Any]] = self.get_student_list_with_course_grades()
      logger.debug(f'Students with grades are {student_grades}')
      self.assign_competancies(student_grades)