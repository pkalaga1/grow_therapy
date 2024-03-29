# Page View Wrapper API

### Documentation
Please see the api_spec.md for the api documentation (this would be a link if the github was public)

<details>
<summary> Startup the app </summary>
I suggest using a python virtual environment for this projects installation. I used
<br><code>python3 -m venv myenv</code>
<br><code>source ./myenv/bin/activate</code>
<br> You will want to install all the dependencies in that virtual env using
<br><code>poetry install</code>

[if you dont have poetry, you should download it following these instructions](https://python-poetry.org/docs/#installation)
<br> To start the webserver, run
<br><code>python3 main.py</code>
<br>From here, just follow the api documentation!

You can either navigate to localhost:8080 on your browser and add the query params into the url, or you can make curl calls. Both will work.

</details>

<details>
    <summary> Running the tests</summary>
This project has both integration and unit tests
<br> To run the unit tests navigate to the <code>grow_therapy</code> directory
<br><code>python -m unittest discover test</code>
<br> this will find all the unittest files in the test directory and run them
<br> To run the integration tests you should start up the webserver following the instructions above then run
<br><code>pytest test/test_integration.py</code>
<br> from the root directory
</details>

<details>
<summary>Considerations, Improvements, and Possible Next Steps</summary>
There were several decisions i made that I will detail here
<br> 1. Async API calls were not used. Due to being on a local machine, i decided not to use async calls. In an ideal world, i would have distributed computing to make the api calls in parallel then combine them afterwards. This would speed up the processing time sincethe api calls would not be blocking.
<br>2. I used a simple http server running in the main.py. In a real project, i would use something like django or flask to make the api to make it cleaner and more usable at scale. if _name__ == 'main' is not a great way to do things in production. Also, it would mean that the api tech would take care of the paths going to different methods, instead of me using an if else statement to check what path they are on.
<br>3. I chose to use a simple cache without any eviction strategies. I felt that implementing my own eviction strategy was out of scope. This is just an in memory dictionary without eviction due to the fact that there really wont be much traffic going through this api between us. Ideally, i would have eviction strategies in place in a production environment
<br>4. I chose not to use a Db. There were some thoughts of using a db to store the wikipedia data, and then using db operations to do the aggregation to make it quick and efficient. I chose not to do this because wikipedia should remain the source of truth for this data. If it ever changes, we would not want stale data in our db.
<br>5. I did not make test suites or automated tests. In general, there should be scripts to run the tests automatically during the building of the app, but i did not do that since i did not feel it necessary for the scope of the project. I would have automated testing and building in a production environment with code coverage as well to keep code quality.
<br> 6. I chose to interperet the month time window as the entire month given, rather than a month from the day given. This made more sense because i wouldnt be sure what exactly was the size of that time window. I did, however, do that way for the week because that made more sense than trying to determine which week a particular day fell in and computing that. 
<br>7. I implemented the cache because the wikipedia api has a daily limit of 200 requests per user agent. This is not really an api that you can use at scale. I didnt want to duplicate calls in a session to make sure not to reach the 200 during a testing session. The only way around this would be changing the user agent every time you start a new session. The way to do that would be to use a config or helm file to change that value as necessary in case we wanted to do larger testing.
<br>8. I chose to only implement en.wikipedia and all-projects. In a future build, i would like to include every single project wikipedia has for full coverage. As of now, for an MVP, i chose to go with only the 2 afore mentioned projects.
<br>9. I did not create a helpers file. For future code cleanliness i believe that would be the best way to add the helping methods, but due to the scope being limited i chose not to do that for the sake of time.
</details>
