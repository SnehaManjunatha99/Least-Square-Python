# tests/test_suite.py

import sys
import os
import unittest
import pandas as pd

# Add the src directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)

from function_selector import FunctionSelector
from database import DatabaseManager
from test_mapper import TestMapper

class TestIdealFunctionMapping(unittest.TestCase):
    def setUp(self):
        """
        Set up a fresh test database before each test.
        """
        self.db_manager = DatabaseManager('test_datasets.db')
        self.db_manager.create_tables()

    def tearDown(self):
        """
        Drop all tables after each test for isolation.
        """
        self.db_manager.drop_tables()

    def test_calculate_least_squares(self):
        """
        Ensure that FunctionSelector selects ideal functions correctly
        when given known data.
        """
        training_data = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1, 2, 3, 4],
            'y2': [2, 3, 4, 5],
            'y3': [3, 4, 5, 6],
            'y4': [4, 5, 6, 7]
        })
        ideal_functions = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1.1, 2.1, 3.1, 4.1],
            'y2': [2.2, 3.2, 4.2, 5.2],
            'y3': [3.3, 4.3, 5.3, 6.3],
            'y4': [4.4, 5.4, 6.4, 7.4],
            'y5': [5, 6, 7, 8],
        })
        # Add dummy columns up to y50
        for i in range(6, 51):
            ideal_functions[f'y{i}'] = ideal_functions['y5'] + i + 0.1

        training_data.to_sql('training_data', self.db_manager.engine, if_exists='replace', index=False)
        ideal_functions.to_sql('ideal_functions', self.db_manager.engine, if_exists='replace', index=False)

        selector = FunctionSelector(self.db_manager)
        selector.calculate_least_squares()
        selected = selector.get_selected_functions()

        self.assertEqual(len(selected), 4)
        self.assertTrue(all(1 <= func <= 50 for func in selected))
        self.assertListEqual(selected, [1, 2, 3, 4])

    def test_map_test_data(self):
        """
        Test that TestMapper correctly maps test data 
        when given known ideal functions.
        """
        training_data = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1, 2, 3, 4],
            'y2': [2, 3, 4, 5],
            'y3': [3, 4, 5, 6],
            'y4': [4, 5, 6, 7]
        })
        ideal_functions = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1.1, 2.1, 3.1, 4.1],
            'y2': [2.2, 3.2, 4.2, 5.2],
            'y3': [3.3, 4.3, 5.3, 6.3],
            'y4': [4.4, 5.4, 6.4, 7.4],
            'y5': [5, 6, 7, 8],
        })
        for i in range(6, 51):
            ideal_functions[f'y{i}'] = ideal_functions['y5'] + i + 0.1

        training_data.to_sql('training_data', self.db_manager.engine, if_exists='replace', index=False)
        ideal_functions.to_sql('ideal_functions', self.db_manager.engine, if_exists='replace', index=False)

        test_data = pd.DataFrame({
            'x': [1.0, 2.0, 3.0, 4.0],
            'y': [1.1, 3.2, 5.3, 7.4]  # Matches y1,y2,y3,y4 respectively
        })
        test_data.to_sql('test_data', self.db_manager.engine, if_exists='replace', index=False)

        selector = FunctionSelector(self.db_manager)
        selector.calculate_least_squares()
        mapper = TestMapper(self.db_manager, selector)
        mapper.map_test_data()

        results_df = pd.read_sql_table('test_results', self.db_manager.engine)
        self.assertFalse(results_df.empty)
        self.assertIn('ideal_function', results_df.columns)
        self.assertIn('delta_y', results_df.columns)

        expected = [1, 2, 3, 4]
        actual = results_df['ideal_function'].tolist()
        self.assertListEqual(actual, expected)

        # Check delta_y is zero for exact matches
        for _, row in results_df.iterrows():
            self.assertEqual(row['delta_y'], 0.0)

    def test_empty_training_data(self):
        """
        Test handling of empty training data.
        """
        empty_training = pd.DataFrame(columns=['x', 'y1', 'y2', 'y3', 'y4'])
        empty_training.to_sql('training_data', self.db_manager.engine, if_exists='replace', index=False)

        ideal_functions = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1.1, 2.1, 3.1, 4.1],
            'y2': [2.2, 3.2, 4.2, 5.2],
            'y3': [3.3, 4.3, 5.3, 6.3],
            'y4': [4.4, 5.4, 6.4, 7.4],
            'y5': [5, 6, 7, 8],
        })
        for i in range(6, 51):
            ideal_functions[f'y{i}'] = ideal_functions['y5'] + i + 0.1
        ideal_functions.to_sql('ideal_functions', self.db_manager.engine, if_exists='replace', index=False)

        selector = FunctionSelector(self.db_manager)
        selector.calculate_least_squares()
        selected = selector.get_selected_functions()
        self.assertEqual(len(selected), 0)

    def test_missing_columns(self):
        """
        Test handling of missing columns in training data.
        """
        incomplete_training = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1, 2, 3, 4],
            # Missing y2, y3, y4
        })
        incomplete_training.to_sql('training_data', self.db_manager.engine, if_exists='replace', index=False)

        ideal_functions = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y1': [1.1, 2.1, 3.1, 4.1],
            'y2': [2.2, 3.2, 4.2, 5.2],
            'y3': [3.3, 4.3, 5.3, 6.3],
            'y4': [4.4, 5.4, 6.4, 7.4],
            'y5': [5, 6, 7, 8],
        })
        for i in range(6, 51):
            ideal_functions[f'y{i}'] = ideal_functions['y5'] + i + 0.1
        ideal_functions.to_sql('ideal_functions', self.db_manager.engine, if_exists='replace', index=False)

        selector = FunctionSelector(self.db_manager)
        selector.calculate_least_squares()
        selected = selector.get_selected_functions()
        self.assertEqual(len(selected), 0)


if __name__ == '__main__':
    unittest.main()
