from src.page_view_api.constants import (
    QUERY_PARAM_MONTH,
    QUERY_PARAM_PROJECT,
    QUERY_PARAM_YEAR,
    QUERY_PARAM_NAME,
    QUERY_PARAM_START_DAY,
    QUERY_PARAM_TIME_WINDOW_SIZE,
    QUERY_PARAM_WEEK_TIME_WINDOW,
    QUERY_PARAM_MONTH_TIME_WINDOW,
    QUERY_PARAM_PAGE_SIZE,
    QUERY_PARAM_PAGE_NUM,
    MONTHS_31_DAYS
)

"""
Validate all parameters
"""
def validate_params(all_params, day_required=False, name_required=True):
    issues = []
    validate_month(all_params[QUERY_PARAM_MONTH], issues)
    validate_year(all_params[QUERY_PARAM_YEAR], issues)
    validate_project(all_params[QUERY_PARAM_PROJECT], issues)
    if name_required:
        validate_name(all_params[QUERY_PARAM_NAME], issues)

    validate_day(all_params, day_required, issues)

    return issues

"""
Checks that page values are integers
"""
def validate_page_values(all_params):
    page_num = all_params[QUERY_PARAM_PAGE_NUM]
    page_size = all_params[QUERY_PARAM_PAGE_SIZE]

    issues = []
    if page_num != None:
        try:
            converted_page_num = int(page_num)
        except ValueError:
            issue = 'page num must be an integer'
            issues.append(issue)
    
    if page_size != None:
        try:
            converted_page_size = int(page_size)
        except ValueError:
            issue = 'page size must be an integer'
            issues.append(issue)

    return issues

"""
Checks that month is not none and is an integer
"""
def validate_month(month, issues):
    try:
        converted_month = int(month)
        if converted_month > 12 or converted_month < 1:
            issue = 'month must be between 1 and 12 inclusive'
            issues.append(issue)
    except ValueError:
        issue = 'month must be an integer'
        issues.append(issue)
    except TypeError:
        issue = 'month can not be none'
        issues.append(issue)

"""
Checks that year is not none and is an integer
Also checks that the year is not earlier than 2001 
since wikipedia was created then and wont have page view data before that
"""
def validate_year(year, issues):
    year_as_str = str(year)
    if len(year_as_str) != 4:
        issue = 'year must have a length of 4'
        issues.append(issue)
    try:
        converted_year = int(year)
        if converted_year < 2001:
            issue = 'wikipedia was created in 2001, no page views would occur before that'
            issues.append(issue)
    except ValueError:
        issue = 'year must be an integer'
        issues.append(issue)
    except TypeError:
        issue = 'year can not be None'
        issues.append(issue)

"""
Checks if project is either english or all. We do not support other projects
"""
def validate_project(project, issues):
    if project != None and project != 'english' and project != 'all':
        issue = 'This api only supports all or english. Please use one of those'
        issues.append(issue)

"""
Checks that name is not None
"""
def validate_name(name, issues):
    if name == None:
        issue = 'name can not be None'
        issues.append(issue)

"""
Checks that start day is present if the time window is a week. 
"""
def validate_day(all_params, required, issues):
    if not required:
        return
    
    check_day_validity = validate_time_window(all_params[QUERY_PARAM_TIME_WINDOW_SIZE], issues)
    if not check_day_validity:
        return
    
    start_day = all_params[QUERY_PARAM_START_DAY]
    month = all_params[QUERY_PARAM_MONTH]
    year = all_params[QUERY_PARAM_YEAR]

    try:
        converted_day = int(start_day)
        converted_month = int(month)
        converted_year = int(year)
        if converted_month in MONTHS_31_DAYS:
            if converted_day > 31:
                issue = 'day must be less than 31'
                issues.append(issue)
        elif converted_month == 2:
            max_day_in_feb = 28
            if converted_year % 4 == 0: # To handle leap year
                max_day_in_feb = 29
            if converted_day > max_day_in_feb:
                issue = f'day in february must be less than {max_day_in_feb} for this year'
                issues.append(issue)
        else:
            if converted_day > 30:
                issue = 'day must be less than 30'
                issues.append(issue)

    except ValueError:
        issue = 'day must be an integer'
        issues.append(issue)
    except TypeError:
        if all_params[QUERY_PARAM_TIME_WINDOW_SIZE] and all_params[QUERY_PARAM_TIME_WINDOW_SIZE] == QUERY_PARAM_WEEK_TIME_WINDOW:
            issue = 'day can not be None for a week-based time window'
            issues.append(issue)

"""
Checks that time window is week or month
Returns True if it is a window of a week and False if its a month

This is to help calculations on if we need to check the day's validity
"""
def validate_time_window(time_window, issues):
    if time_window != QUERY_PARAM_WEEK_TIME_WINDOW and time_window != QUERY_PARAM_MONTH_TIME_WINDOW:
        issue = 'time window must be either a week or a month'
        issues.append(issue)
    if time_window == QUERY_PARAM_WEEK_TIME_WINDOW:
        return True
    return False