from src.page_view_api.constants import (
     ALL_PROJECTS,
     ALL_PROJECTS_NO_AGENTS,
     DAILY,
     ENGLISH_PROJECTS,
     ENGLISH_PROJECTS_NO_AGENTS,
     MONTHS_31_DAYS,
     QUERY_PARAM_MONTH_TIME_WINDOW,
     STATUS_OK,
     STATUS_BAD_REQ, 
     USER_AGENT,
     USER_AGENT_HEADER, 
     WIKIMEDIA_PAGEVIEWS_PER_ARTICLE_URL, 
     WIKIMEDIA_TOP_PAGEVIEWS_URL
)

from datetime import date, timedelta

import requests

class WikiGateway:
    cache = {}

    def map_function(self, res_json, total_counts):
        for attribute in res_json:
            if attribute == 'items': # In case there are other attributes in the response dict (there shouldnt be)
                # items is a list with 1 dict element
                # we want the element articles from that dict
                articles = res_json[attribute][0]['articles']
                for elem in articles:
                    article_name = elem['article']
                    view_count = int(elem['views'])
                    if article_name not in total_counts:
                        total_counts[article_name] = 0
                    total_counts[article_name] += view_count

    def call_wiki_api_for_top_articles_for_time_period(self, month:str, year: str, day: int, end_day: int, url:str, total_counts):
        headers = self.construct_headers()
        curr_date = date(year=int(year), month=int(month), day=day)
        i = 1
        while i <= end_day:
            month_string = str(curr_date.month) if curr_date.month >= 10 else f'0' + str(curr_date.month)
            day_string = str(curr_date.day) if curr_date.day >= 10 else f'0' + str(curr_date.day)
            curr_url = url + str(curr_date.year) + '/' + month_string + '/' + day_string
            res = requests.get(url=curr_url,headers=headers)
            res_json = res.json()
            if res.status_code != STATUS_OK:
                return res.json(), STATUS_BAD_REQ
            else:
                self.map_function(res_json, total_counts)

            curr_date = curr_date + timedelta(days=1)
            i += 1
        return None, STATUS_OK

    def get_most_viewed_articles_for_time_window(
            self,
            month: str,
            year: str,
            time_window_size: str,
            start_day: str,
            projects: str = None,
            page_num: int = 0,
            page_size: int = 10,
        ):
        
        url = WIKIMEDIA_TOP_PAGEVIEWS_URL
        if projects == 'english':
            url += ENGLISH_PROJECTS_NO_AGENTS
        else:
            url += ALL_PROJECTS_NO_AGENTS

        total_counts = {}
        total_counts_list = []
        issues = []
        cache_key = (month, year, time_window_size, projects, start_day)

        if cache_key in self.cache:
            total_counts_list, issues = self.cache[cache_key]
        else:
            end_day = 0
            start_day = 1
            if time_window_size == QUERY_PARAM_MONTH_TIME_WINDOW:
                end_day = 31 if int(month) in MONTHS_31_DAYS else 30
                if int(month) == 2:
                    if int(year) % 4 == 0:
                        end_day = 29
                    else:
                        end_day = 28
            else:
                end_day = 7
                start_day = start_day

            wiki_response, status = self.call_wiki_api_for_top_articles_for_time_period(
                month=month,
                year=year,
                day=start_day,
                end_day=end_day,
                url=url,
                total_counts=total_counts
            )
            if wiki_response != None:
                return wiki_response, status
            
            total_counts_list = sorted(total_counts.items(), key=lambda x:x[1], reverse=True)
            self.cache[cache_key] = (total_counts_list, issues)

        first_item_on_page = 0 + page_num * page_size
        last_item_on_page = first_item_on_page + page_size

        if first_item_on_page > len(total_counts_list):
            failed_response = {
                'issues' : ['There are no more items on this call'] 
            }
            return failed_response, STATUS_BAD_REQ
        if last_item_on_page > len(total_counts_list):
            last_item_on_page = len(total_counts_list)

        rank = first_item_on_page + 1

        ranked_list = []
        for i in range(first_item_on_page, last_item_on_page):
            curr_dict = {}
            curr_dict['article_name'] = total_counts_list[i][0]
            curr_dict['views'] = total_counts_list[i][1]
            curr_dict['rank'] = rank
            ranked_list.append(curr_dict)
            rank += 1

        ranked_response = {
            'year' : year,
            'month': month,
            'time_window_size': time_window_size,
            'start_day': None if time_window_size == QUERY_PARAM_MONTH_TIME_WINDOW else start_day,
            'issues': issues,
            'page_num' : page_num,
            'page_size' : page_size,
            'rankings': ranked_list
        }

        return ranked_response, STATUS_OK

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

        url +=  name + '/' + DAILY
        start_date_str = ''
        start_date = date(year=int(year), month=int(month), day=1)
        start_month_string = f'{start_date.month}' if int(start_date.month) >= 10 else f'0{start_date.month}'
        if time_window_size == QUERY_PARAM_MONTH_TIME_WINDOW:
            # Create the start date string for the response
            start_date_str = str(start_date.year) + start_month_string + '01'
            url = self.add_month_string(month, year, url)
        else:
            url, start_day_str = self.add_week_string(month=month, year=year, start_day=start_day, url=url)
            start_date_str = str(start_date.year) + start_month_string + start_day_str
        
        total_count_response = {}
        cache_key = (name, month, year, time_window_size, start_day, projects)
        if cache_key in self.cache:
            total_count_response = self.cache[cache_key]
        else:
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
            self.cache[cache_key] = total_count_response

        return total_count_response, 200


    def day_of_most_views_for_article_in_given_month(self, name: str, month: str, year: str, projects:str = None):
        headers = self.construct_headers()
        url = WIKIMEDIA_PAGEVIEWS_PER_ARTICLE_URL
        if projects == 'english':
            url += ENGLISH_PROJECTS
        else:
            url += ALL_PROJECTS
        
        url +=  name + '/' + DAILY
        url = self.add_month_string(month, year, url) 

        cache_key = (name, month, year, projects)
        most_viewed_day = {}
        if cache_key in self.cache:
            most_viewed_day = self.cache[cache_key] 
        else:   
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
            self.cache[cache_key] = most_viewed_day
        
        return most_viewed_day, STATUS_OK
    

    def construct_headers(self):
        headers = {}
        headers[USER_AGENT_HEADER] = USER_AGENT
        return headers
    
    def add_week_string(self, month: str, year: str, start_day: str, url: str):
        converted_month = int(month)
        
        start_date = date(year=int(year), month=converted_month, day=int(start_day))
        end_date = start_date + timedelta(days=7)

        start_date_str = str(start_date.year)
        start_month_string = f'{converted_month}' if converted_month >= 10 else f'0{converted_month}'
        start_day_string = f'{start_date.day}' if int(start_date.day) >= 10 else f'0{start_date.day}'
        start_date_str += start_month_string + start_day_string
        
        end_date_str = str(end_date.year)
        end_month_string = f'{end_date.month}' if end_date.month >= 10 else f'0{end_date.month}'
        end_day_string = f'{end_date.day}' if int(end_date.day) >= 10 else f'0{end_date.day}'
        end_date_str += end_month_string + end_day_string

        url += start_date_str + '/' + end_date_str
        
        return url, start_day_string

    def add_month_string(self, month: str, year: str, url: str):
        converted_month = int(month)
        month_string = f'{converted_month}' if converted_month >= 10 else f'0{converted_month}'
        if converted_month in MONTHS_31_DAYS:
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
    