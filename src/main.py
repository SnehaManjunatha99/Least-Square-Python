# src/main.py

import os
import logging
from database import DatabaseManager
from data_loader import DataLoader
from function_selector import FunctionSelector
from test_mapper import TestMapper
from visualizer import Visualizer
from exceptions import DataLoadingError, FunctionSelectionError, TestMappingError

def main():
    """
    Main entry point of the application.
    1. Prepare file paths for training, ideal, and test data.
    2. Create and initialize the database.
    3. Load data into database tables.
    4. Perform ideal function selection via least-squares.
    5. Map test data to selected ideal functions.
    6. Visualize all results using Bokeh.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')

    training_file = os.path.join(data_dir, 'train.csv')
    ideal_file = os.path.join(data_dir, 'ideal.csv')
    test_file = os.path.join(data_dir, 'test.csv')

    # Validate file existence
    for file_path in [training_file, ideal_file, test_file]:
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return

    # Initialize database
    db_manager = DatabaseManager('datasets.db')
    db_manager.create_tables()

    # Load data
    loader = DataLoader(db_manager)
    try:
        loader.load_all_data(training_file, ideal_file, test_file)
    except DataLoadingError as e:
        logging.error(e)
        return

    # Select best fit functions
    selector = FunctionSelector(db_manager)
    try:
        selector.calculate_least_squares()
    except FunctionSelectionError as e:
        logging.error(e)
        return

    selected_funcs = selector.get_selected_functions()
    if not selected_funcs:
        logging.warning("No ideal functions selected. Visualization and test mapping may not proceed.")
        return

    # Map test data
    mapper = TestMapper(db_manager, selector)
    try:
        mapper.map_test_data()
    except TestMappingError as e:
        logging.error(e)
        return

    # Visualization
    visualizer = Visualizer(db_manager)
    training_plot = visualizer.plot_training_data()
    ideal_plot = visualizer.plot_ideal_functions(selected_funcs)
    test_plot = visualizer.plot_test_data()
    visualizer.show_plots(training_plot, ideal_plot, test_plot)

    logging.info("Process completed successfully.")

if __name__ == "__main__":
    main()
