import pandas as pd
import pytest
from constants import COL_COURSE_ID

@pytest.fixture(scope="module")
def dummy_df():
  data = [['History', 234455], ['Math', 2345], ['Science', 12345], ['English', 22345], ['Art', 32345], ['Physics', 'Shell'], ['Chemistry', 'n/a']]
  return pd.DataFrame(data, columns = ['Name', COL_COURSE_ID])
