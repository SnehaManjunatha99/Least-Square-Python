# src/test_mapper.py

import pandas as pd
import logging
from database import DatabaseManager
from exceptions import TestMappingError
from sqlalchemy.exc import SQLAlchemyError

class TestMapper:
    """
    Maps test data points to the selected ideal functions if the deviation criteria are met.
    """

    def __init__(self, db_manager: DatabaseManager, function_selector):
        """
        Initialize the TestMapper with a DatabaseManager and a FunctionSelector.
        
        :param db_manager: An instance of DatabaseManager.
        :param function_selector: An instance of FunctionSelector to obtain selected functions and deviations.
        """
        self.db_manager = db_manager
        self.function_selector = function_selector
        self.session = self.db_manager.get_session()

    def map_test_data(self) -> None:
        """
        Map each test data point to one of the selected ideal functions if its deviation does not exceed
        the allowed max deviation.
        
        Steps:
        1. Retrieve selected functions and their max deviations.
        2. For each test data point, find the ideal function value, compute deviation.
        3. Assign the test point to the ideal function if deviation <= max_deviation.
        4. Save all assigned test points into 'test_results' table.
        
        :raises TestMappingError: If there's an error during the mapping process.
        """
        selected = self.function_selector.get_selected_functions()
        max_devs = self.function_selector.get_max_deviations()

        if not selected or not max_devs:
            logging.info("No ideal functions selected. Skipping test data mapping.")
            return

        try:
            test_df = pd.read_sql_table('test_data', self.db_manager.engine)
            ideal_df = pd.read_sql_table('ideal_functions', self.db_manager.engine)
        except SQLAlchemyError as e:
            raise TestMappingError(f"Error reading from database: {e}")

        results = []
        for _, test_row in test_df.iterrows():
            x_val = test_row['x']
            y_val = test_row['y']
            deviations = []

            # Find deviations for each selected ideal function
            for idx, func_no in enumerate(selected):
                # Find ideal y for the given x
                ideal_subset = ideal_df[ideal_df['x'] == x_val]
                if ideal_subset.empty:
                    # If exact x not found, choose the closest x
                    nearest_idx = (ideal_df['x'] - x_val).abs().idxmin()
                    ideal_y = ideal_df.at[nearest_idx, f'y{func_no}']
                else:
                    ideal_y = ideal_subset.iloc[0][f'y{func_no}']

                deviation = abs(y_val - ideal_y)
                deviations.append(deviation)

            # Determine best fit function
            if deviations:
                min_dev = min(deviations)
                best_func_index = deviations.index(min_dev)
                best_func = selected[best_func_index]

                # Check against max deviation threshold
                if min_dev <= max_devs[best_func_index]:
                    results.append({
                        'x': x_val,
                        'y': y_val,
                        'delta_y': min_dev,
                        'ideal_function': best_func
                    })

        if results:
            results_df = pd.DataFrame(results)
            try:
                results_df.to_sql('test_results', self.db_manager.engine, if_exists='replace', index=False)
                logging.info("Test data mapping completed. Results stored in 'test_results'.")
            except SQLAlchemyError as e:
                raise TestMappingError(f"Error writing test results to database: {e}")
        else:
            logging.info("No test data points matched the deviation criteria.")
