import pytest
import requests


base_url = 'http://localhost:8080/'

def test_get_instructions():
     response = requests.get(base_url)
     expected_response = {'instructions': 'Please see our ReadME for help!'}
     assert response.status_code == 200
     assert response.json() == expected_response

def test_bad_req_no_params():
     response = requests.get(base_url + '/day_article_most_viewed_in_month')
     expected_response = '{"issues": ["month can not be none", "year can not be None", "name can not be None"]}'
     assert response.status_code == 400
     assert response.json() == expected_response

def test_bad_req_incorrect_params():
     query_param_string = '?month=90&name=test&year=abcd'
     response = requests.get(base_url + '/day_article_most_viewed_in_month' + query_param_string)
     expected_response = '{"issues": ["month must be between 1 and 12 inclusive", "year must be an integer"]}'
     assert response.status_code == 400
     assert response.json() == expected_response

def test_bad_req_incorrect_project_params():
     query_param_string = '?month=10&name=test&year=2021&project=spanish'
     response = requests.get(base_url + '/day_article_most_viewed_in_month' + query_param_string)
     expected_response = '{"issues": ["This api only supports all or english. Please use one of those"]}'
     assert response.status_code == 400
     assert response.json() == expected_response

def test_bad_req_page_params_incorrect_top_articles():
     query_param_string = '?month=11&name=test&year=2021&time_window_size=month&page_num=abcd&page_size=abcd'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     expected_response = '{"issues": ["page num must be an integer", "page size must be an integer"]}'
     assert response.status_code == 400
     assert response.json() == expected_response

def test_bad_req_window_size_params_incorrect_top_articles():
     query_param_string = '?month=11&name=test&year=2021&time_window_size=biannual'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     expected_response = '{"issues": ["time window must be either a week or a month"]}'
     assert response.status_code == 400
     assert response.json() == expected_response

def test_bad_req_window_size_params_for_week_missing_day_top_articles():
     query_param_string = '?month=11&name=test&year=2021&time_window_size=week'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     expected_response = '{"issues": ["day can not be None for a week-based time window"]}'
     assert response.status_code == 400
     assert response.json() == expected_response

def test_bad_req_window_size_params_for_week_invalid_day_top_articles():
     query_param_string = '?month=11&name=test&year=2021&time_window_size=week&start_day=abcd'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     expected_response = '{"issues": ["day must be an integer"]}'
     assert response.status_code == 400
     assert response.json() == expected_response

def test_not_found_most_viewed_day():
     query_param_string = '?month=10&name=test&year=2019'
     response = requests.get(base_url + '/day_article_most_viewed_in_month' + query_param_string)
     assert response.status_code == 404

def test_most_viewed_day_success():
     query_param_string = '?month=10&name=Albert_Einstein&year=2019&project=english'
     response = requests.get(base_url + '/day_article_most_viewed_in_month' + query_param_string)
     assert response.status_code == 200
     expected_response = {
          'date': '2019-10-08',
           'name': 'Albert_Einstein',
           'url': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/20191001/20191031',
           'views': 22903
     }
     assert expected_response == response.json()

def test_total_views_for_article_over_month_success():
     query_param_string = '?month=10&name=Albert_Einstein&year=2019&project=english&time_window_size=month'
     response = requests.get(base_url + '/view_count_for_article_for_time_window' + query_param_string)
     assert response.status_code == 200
     expected_response = {
          'start_date': '2019-10-01',
          'time_window_size': 'month',
          'name': 'Albert_Einstein',
          'url': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/20191001/20191031',
          'views': 551426
     }
     assert expected_response == response.json()

def test_total_views_for_article_over_week_success():
     query_param_string = '?month=10&name=Albert_Einstein&year=2019&project=english&time_window_size=week&start_day=27'
     response = requests.get(base_url + '/view_count_for_article_for_time_window' + query_param_string)
     assert response.status_code == 200
     expected_response = {
          'start_date': '2019-10-27',
          'time_window_size': 'week',
          'name': 'Albert_Einstein',
          'url': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/20191027/20191103',
          'views': 128736
     }
     assert expected_response == response.json()

