# src/function_selector.py

import numpy as np
import pandas as pd
import logging
from database import DatabaseManager
from exceptions import FunctionSelectionError

class FunctionSelector:
    """
    Handles the selection of ideal functions that best fit the given training data
    using the least-squares criterion.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the FunctionSelector with a DatabaseManager.
        
        :param db_manager: An instance of DatabaseManager.
        """
        self.db_manager = db_manager
        self.session = self.db_manager.get_session()
        self.selected_functions = []
        self.max_deviations = []

    def calculate_least_squares(self) -> None:
        """
        Calculate and select the ideal functions that minimize the sum of squared deviations 
        for each training function. Also, store the maximum allowed deviations for test mapping.
        
        Steps:
        1. Load training_data and ideal_functions into DataFrames.
        2. Compute sum of squared errors (SSE) for each ideal function against each training function.
        3. Select the ideal function with the minimum SSE for each of the 4 training functions.
        4. Compute max deviation limits for test mapping.
        
        :raises FunctionSelectionError: If training or ideal data is missing or invalid.
        """
        try:
            training_df = pd.read_sql_table('training_data', self.db_manager.engine)
            ideal_df = pd.read_sql_table('ideal_functions', self.db_manager.engine)
        except Exception as e:
            raise FunctionSelectionError(f"Error reading data from database: {e}")

        if training_df.empty:
            logging.error("Training data is empty. Cannot select functions.")
            return

        # Verify required columns in training data
        required_training_cols = ['y1', 'y2', 'y3', 'y4']
        for col in required_training_cols:
            if col not in training_df.columns:
                logging.error(f"Column '{col}' missing in training_data.")
                return

        # Verify required columns in ideal functions
        required_ideal_cols = [f'y{i}' for i in range(1, 51)]
        for col in required_ideal_cols:
            if col not in ideal_df.columns:
                logging.error(f"Column '{col}' missing in ideal_functions.")
                return

        # Calculate SSE (Sum of Squared Errors)
        deviations = np.zeros((4, 50))  # 4 training funcs vs 50 ideal funcs
        for i in range(1, 5):
            y_train = training_df[f'y{i}']
            for j in range(1, 51):
                y_ideal = ideal_df[f'y{j}']
                # Ensure equal lengths (if needed, align by x)
                # Here we assume identical x-sets for simplicity
                deviations[i - 1, j - 1] = np.sum((y_train - y_ideal) ** 2)

        # Select ideal functions with minimum SSE for each training function
        for i in range(4):
            min_idx = np.argmin(deviations[i])
            chosen_func = min_idx + 1  # Function numbering starts at 1
            self.selected_functions.append(chosen_func)
            # Max deviation for mapping: SSE_min * sqrt(2) as per given criterion
            self.max_deviations.append(deviations[i][min_idx] * np.sqrt(2))

        logging.info(f"Selected Ideal Functions: {self.selected_functions}")
        logging.info(f"Max Deviations: {self.max_deviations}")

    def get_selected_functions(self) -> list:
        """
        Get the list of selected ideal functions.
        
        :return: A list of integers representing the selected ideal functions.
        """
        return self.selected_functions

    def get_max_deviations(self) -> list:
        """
        Get the list of max deviations corresponding to each selected ideal function.
        
        :return: A list of floats representing max allowed deviations.
        """
        return self.max_deviations
