# src/data_loader.py

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from database import DatabaseManager
import logging

from exceptions import DataLoadingError

class DataLoader:
    """
    Responsible for loading CSV files into the database tables.
    Utilizes pandas for CSV reading and SQLAlchemy for database I/O.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the DataLoader with a given DatabaseManager.
        
        :param db_manager: An instance of DatabaseManager.
        """
        self.db_manager = db_manager

    def load_csv_to_table(self, csv_path: str, table_name: str) -> None:
        """
        Load a CSV file into a specified database table.
        
        :param csv_path: Path to the CSV file.
        :param table_name: Name of the database table to load the data into.
        :raises DataLoadingError: If file not found or SQL error occurs.
        """
        try:
            df = pd.read_csv(csv_path)
            df.columns = [col.lower() for col in df.columns]  # Normalize column names
            df.to_sql(table_name, self.db_manager.engine, if_exists='replace', index=False)
            logging.info(f"Data loaded into {table_name} from {csv_path}.")
        except FileNotFoundError:
            raise DataLoadingError(f"File {csv_path} not found.")
        except SQLAlchemyError as e:
            raise DataLoadingError(f"Error loading data into {table_name}: {e}")

    def load_all_data(self, training_file: str, ideal_file: str, test_file: str) -> None:
        """
        Load all three CSV files: training, ideal, and test data into their respective tables.
        
        :param training_file: Path to training data CSV.
        :param ideal_file: Path to ideal functions CSV.
        :param test_file: Path to test data CSV.
        """
        self.load_csv_to_table(training_file, 'training_data')
        self.load_csv_to_table(ideal_file, 'ideal_functions')
        self.load_csv_to_table(test_file, 'test_data')
