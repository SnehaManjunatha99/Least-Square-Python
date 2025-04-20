# src/visualizer.py

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot
import pandas as pd
from database import DatabaseManager

class Visualizer:
    """
    Visualizes the training data, ideal functions, and test results using Bokeh.
    """

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the Visualizer with a DatabaseManager.
        
        :param db_manager: An instance of DatabaseManager.
        """
        self.db_manager = db_manager

    def plot_training_data(self):
        """
        Create a Bokeh figure for the training data (y1, y2, y3, y4).
        
        :return: A Bokeh figure object.
        """
        training_df = pd.read_sql_table('training_data', self.db_manager.engine)
        p = figure(title="Training Data", x_axis_label='X', y_axis_label='Y')
        for i in range(1, 5):
            p.line(training_df['x'], training_df[f'y{i}'], line_width=2, legend_label=f'Training y{i}')
        p.legend.location = "top_left"
        return p

    def plot_ideal_functions(self, selected_functions: list):
        """
        Create a Bokeh figure for the selected ideal functions.
        
        :param selected_functions: List of integers representing selected ideal functions.
        :return: A Bokeh figure object.
        """
        ideal_df = pd.read_sql_table('ideal_functions', self.db_manager.engine)
        p = figure(title="Selected Ideal Functions", x_axis_label='X', y_axis_label='Y')
        for func_no in selected_functions:
            p.line(ideal_df['x'], ideal_df[f'y{func_no}'], line_width=2, legend_label=f'Ideal y{func_no}')
        p.legend.location = "top_left"
        return p

    def plot_test_data(self):
        """
        Create a Bokeh figure for the test data points and their deviations.
        
        :return: A Bokeh figure object.
        """
        results_df = pd.read_sql_table('test_results', self.db_manager.engine)
        p = figure(title="Test Data with Deviations", x_axis_label='X', y_axis_label='Y')
        p.scatter(results_df['x'], results_df['y'], size=8, color='navy', alpha=0.5, legend_label='Test Data')

        # Add lines to represent delta_y visually
        for _, row in results_df.iterrows():
            p.line([row['x'], row['x']], [row['y'], row['y'] - row['delta_y']], 
                   line_dash='dashed', color='red')
        p.legend.location = "top_left"
        return p

    def show_plots(self, training_plot, ideal_plot, test_plot):
        """
        Arrange and display the three plot figures in a grid layout.
        
        :param training_plot: Bokeh figure for training data.
        :param ideal_plot: Bokeh figure for ideal functions.
        :param test_plot: Bokeh figure for test data.
        """
        grid = gridplot([[training_plot], [ideal_plot], [test_plot]], sizing_mode='stretch_both')
        output_file("data_visualization.html")
        show(grid)
