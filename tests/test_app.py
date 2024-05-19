import sys
import os
import unittest
import pandas as pd
from dash.exceptions import PreventUpdate

# Adjust the sys.path to ensure the Scripts module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import functions to be tested
from app import search_term, update_dropdown_options

# Sample data for testing
df_actors_sample = pd.DataFrame({
    'primaryName': ['Robert Downey Jr.', 'Scarlett Johansson', 'Chris Hemsworth']
})

# Define the test case class
class TestAppFunctions(unittest.TestCase):

    def test_search_term_found(self):
        result = search_term('Robert Downey Jr.', df_actors_sample, 'primaryName')
        self.assertEqual(result, ['Robert Downey Jr.'], "Should find 'Robert Downey Jr.'")

    def test_search_term_not_found(self):
        result = search_term('Tom Hanks', df_actors_sample, 'primaryName')
        self.assertEqual(result, [], "Return should be empty")

    def test_update_dropdown_options_empty_search_value(self):
        with self.assertRaises(PreventUpdate):
            update_dropdown_options('', [], df_actors_sample, 'primaryName')

    def test_update_dropdown_options_no_search_value(self):
        with self.assertRaises(PreventUpdate):
            update_dropdown_options(None, [], df_actors_sample, 'primaryName')

    def test_update_dropdown_options_with_search_value(self):
        result = update_dropdown_options('Robert Downey Jr.', [], df_actors_sample, 'primaryName')
        expected = [{'label': 'Robert Downey Jr.', 'value': 'Robert Downey Jr.'}]
        self.assertEqual(result, expected, "Should return dropdown option for 'Robert Downey Jr.'")
    
    def test_update_dropdown_options_with_state(self):
        result = update_dropdown_options('Robert Downey Jr.', ['Scarlett Johansson'], df_actors_sample, 'primaryName')
        expected = [{'label': 'Robert Downey Jr.', 'value': 'Robert Downey Jr.'}, {'label' : 'Scarlett Johansson', 'value': 'Scarlett Johansson'}]
        self.assertEqual(result, expected, "Should return dropdown options with Robert Downey Jr. and Scarlett Johansson")

if __name__ == "__main__":
    unittest.main()

