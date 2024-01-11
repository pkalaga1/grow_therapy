# import pytest
import requests


base_url = 'http://localhost:8080/'

def test_get_instructions():
     response = requests.get(base_url)
     expected_response = {'instructions': 'Please see our ReadME for help!'}
     assert response.status_code == 200
     assert response.json() == expected_response

# def test_bad_req_highest_viewed_day_for_article():
#      response = requests.get(base_url + API_ENDPOINT_HIGHEST_VIEWED_DAY_FOR_ARTICLE)
#      expected_response = {'instructions': 'Please see our ReadME for help!'}
#      assert response.status_code == STATUS_BAD_REQ
#      assert response.json() == expected_response
#      print(response.json())