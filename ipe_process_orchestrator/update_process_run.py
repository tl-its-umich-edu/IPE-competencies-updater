class UpdateProcessRun(object):
    def __init__(self, course):
      self.course = course
    
    def update_process_run_finished(self, process_run_id, process_run_status):
      """
      This function updates google sheets Script Run? column once competencies assignment is done for a particulate course
      The step will include
      1. Search for the course in present context, get the Cell values of it
      2. Update the Script Run? column with the date and time
      """ 
      
