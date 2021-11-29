import logging, json, pandas as pd
import time, datetime
from typing import Any, Dict, List, Union
from requests import Response
from dataclasses import dataclass
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
      logger.info(f'Getting enrollments/grades for course {self.course[COL_COURSE_ID]}')
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
      logger.info(f'{len(students_with_grades)} active enrolled students may receive IPE competencies in the course {self.course[COL_COURSE_ID]}')
      return students_with_grades
      
    def get_competency_payload(self) -> Dict[str, Any]:
      competency_payload: Dict[str, Any] = dict()
      logger.info(f'Course: {self.course[COL_COURSE_ID]} enrollments will get competencies values as: {tuple([(key, self.course[key]) for key, value in self.rubric_data.items()])}')
      for rubric_key, rubric_value in self.rubric_data.items():
        competency_asignment_value = self.course[rubric_key]
        competency_id = rubric_value['id']
        competency_ratings = rubric_value['ratings']
        if rubric_key == COL_DOSAGE:
            if competency_asignment_value and competency_asignment_value > 0:
              rating = next(rating for rating in competency_ratings if rating['description'] == FULL_DOSE)
              competency_payload[f"rubric_assessment[{competency_id}][rating_id]"] = rating['id']
              competency_payload[f"rubric_assessment[{competency_id}][points]"] = competency_asignment_value
            else:
              rating = next(rating for rating in competency_ratings if rating['description'] == NO_DOSE)
              competency_payload[f"rubric_assessment[{competency_id}][rating_id]"] = rating['id']
              competency_payload[f"rubric_assessment[{competency_id}][points]"] = 0
        else:
          for rating in competency_ratings:
            if rating['description'] == competency_asignment_value:
              competency_payload[f"rubric_assessment[{competency_id}][rating_id]"] = rating['id']
              competency_payload[f"rubric_assessment[{competency_id}][points]"] = rating['points']
              break
          
      logger.debug(f'Competency payload is {competency_payload}')
      return competency_payload

    def get_student_list_to_receive_competencies(self, student_grades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
      """
      returns the list of students who will receive competencies. If the Criteria is `All Enrolled`, then all the students will be returned. 
      If the criteria is `70% grade`, then only the students with 70% grade will be returned.
      If student did not receive any grade like empty in Gradebook, the API returns a None value. 
      So we are checking for None value and then filtering the students based on graded
      """
      assignment_criteria = self.course[COL_ASSIGNING_LO_CRITERIA]
      if assignment_criteria == AC_ALL_ENROLLED:
        logger.info(f"For course {self.course[COL_COURSE_ID]} with competencies criteria: '{AC_ALL_ENROLLED}', {len(student_grades)} students will receive competencies")
        return student_grades
      elif assignment_criteria == AC_70_PERCENT_GRADE:
        students_greater_than_70_percent_grade = [student for student in student_grades if student['grade'] is not None and student['grade'] >= COMPETENCY_ASSIGNING_COURSE_GRADE]
        logger.info(f"For course {self.course[COL_COURSE_ID]} with competencies criteria: '{AC_70_PERCENT_GRADE}', {len(students_greater_than_70_percent_grade)}/{len(student_grades)} students will receive competencies")
        return students_greater_than_70_percent_grade
      else:return student_grades
      
    def assign_competancies(self, students_grades) -> None:
      course_id = self.course[COL_COURSE_ID]
      logger.info(f'Starting assigning competencies in course {course_id} to assignment {self.assignment_id} for {len(students_grades)} students.....')
      competency_assign_payload = self.get_competency_payload()
      students_for_assigning_competencies: List[Dict[str, Any]] = self.get_student_list_to_receive_competencies(students_grades)

      failed_students: List[Dict[int, str]] = list()
      
      for student in students_for_assigning_competencies:
        student_id = student['student_canvas_id']
        student_name = student['student_name']
        
        assigning_rubrics_url= f'{CANVAS_URL_BEGIN}/courses/{course_id}/assignments/{self.assignment_id}/submissions/{student_id}'
        resp = self.api_handler.api_call_with_retries(assigning_rubrics_url, 'PUT', competency_assign_payload)
        if resp is None:
          failed_students.append({student_id: student_name})
          continue

        logger.debug(f'Assigned competancies for student: {student_name} id: {student_id} assignment: {self.assignment_id} course {course_id}')
      
      if failed_students:
        logger.error(f"{len(students_grades)-len(failed_students)}/{len(students_grades)} students didn't got competancies assigned in course {course_id} in assignment {self.assignment_id}.")
        logger.error(failed_students)
    

    
    def start_assigning_process(self) -> None:
      logger.info(f'Assigning competencies for course {self.course[COL_COURSE_ID]} in assignment {self.assignment_id}')
      start_time = time.perf_counter()
      student_grades: List[Dict[str, Any]] = self.get_student_list_with_course_grades()
      if(len(student_grades) == 0):
        return
      self.assign_competancies(student_grades)
      end_time = time.perf_counter()
      logger.info(f"Assigning competencies for course {self.course[COL_COURSE_ID]} took {datetime.timedelta(seconds=(end_time - start_time))}")