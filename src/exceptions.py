# src/exceptions.py

class DataLoadingError(Exception):
    """Raised when an error occurs during data loading into the database."""
    pass


class FunctionSelectionError(Exception):
    """Raised when an error occurs during the function selection (least-squares) process."""
    pass


class TestMappingError(Exception):
    """Raised when an error occurs during the test data mapping process."""
    pass
