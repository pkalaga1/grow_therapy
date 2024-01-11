import unittest
from unittest.mock import MagicMock, patch
from src.page_view_api.constants import *
from src.page_view_api.wiki_gateway import WikiGateway


class TestWikiGateway(unittest.TestCase):

    def setUp(self):
        self.gateway = WikiGateway()

    def test_map_function(self):
        res_json = {'items': [{'articles': [{'article': 'Article1', 'views': '10'}]}]}
        total_counts = {}

        self.gateway.map_function(res_json, total_counts)
        self.assertEqual(total_counts, {'Article1': 10})

    @patch('requests.get')
    def test_call_wiki_api_for_top_articles_for_time_period(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = STATUS_OK
        mock_response.json.return_value = {'items': [{'articles': [{'article': 'Article1', 'views': '10'}]}]}
        mock_requests_get.return_value = mock_response

        result, status = self.gateway.call_wiki_api_for_top_articles_for_time_period(
            month='01', year='2022', day=1, end_day=2, url=WIKIMEDIA_TOP_PAGEVIEWS_URL, total_counts={}
        )

        self.assertEqual(result, None)
        self.assertEqual(status, STATUS_OK)

    def test_get_most_viewed_articles_for_time_window(self):
        self.gateway.cache = {}

        result, status = self.gateway.get_most_viewed_articles_for_time_window(
            month='01', year='2022', time_window_size='daily', start_day='01', projects=None
        )

        self.assertEqual(status, STATUS_BAD_REQ)

    @patch('requests.get')
    def test_get_view_count_for_article_for_time_window(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = STATUS_OK
        mock_response.json.return_value = {'items': [{'views': 10}]}
        mock_requests_get.return_value = mock_response

        result, status = self.gateway.get_view_count_for_article_for_time_window(
            name='Article1', month='01', year='2022', time_window_size='month', projects=None
        )

        self.assertEqual(status, STATUS_OK)
        self.assertEqual(result['views'], 10)

        result, status = self.gateway.get_view_count_for_article_for_time_window(
            name='Article1', month='01', year='2022', time_window_size='week', start_day='01', projects=None
        )

        self.assertEqual(status, STATUS_OK)
        self.assertEqual(result['views'], 10)

    @patch('requests.get')
    def test_day_of_most_views_for_article_in_given_month(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = STATUS_OK
        mock_response.json.return_value = {'items': [{'views': 10, 'timestamp': '2022-01-01'}]}
        mock_requests_get.return_value = mock_response

        result, status = self.gateway.day_of_most_views_for_article_in_given_month(
            name='Article1', month='01', year='2022', projects=None
        )

        self.assertEqual(status, STATUS_OK)
        self.assertEqual(result['views'], 10)

    def test_construct_headers(self):
        headers = self.gateway.construct_headers()
        self.assertEqual(headers[USER_AGENT_HEADER], USER_AGENT)

    def test_add_month_string(self):
        self.gateway.add_week_string = MagicMock(return_value=('', ''))
        
        url = self.gateway.add_month_string(month='01', year='2022', url='mock_url')
        expected_url = 'mock_url20220101/20220131'
        self.assertEqual(url, expected_url)

        url = self.gateway.add_month_string(month='02', year='2022', url='mock_url')
        expected_url = 'mock_url20220201/20220228'
        self.assertEqual(url, expected_url)

        url = self.gateway.add_month_string(month='02', year='2024', url='mock_url')
        expected_url = 'mock_url20240201/20240229'
        self.assertEqual(url, expected_url)

        url = self.gateway.add_month_string(month='04', year='2022', url='mock_url')
        expected_url = 'mock_url20220401/20220430'
        self.assertEqual(url, expected_url)

    def test_add_week_string(self):
        url, start_day_string = self.gateway.add_week_string(month='01', year='2022', start_day='01', url='mock_url')
        expected_url = 'mock_url20220101/20220108'
        self.assertEqual(expected_url, url)

        url, start_day_string = self.gateway.add_week_string(month='01', year='2022', start_day='27', url='mock_url')
        expected_url = 'mock_url20220127/20220203'
        self.assertEqual(expected_url, url)

        url, start_day_string = self.gateway.add_week_string(month='12', year='2021', start_day='27', url='mock_url')
        expected_url = 'mock_url20211227/20220103'
        self.assertEqual(expected_url, url)
