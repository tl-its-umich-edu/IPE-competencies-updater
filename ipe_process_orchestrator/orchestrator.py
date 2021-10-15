import logging
import pandas as pd


logger = logging.getLogger(__name__)
class IPECompetenciesOrchestrator:
    def __init__(self, worksheet_df, props) -> None:
        """
        Initialize the orchestrator
        """
        self.worksheet_df: pd.DataFrame = worksheet_df
        self.props = props
    
    def clean_up_df(self):
        """
        Clean up the dataframe
        1. leading and trailing spaces df.columns
        2. courses id list with values Shell, shell, empty, n/a, shell(23333)

        """
        self.worksheet_df.columns = self.worksheet_df.columns.df_columns_strip()

        pass
    
    def start_composing_process(self):
        """
        This is the place where all the IPE process flow will be orchestrated.
        """
        self.clean_up_df()
        pass