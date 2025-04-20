
## Introduction

Data analysis and visualization are essential for deriving meaningful insights from complex datasets. This project focuses on selecting optimal functions that best fit training data, mapping test data to these selected functions based on minimal deviations, and visualizing the results for comprehensive understanding. Leveraging Python's robust libraries such as Pandas, SQLAlchemy, NumPy, and Bokeh, the project ensures efficient data handling, precise computation, and interactive visual representation.

## Objectives

- **Data Management**: Efficiently load and store training, ideal, and test datasets using a relational database.
- **Function Selection**: Implement a least squares approach to identify ideal functions that best fit the training data.
- **Data Mapping**: Map test data points to the selected ideal functions based on deviation criteria.
- **Visualization**: Generate interactive plots to visualize training data, selected ideal functions, and test data mappings.
- **Testing**: Develop comprehensive unit tests to ensure the reliability and accuracy of each module.

## Technologies Used

- **Programming Language**: Python 3.8+
- **Libraries**:
  - [Pandas](https://pandas.pydata.org/) for data manipulation
  - [NumPy](https://numpy.org/) for numerical computations
  - [SQLAlchemy](https://www.sqlalchemy.org/) for ORM and database interactions
  - [Bokeh](https://bokeh.org/) for interactive visualizations
  - [unittest](https://docs.python.org/3/library/unittest.html) for unit testing
- **Database**: SQLite

## Project Structure

```plaintext
UC-9850/
├── data/
│   ├── train.csv
│   ├── ideal.csv
│   └── test.csv
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── data_loader.py
│   ├── function_selector.py
│   ├── test_mapper.py
│   ├── visualizer.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_suite.py
├── reports/
│   ├── report.pdf
│   └── images/
│       ├── training_data.png
│       ├── ideal_functions.png
│       └── test_data_mapping.png
├── app.log
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher: Ensure Python is installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/UC-9850.git
   cd UC-9850
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - Windows: `venv\Scriptsctivate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- **Running the Application**:
  Execute the `main.py` script to perform function selection, test data mapping, and generate visualizations:
  ```bash
  python src/main.py
  ```

- **Running Unit Tests**:
  To ensure the system's reliability and accuracy, run the unit tests located in the `tests/` directory:
  ```bash
  python tests/test_suite.py
  ```

## Features

- **Data Loading and Management**: Efficient ingestion and storage of CSV datasets into a SQLite database using SQLAlchemy.
- **Function Selection**: Implements the least squares method to identify ideal functions that best fit the training data.
- **Test Data Mapping**: Maps test data points to the selected ideal functions based on calculated deviations.
- **Interactive Visualization**: Generates comprehensive plots using Bokeh to visualize data relationships and mappings.
- **Robust Testing Framework**: Comprehensive unit tests covering standard operations and edge cases to ensure system reliability.

## Visualization Outputs

Interactive visualizations are generated using Bokeh and saved as `data_visualization.html`. The visualizations include:
- **Training Data Plot**: Displays the original training functions y1 to y4.
- **Ideal Functions Plot**: Illustrates the selected ideal functions y42, y41, y11, and y48 that best fit the training data.
- **Test Data Mapping Plot**: Shows the test data points mapped to the ideal functions, with deviation lines indicating the differences.

## Contributing

Contributions are welcome! To contribute:
1. Fork the Repository
2. Create a New Branch: `git checkout -b feature/YourFeature`
3. Commit Your Changes: `git commit -m "Add Your Feature"`
4. Push to the Branch: `git push origin feature/YourFeature`
5. Open a Pull Request

