from constants import (
     ALL_PROJECTS,
     ENGLISH_PROJECTS,
     MONTHS_31_DAYS,
     STATUS_OK, 
     USER_AGENT,
     USER_AGENT_HEADER, 
     WIKIMEDIA_PAGEVIEWS_PER_ARTICLE_URL, 
     WIKIMEDIA_TOP_PAGEVIEWS_URL
)

from datetime import date

from json import dumps

import requests

class WikiGateway:

    def day_of_most_views_for_article_in_given_month(self, name: str, month: str, year: str, projects:str = None):
        headers = self.construct_headers()
        url = WIKIMEDIA_PAGEVIEWS_PER_ARTICLE_URL
        if projects == 'english':
            url += ENGLISH_PROJECTS
        else:
            url += ALL_PROJECTS
        
        url +=  name + '/daily/'
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
    