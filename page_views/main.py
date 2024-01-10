from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from wiki_gateway import WikiGateway
from validate import validate_params
import markdown_to_json
from constants import (
    STATUS_OK, 
    STATUS_BAD_REQ,
    QUERY_PARAM_DELIMITER,
    QUERY_PARAM_MONTH,
    QUERY_PARAM_PROJECT,
    QUERY_PARAM_YEAR,
    QUERY_VALUE_DELIMITER,
    QUERY_PARAM_NAME
)
hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self): 

        u = urlparse(self.path)
        query_params = parse_parameters(u.query)

        response_json = None
        status_code = STATUS_OK

        
        if self.path == '/':
            status_code = STATUS_OK

        elif self.path == '/day_article_most_viewed_in_month':
            response_json, status_code = self.do_get_day_of_most_view_for_article_in_given_month(query_params)
        self.send_response(status_code)
        json_string = json.dumps(response_json)
        self.path = '/example'
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(json_string, "utf-8"))

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
        instructions = {'instructions': 'Please see our ReadME at for help!'}
    
def parse_parameters(query_params):
    params_list = query_params.split(QUERY_PARAM_DELIMITER)
    all_params = {
        QUERY_PARAM_NAME: None,
        QUERY_PARAM_MONTH: None,
        QUERY_PARAM_PROJECT : None,
        QUERY_PARAM_YEAR : None
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