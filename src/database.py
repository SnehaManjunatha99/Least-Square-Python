# src/database.py

from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class TrainingData(Base):
    """
    ORM class representing the 'training_data' table structure.
    Columns:
        x, y1, y2, y3, y4
    """
    __tablename__ = 'training_data'
    x = Column(Float, primary_key=True)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)


class IdealFunctions(Base):
    """
    ORM class representing the 'ideal_functions' table structure.
    Contains x and y1 to y50 columns.
    """
    __tablename__ = 'ideal_functions'
    x = Column(Float, primary_key=True)
    # Dynamically add columns y1 to y50
    for i in range(1, 51):
        vars()[f'y{i}'] = Column(Float)


class TestData(Base):
    """
    ORM class representing the 'test_data' table structure.
    Columns:
        id, x, y
    """
    __tablename__ = 'test_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float)
    y = Column(Float)


class TestResults(Base):
    """
    ORM class representing the 'test_results' table structure.
    Columns:
        id, x, y, delta_y, ideal_function
    """
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float)
    y = Column(Float)
    delta_y = Column(Float)
    ideal_function = Column(Integer)


class DatabaseManager:
    """
    Manages database connections, sessions, and schema creation/drop.
    """

    def __init__(self, db_name: str = 'datasets.db'):
        """
        Initialize the database manager with the given SQLite database name.
        
        :param db_name: Name of the SQLite database file.
        """
        self.engine = create_engine(f'sqlite:///{db_name}')
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = Base.metadata

    def create_tables(self) -> None:
        """
        Create all tables defined by the Base metadata.
        """
        try:
            self.metadata.create_all(self.engine)
            print("Tables created successfully.")
        except SQLAlchemyError as e:
            print(f"Error creating tables: {e}")

    def drop_tables(self) -> None:
        """
        Drop all tables from the database.
        """
        try:
            self.metadata.drop_all(self.engine)
            print("Tables dropped successfully.")
        except SQLAlchemyError as e:
            print(f"Error dropping tables: {e}")

    def get_session(self):
        """
        Get a new SQLAlchemy session object.
        
        :return: A session object.
        """
        return self.Session()
