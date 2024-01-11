from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from src.page_view_api.wiki_gateway import WikiGateway
from src.page_view_api.validate import validate_params, validate_page_values
from src.page_view_api.constants import (
    API_ENDPOINT_HIGHEST_VIEWED_DAY_FOR_ARTICLE,
    API_ENDPOINT_TOP_VIEWED_ARTICLES_FOR_TIME_PERIOD,
    API_ENDPOINT_VIEW_COUNT_FOR_ARTICLE_FOR_TIME_WINDOW,
    STATUS_OK, 
    STATUS_BAD_REQ,
    PAGE_NUM_DEFAULT,
    PAGE_SIZE_DEFAULT,
    QUERY_PARAM_DELIMITER,
    QUERY_PARAM_MONTH,
    QUERY_PARAM_PROJECT,
    QUERY_PARAM_YEAR,
    QUERY_VALUE_DELIMITER,
    QUERY_PARAM_NAME,
    QUERY_PARAM_START_DAY,
    QUERY_PARAM_TIME_WINDOW_SIZE,
    QUERY_PARAM_PAGE_SIZE,
    QUERY_PARAM_PAGE_NUM,
)
hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self): 

        u = urlparse(self.path)
        query_params = parse_parameters(u.query)

        response_json = None
        status_code = STATUS_OK

        # Figure out path and direct it to the proper code
        print(self.path)            
        if u.path == API_ENDPOINT_HIGHEST_VIEWED_DAY_FOR_ARTICLE:
            response_json, status_code = self.do_get_day_of_most_view_for_article_in_given_month(query_params)
        elif u.path == API_ENDPOINT_VIEW_COUNT_FOR_ARTICLE_FOR_TIME_WINDOW:
            response_json, status_code = self.do_get_view_count_for_article_for_time_window(query_params)
        elif u.path == API_ENDPOINT_TOP_VIEWED_ARTICLES_FOR_TIME_PERIOD:
            response_json, status_code = self.do_get_most_viewed_articles_for_time_window(query_params)
        else:
            response_json, status_code = self.instructions()

        # Grab the response and write it to the website if you are using that instead of curl calls
        self.send_response(status_code)
        json_string = json.dumps(response_json, indent=2)
        self.path = '/example'
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))

    """
    Gets a ranked list of the most viewed articles for a week or a month
    Number of results can be modified by changing page num and page size
    Required: month, year
    Optional: time_window_size, start_day, page_size, page_num, project
    """
    def do_get_most_viewed_articles_for_time_window(self, query_params):
        issues = validate_params(query_params, day_required=True, name_required=False)
        issues.extend(validate_page_values(query_params))
        gateway = WikiGateway()

        if len(issues) > 0:
            issue_dict = {'issues': issues}
            response_json = json.dumps(issue_dict)
            status_code = STATUS_BAD_REQ
        else:
            page_num = PAGE_NUM_DEFAULT if not query_params[QUERY_PARAM_PAGE_NUM] else int(query_params[QUERY_PARAM_PAGE_NUM])
            page_size = PAGE_SIZE_DEFAULT if not query_params[QUERY_PARAM_PAGE_SIZE] else int(query_params[QUERY_PARAM_PAGE_SIZE])

            response_json, status_code = gateway.get_most_viewed_articles_for_time_window(
                month=query_params[QUERY_PARAM_MONTH],
                year=query_params[QUERY_PARAM_YEAR],
                start_day=query_params[QUERY_PARAM_START_DAY],
                time_window_size=query_params[QUERY_PARAM_TIME_WINDOW_SIZE],
                projects=query_params[QUERY_PARAM_PROJECT],
                page_num=page_num,
                page_size=page_size
            )

        return response_json, status_code

    """
    Gets a total count of the views over a time window of a month or week for a specific article
    Required: month, year, name
    Optional: time_window_size, start_day
    """
    def do_get_view_count_for_article_for_time_window(self, query_params):
        issues = validate_params(query_params, day_required=True)
        gateway = WikiGateway()

        if len(issues) > 0:
            issue_dict = {'issues': issues}
            response_json = json.dumps(issue_dict)
            status_code = STATUS_BAD_REQ
        else:
            response_json, status_code = gateway.get_view_count_for_article_for_time_window(
                name=query_params[QUERY_PARAM_NAME],
                month=query_params[QUERY_PARAM_MONTH],
                year=query_params[QUERY_PARAM_YEAR],
                start_day=query_params[QUERY_PARAM_START_DAY],
                time_window_size=query_params[QUERY_PARAM_TIME_WINDOW_SIZE],
                projects=query_params[QUERY_PARAM_PROJECT]
            )
        return response_json, status_code

    """
    Finds the day a specific article was most viewed given a month
    Required: month, year, name
    """
    def do_get_day_of_most_view_for_article_in_given_month(self, query_params):
        issues = validate_params(query_params)
        gateway = WikiGateway()

        if len(issues) > 0:
            issue_dict = {'issues': issues}
            response_json = json.dumps(issue_dict)
            status_code = STATUS_BAD_REQ
        else:    
            response_json, status_code = gateway.day_of_most_views_for_article_in_given_month(
                name=query_params[QUERY_PARAM_NAME],
                month=query_params[QUERY_PARAM_MONTH],
                year=query_params[QUERY_PARAM_YEAR],
                projects=query_params[QUERY_PARAM_PROJECT]
            )

        return response_json, status_code
    
    def instructions(self):
        instructions = {'instructions': 'Please see our ReadME for help!'}
        return instructions, STATUS_OK

"""
Create a dictionary of parameters that are expected for validation
"""
def parse_parameters(query_params):
    params_list = query_params.split(QUERY_PARAM_DELIMITER) if query_params else []
    all_params = {
        QUERY_PARAM_NAME: None,
        QUERY_PARAM_MONTH: None,
        QUERY_PARAM_PROJECT : None,
        QUERY_PARAM_YEAR : None,
        QUERY_PARAM_START_DAY: None,
        QUERY_PARAM_TIME_WINDOW_SIZE: None,
        QUERY_PARAM_PAGE_NUM: None,
        QUERY_PARAM_PAGE_SIZE: None 
    }
    for param in params_list:
        key, value = param.split(QUERY_VALUE_DELIMITER)
        if key not in all_params:
            all_params[key] = None
        all_params[key] = value
    
    return all_params    


if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort)) 
    try:
            webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close() 
        print("Server stopped.")