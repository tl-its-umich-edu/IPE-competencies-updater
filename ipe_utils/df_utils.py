import pandas as pd
from datetime import datetime
from constants import (WHEN_TO_RUN_SCRIPT, SCRIPT_RUN, COL_COURSE_ID, COL_DOSAGE, COMPETENCIES_VAL_INTRODUCE,
COMPETENCIES_VAL_NONE, COMPETENCIES_VAL_PRACTICE, COMPETENCIES_VAL_REINFORCE,COL_ASSIGNING_LO_CRITERIA, 
COL_COMPETENCIES_RR, COL_COMPETENCIES_TTW, COL_COMPETENCIES_IC, COL_COMPETENCIES_VE, COL_COMPETENCIES_IH, AC_70_PERCENT_GRADE, AC_ALL_ENROLLED)
import logging
from pytz import timezone

logger = logging.getLogger(__name__)

def df_columns_strip(df_columns: pd.Index) -> pd.Index:
    """
    Strip whitespace from column names.
    """
    return df_columns.str.strip() #type: ignore

def df_remove_non_course_id(df: pd.DataFrame) -> pd.DataFrame: 
    """
    Remove non canvas course IDs from a course ID column like Shell, empty space, n/a.
    """
    logging.info(f'{len(df)} rows before removing non course IDs')
    df_with_coursesId = df.loc[df[COL_COURSE_ID].apply(
        pd.to_numeric, errors='coerce').notnull()]
    return df_with_coursesId

def df_dosage_clean_up(df: pd.DataFrame) -> pd.DataFrame:
    """
    Dosage values should be  number, and in between 0 and 100.
    """
    df_dosage_to_numeric = df.loc[df[COL_DOSAGE].apply(pd.to_numeric, errors='coerce').notnull()]
    df_dosage_to_numeric[COL_DOSAGE] = pd.to_numeric(df_dosage_to_numeric[COL_DOSAGE], downcast="float")
    return df_dosage_to_numeric[(0 <= df_dosage_to_numeric[COL_DOSAGE]) & (df_dosage_to_numeric[COL_DOSAGE] <= 100)]

def df_filter_courses_no_competencies_dosage_criteria_values(df: pd.DataFrame) -> pd.DataFrame:
    """
     Remove courses with non numeric dosage values like empty space, n/a, randam string.
     Remove courses competencies values other than Practice, Eeinforce, Introduce, n/a.
     Remove courses with do not run criteria for assigning LO's.
    """
    comp_val = [COMPETENCIES_VAL_NONE, COMPETENCIES_VAL_PRACTICE, COMPETENCIES_VAL_REINFORCE, COMPETENCIES_VAL_INTRODUCE]
    criteria_val = [AC_70_PERCENT_GRADE, AC_ALL_ENROLLED]
    df = df_dosage_clean_up(df)
    return df.loc[df[COL_COMPETENCIES_TTW].isin(comp_val) & df[COL_COMPETENCIES_VE].isin(comp_val) & df[COL_COMPETENCIES_IC].isin(comp_val)
               & df[COL_COMPETENCIES_IH].isin(comp_val) & df[COL_COMPETENCIES_RR].isin(comp_val) & df[COL_ASSIGNING_LO_CRITERIA].isin(criteria_val)]

def df_filter_course_based_on_month(df: pd.DataFrame, month: str) -> pd.DataFrame:
    """
    Filter a dataframe based on given month value and script run column is empty.
    Converting all months to lower case since this is typed by hand in the sheet instead of dropdown.
    """
    df = df.loc[(df[WHEN_TO_RUN_SCRIPT].str.lower().str.strip() == month.lower().strip()) & (df[SCRIPT_RUN] == '')]
    df_few = df[[COL_COURSE_ID, COL_DOSAGE, COL_COMPETENCIES_IC, COL_COMPETENCIES_IH, COL_COMPETENCIES_RR, COL_COMPETENCIES_TTW, COL_COMPETENCIES_VE, COL_ASSIGNING_LO_CRITERIA]]
    return df_few

def df_filter_course_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate course id's from a dataframe. the dataframe will have below column headers
    COL_COURSE_ID, COL_DOSAGE, COL_COMPETENCIES_IC, COL_COMPETENCIES_IH, COL_COMPETENCIES_RR, COL_COMPETENCIES_TTW, COL_COMPETENCIES_VE, COL_ASSIGNING_LO_CRITERIA

    1. The first drop duplicates will remove exact match of duplicate rows but keep just one.
    2. The second drop duplicates will remove all rows with same course id. This is case when an IPE offerning has same course id 
       but with in different dosage, competencies, criteria value. This case is hard to tell which competencies need to assign to the course. 
       So we just drop all these ambiguous courses id's.
    """
    df = df.drop_duplicates()
    df = df.drop_duplicates(subset=[COL_COURSE_ID], keep = False)
    return df

def current_time()-> str:
    """
    Return current time in format: YYYY-MM-DD HH:MM:SS
    """
    est = timezone('US/Eastern')
    return datetime.now(est).strftime('%Y-%m-%d %H:%M:%S')