def test_ranked_articles_over_week_success():
     query_param_string = '?month=12&name=test&year=2017&time_window_size=week&start_day=27&project=english'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     
     assert response.status_code == 200
     res_json = response.json()
     assert res_json['month'] == '12'
     assert res_json['year'] == '2017'
     assert res_json['start_day'] == '27'
     assert res_json['page_num'] == 0
     assert res_json['page_size'] == 10
     assert len(res_json['issues']) == 0
     assert len(res_json['rankings']) == 10
     assert res_json['rankings'][0]['rank'] == 1

def test_ranked_articles_over_week_success_third_page():
     query_param_string = '?month=12&name=test&year=2017&time_window_size=week&start_day=27&project=english&page_num=3'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     
     assert response.status_code == 200
     res_json = response.json()
     assert res_json['month'] == '12'
     assert res_json['year'] == '2017'
     assert res_json['start_day'] == '27'
     assert res_json['page_num'] == 3
     assert res_json['page_size'] == 10
     assert len(res_json['issues']) == 0
     assert len(res_json['rankings']) == 10
     assert res_json['rankings'][0]['rank'] == 31

def test_ranked_articles_over_week_large_page_size_success():
     query_param_string = '?month=12&name=test&year=2017&time_window_size=week&start_day=27&project=english&page_size=300'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     
     assert response.status_code == 200
     res_json = response.json()
     rankings_length = len(res_json['rankings'])
     assert res_json['month'] == '12'
     assert res_json['year'] == '2017'
     assert res_json['start_day'] == '27'
     assert res_json['page_num'] == 0
     assert res_json['page_size'] == 300
     assert len(res_json['issues']) == 0
     assert  rankings_length == 300
     assert res_json['rankings'][0]['rank'] == 1
     assert res_json['rankings'][rankings_length - 1]['rank'] == 300

def test_ranked_articles_over_month_success():
     query_param_string = '?month=12&name=test&year=2017&time_window_size=month&project=english'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     
     assert response.status_code == 200
     res_json = response.json()
     assert res_json['month'] == '12'
     assert res_json['year'] == '2017'
     assert res_json['start_day'] == '01'
     assert res_json['page_num'] == 0
     assert res_json['page_size'] == 10
     assert len(res_json['issues']) == 0
     assert len(res_json['rankings']) == 10
     assert res_json['rankings'][0]['rank'] == 1

def test_ranked_articles_over_month_success_third_page():
     query_param_string = '?month=12&name=test&year=2017&time_window_size=month&project=english&page_num=3'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     
     assert response.status_code == 200
     res_json = response.json()
     assert res_json['month'] == '12'
     assert res_json['year'] == '2017'
     assert res_json['start_day'] == '01'
     assert res_json['page_num'] == 3
     assert res_json['page_size'] == 10
     assert len(res_json['issues']) == 0
     assert len(res_json['rankings']) == 10
     assert res_json['rankings'][0]['rank'] == 31

def test_ranked_articles_over_month_large_page_size_success():
     query_param_string = '?month=12&name=test&year=2017&time_window_size=month&project=english&page_size=300'
     response = requests.get(base_url + '/most_viewed_articles_for_time_window' + query_param_string)
     
     assert response.status_code == 200
     res_json = response.json()
     rankings_length = len(res_json['rankings'])
     assert res_json['month'] == '12'
     assert res_json['year'] == '2017'
     assert res_json['start_day'] == '01'
     assert res_json['page_num'] == 0
     assert res_json['page_size'] == 300
     assert len(res_json['issues']) == 0
     assert  rankings_length == 300
     assert res_json['rankings'][0]['rank'] == 1
     assert res_json['rankings'][rankings_length - 1]['rank'] == 300
