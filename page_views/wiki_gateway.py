from constants import (
     ALL_PROJECTS,
     ENGLISH_PROJECTS,
     MONTHS_31_DAYS,
     QUERY_PARAM_MONTH_TIME_WINDOW,
     STATUS_OK, 
     USER_AGENT,
     USER_AGENT_HEADER, 
     WIKIMEDIA_PAGEVIEWS_PER_ARTICLE_URL, 
     WIKIMEDIA_TOP_PAGEVIEWS_URL
)

from datetime import date, datetime, timedelta

from json import dumps

import requests

class WikiGateway:

    def get_view_count_for_article_for_time_window(
            self, 
            name: str, 
            month: str,
            year: str,
            time_window_size: str, 
            start_day: str = None, 
            projects:str = None
        ):
        headers = self.construct_headers()
        url = WIKIMEDIA_PAGEVIEWS_PER_ARTICLE_URL
        if projects == 'english':
            url += ENGLISH_PROJECTS
        else:
            url += ALL_PROJECTS

        url +=  name + '/daily/'
        start_date_str = ''
        if time_window_size == QUERY_PARAM_MONTH_TIME_WINDOW:
            start_date = date(year=int(year), month=int(month), day=1)
            start_month_string = f'{start_date.month}' if int(start_date.month) >= 10 else f'0{start_date.month}'
            start_date_str = str(start_date.year) + start_month_string + '01'
            url = self.add_month_string(month, year, url)
        else:
            
            start_date = date(year=int(year), month=int(month), day=int(start_day))
            end_date = start_date + timedelta(days=7)

            start_date_str = str(start_date.year)
            start_month_string = f'{month}' if int(month) >= 10 else f'0{month}'
            start_day_string = f'{start_date.day}' if int(start_date.day) >= 10 else f'0{start_date.day}'
            start_date_str += start_month_string + start_day_string
            
            end_date_str = str(end_date.year)
            end_month_string = f'{month}' if int(month) >= 10 else f'0{month}'
            end_day_string = f'{end_date.day}' if int(end_date.day) >= 10 else f'0{end_date.day}'
            end_date_str += end_month_string + end_day_string

            url += start_date_str + '/' + end_date_str
        
        res = requests.get(url=url, headers=headers)
        res_json = res.json()
        if res.status_code != STATUS_OK:
            return res_json, res.status_code
    
        total_count = 0
        for attribute in res_json:
            if attribute == 'items': # In case there are other attributes in the response dict (there shouldnt be)
                for day in res_json[attribute]:
                    total_count += day['views']

        total_count_response = {
            'name': name,
            'start_date': str(date.fromisoformat(start_date_str)),
            'time_window_size': time_window_size,
            'views': total_count,
            'url': url,
        }
        return total_count_response, 200


    def day_of_most_views_for_article_in_given_month(self, name: str, month: str, year: str, projects:str = None):
        headers = self.construct_headers()
        url = WIKIMEDIA_PAGEVIEWS_PER_ARTICLE_URL
        if projects == 'english':
            url += ENGLISH_PROJECTS
        else:
            url += ALL_PROJECTS
        
        url +=  name + '/daily/'
        url = self.add_month_string(month, year, url)       

        res = requests.get(url=url, headers=headers)

        res_json = res.json()
        if res.status_code != STATUS_OK:
            return res_json, res.status_code

        max_count = -1
        max_timestamp = ''

        for attribute in res_json:
            if attribute == 'items': # In case there are other attributes in the response dict (there shouldnt be)
                for day in res_json[attribute]:
                    if day['views'] > max_count:
                        max_count = day['views']
                        max_timestamp = str(day['timestamp'])

        most_viewed_day = {
            'name': name,
            'date': str(date.fromisoformat(max_timestamp)),
            'views': max_count,
            'url': url,
        }
        
        return most_viewed_day, STATUS_OK
    

    def construct_headers(self):
        headers = {}
        headers[USER_AGENT_HEADER] = USER_AGENT
        return headers
    
    def add_month_string(self, month: str, year: str, url: str):
        converted_month = int(month)
        month_string = f'{month}' if converted_month >= 10 else f'0{month}'
        if month in MONTHS_31_DAYS:
            start = f'{year}{month_string}01'
            end = f'{year}{month_string}31'
            url += start + '/' + end
        elif converted_month == 2:
            max_day_in_feb = 28
            if int(year) % 4 == 0: # To handle leap year
                max_day_in_feb = 29
            start = f'{year}{month_string}01'
            end = f'{year}{month_string}{max_day_in_feb}'
            url += start + '/' + end
        else:
            start = f'{year}{month_string}01'
            end = f'{year}{month_string}30'
            url += start + '/' + end
        
        return url
    