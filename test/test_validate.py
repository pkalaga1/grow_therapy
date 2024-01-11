import unittest
from src.page_view_api.constants import *
from src.page_view_api.validate import validate_params, validate_page_values

class TestValidateParamsAndPageValues(unittest.TestCase):

    def test_validate_params_valid_input(self):
        all_params = {
            QUERY_PARAM_MONTH: '12',
            QUERY_PARAM_YEAR:  '2022',
            QUERY_PARAM_PROJECT: 'english',
            QUERY_PARAM_NAME: 'Article1',
            QUERY_PARAM_START_DAY: '15',
            QUERY_PARAM_TIME_WINDOW_SIZE: QUERY_PARAM_MONTH_TIME_WINDOW,
        }

        issues = validate_params(all_params)
        self.assertEqual(issues, [])

    def test_validate_params_invalid_month(self):
        all_params = {
            QUERY_PARAM_MONTH: '13',
            QUERY_PARAM_YEAR:  '2022',
            QUERY_PARAM_PROJECT: 'english',
            QUERY_PARAM_NAME: 'Article1',
            QUERY_PARAM_START_DAY: '15',
            QUERY_PARAM_TIME_WINDOW_SIZE: QUERY_PARAM_MONTH_TIME_WINDOW,
        }

        issues = validate_params(all_params)
        self.assertIn('month must be between 1 and 12 inclusive', issues)

    def test_validate_params_invalid_year(self):
        all_params = {
            QUERY_PARAM_MONTH: '12',
            QUERY_PARAM_YEAR:  '22',  # Invalid year length
            QUERY_PARAM_PROJECT: 'english',
            QUERY_PARAM_NAME: 'Article1',
            QUERY_PARAM_START_DAY: '15',
            QUERY_PARAM_TIME_WINDOW_SIZE: QUERY_PARAM_MONTH_TIME_WINDOW,
        }

        issues = validate_params(all_params)
        self.assertIn('year must have a length of 4', issues)

    def test_validate_params_invalid_time_window(self):
        all_params = {
            QUERY_PARAM_MONTH: '12',
            QUERY_PARAM_YEAR:  '2022',
            QUERY_PARAM_PROJECT: 'english',
            QUERY_PARAM_NAME: 'Article1',
            QUERY_PARAM_START_DAY: '15',
            QUERY_PARAM_TIME_WINDOW_SIZE: 'invalid_time_window',
        }

        issues = validate_params(all_params, day_required=True)
        self.assertIn('time window must be either a week or a month', issues)

    def test_validate_page_values_valid_input(self):
        all_params = {
            QUERY_PARAM_PAGE_NUM: '1',
            QUERY_PARAM_PAGE_SIZE: '10',
        }

        issues = validate_page_values(all_params)
        self.assertEqual(issues, [])

    def test_validate_page_values_invalid_page_num(self):
        all_params = {
            QUERY_PARAM_PAGE_NUM: 'invalid_page_num',
            QUERY_PARAM_PAGE_SIZE: '10',
        }

        issues = validate_page_values(all_params)
        self.assertIn('page num must be an integer', issues)

    def test_validate_page_values_invalid_page_size(self):
        all_params = {
            QUERY_PARAM_PAGE_NUM: '1',
            QUERY_PARAM_PAGE_SIZE: 'invalid_page_size',
        }

        issues = validate_page_values(all_params)
        self.assertIn('page size must be an integer', issues)
