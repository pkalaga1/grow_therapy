## Page View API

#### Description
##### This API wraps the Wikipedia Page views api. It gets aggregated data by week or month instead of just by day as provided by the Wikipedia api. 

#### Gotchas
##### In the event of a 404, the wikipedia api could not find the result for the given dates. Try changing the date before trying again.
##### This api only supports projects from wikipedias "all-projects" and "en.wikipedia". If you get a 404, try changing the project to the other option

### GET requests for aggregated page view data

<details>
 <summary><code>GET</code> <code><b>/</b></code> <code>(gives instructions to see our ReadMe) </code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        |  { <br>"instructions": "Please see our ReadME for help!" <br> }                                                          |

##### Example cURL

> ```javascript
>  curl -X GET -H "Content-Type: application/json" http://localhost:8080/
> ```

</details>

<details>
 <summary><code>GET</code> <code><b>/day_article_most_viewed_in_month</b></code> <code>(returns the day an article had the most views in a given month)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                         |
> |-------------------|-----------|----------------|-------------------------------------|
> | `name` |  required | str   | The name of the article you are looking for        |
> | `month` |  required | int   | The month that you are checking for the max views       |
> | `year` |  required | int   | The year that you are checking for the max views       |
> | `project` |  optional | str   | limit the scope of the search to specific wikipedia zones. currently supports all or english      |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | { <br> 'date': '2019-10-08',<br> 'name': 'Albert_Einstein',<br>'url': "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/test/daily/20211001/20211031",<br> 'views': 22903 <br> }                                                          |
> | `400`         | `application/json`                | {<br> "issues": ["month can not be none", "year can not be None", "name can not be None"]<br>}                            |
> | `404`         | `application/json`        |  { <br>"detail": "The date(s) you used are valid, but we either do not have data for those date(s), or the project you asked for is not loaded yet. Please check documentation for more information.", "method": "get", "status": 404, "title": "Not Found", "type": "about:blank", "uri": "/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/test/daily/20211001/20211031"<br> } 

##### Example cURL

> ```javascript
>  curl -X GET -H "Content-Type: application/json" "http://localhost:8080/day_article_most_viewed_in_month?month=10&name=test&year=2021&project=english"   
> ```

</details>

<details>
  <summary><code>GET</code> <code><b>/view_count_for_article_for_time_window</b></code> <code>(gets the total view count for a time period of a week or a month)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                         |
> |-------------------|-----------|----------------|-------------------------------------|
> | `name` |  required | str   | The name of the article you are looking for        |
> | `month` |  required | int   | The month that you are checking for the max views       |
> | `year` |  required | int   | The year that you are checking for the max views       |
> | `project` |  optional | str   | limit the scope of the search to specific wikipedia zones. currently supports all or english      |
> | `time_window_size` |  optional | str   | default: month ; Must be either month or week. Determines size of window we look at for aggregating view count     |
> | `start_day` |  optional | str   | required if the time_window_size is week. Determines the start day of the window. It is default to day 1 if time_window_size is month     |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | { <br> 'start_date': '2019-10-27', <br> 'time_window_size': 'week', <br> 'name': 'Albert_Einstein',<br> 'url': 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/20191027/20191103',<br> 'views': 128736 <br>}                                                          |
> | `400`         | `application/json`                | {<br> "issues": ["month can not be none", "year can not be None", "name can not be None"]<br>}                            |
> | `404`         | `application/json`        |  { <br>"detail": "The date(s) you used are valid, but we either do not have data for those date(s), or the project you asked for is not loaded yet. Please check documentation for more information.", "method": "get", "status": 404, "title": "Not Found", "type": "about:blank", "uri": "metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/Albert_Einstein/daily/20191027/20191103"<br> } `                            |

##### Example cURL

> ```javascript
>  curl -X GET -H "Content-Type: application/json" "http://localhost:8080/view_count_for_article_for_time_window?month=10&name=Albert_Einstein&year=2019&project=english&time_window_size=week&start_day=27"
> ```

</details>


<details>
  <summary><code>GET</code> <code><b>/most_viewed_articles_for_time_window</b></code> <code>(Gets and ranks the top articles for a week or month time window)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                         |
> |-------------------|-----------|----------------|-------------------------------------|
> | `month` |  required | int   | The month that you are checking for the max views       |
> | `year` |  required | int   | The year that you are checking for the max views       |
> | `project` |  optional | str   | Default: all; limit the scope of the search to specific wikipedia zones. currently supports all or english      |
> | `time_window_size` |  optional | str   | default: month ; Must be either month or week. Determines size of window we look at for aggregating view count     |
> | `start_day` |  optional | str   | required if the time_window_size is week. Determines the start day of the window. It is default to day 1 if time_window_size is month     |
> | `page_size` |  optional | int   | Default: 10; Determines how many results you get back     |
> | `page_num` |  optional | int   | Default: 0; Determines which page you are looking at     |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | {<br> "year": "2017",<br> "month": "12",<br> "time_window_size": "month",<br> "start_day": "01",<br> "issues": [],<br> "page_num": 0,<br> "page_size": 2,<br> "rankings": [<br> &nbsp;&nbsp;&nbsp;&nbsp;{<br>&nbsp;&nbsp;&nbsp;&nbsp;"article_name": "Main_Page",<space><br> &nbsp;&nbsp;&nbsp;&nbsp;"views": 502712036,<br> &nbsp;&nbsp;&nbsp;&nbsp;"rank": 1<br> &nbsp;&nbsp;&nbsp;&nbsp;},<br> &nbsp;&nbsp;&nbsp;&nbsp;{<br> &nbsp;&nbsp;&nbsp;&nbsp;"article_name": "Special:Search",<br> &nbsp;&nbsp;&nbsp;&nbsp;"views": 55883689,<br> &nbsp;&nbsp;&nbsp;&nbsp;"rank": 2<br> &nbsp;&nbsp;&nbsp;&nbsp;}<br> ] <br>}                                                          |
> | `400`         | `application/json`                | {<br> "issues": ["month can not be none", "year can not be None", "name can not be None"]<br>}                            |
> | `404`         | `application/json`        |  { <br>"detail": "The date(s) you used are valid, but we either do not have data for those date(s), or the project you asked for is not loaded yet. Please check documentation for more information.", "method": "get", "status": 404, "title": "Not Found", "type": "about:blank", "uri": "/metrics/pageviews/top/all_projects/all-access/2018/11/01"<br> } `                            |

##### Example cURL

> ```javascript
>  curl -X GET -H "Content-Type: application/json" "http://localhost:8080/most_viewed_articles_for_time_window?month=12&name=test&year=2017&time_window_size=month&project=english&page_num=0&page_size=2"
> ```

</details>
