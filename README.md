# Page View Wrapper API

### Documentation
Please see the api_spec.md for the api documentation (this would be a link if the github was public)

<details>
<summary> Startup the app </summary>
I suggest using a python virtual environment for this project
<br><code>python3 -m venv myenv</code>
<br><code>source ./myenv/bin/activate</code>
<br> You will want to install all the dependencies in that virtual env using
<br><code>poetry install</code>

[if you dont have poetry, you should download it following these instructions](https://python-poetry.org/docs/#installation)
<br> To start the webserver, run
<br><code>python3 src/page_view_api/main.py</code>
<br>From here, just follow the documentation!

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