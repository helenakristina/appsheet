# APPSHEET exercise

We have a simple web service that exposes some dummy people data (id, name, age, number, photo, bio).  The details of the service are below, but the goal is to make a simple app that displays the 5 youngest users with valid us telephone numbers sorted by name.  The UI for displaying the results is up to you --- this is a backend project so we don’t worry too much about the UI. You can use any third party packages / plugins / frameworks you like, and contact me with any questions. We are interested in the cleanness of code design and implementation. For “extra credit”, describe a way to automatically test the app and how the design of the end-to-end service + app should change if the dataset were three orders of magnitude larger. Thanks.

Service Endpoint

https://appsheettest1.azurewebsites.net/sample/

 

method

list

 

notes

This method will return an array of up to 10 user ids.  If there are more than 10 results the response will also contain a token that can be used to retrieve the next set of results.  This optional token can be passed as a query string parameter

ex https://appsheettest1.azurewebsites.net/sample/list or https://appsheettest1.azurewebsites.net/sample/list?token=b32b3

 

method

detail/{user id}

 

notes

This method will returns the full details for a given user 

ex http://appsheettest1.azurewebsites.net/sample/detail/21
### Usage:

- ensure virtual environment is Python 3.7+
- install requirements `pip install -r requirements.txt`
- `export PYTHONPATH=./`
- run application `make run` or `python app/app.py`
- run tests (no tests available yet) `make test` or `pytest -vvs ./tests/ --cov=app tests/`


- Note: The image directory is empty but it will fill as the app runs the first time
- If this were a real application, I would use configargparse for the web service url config
-  
TODO:
- metrics/observability
- configargparse
- tests
- More logging


#### With respect to the question of how to scale this app:

The bottleneck is currently the pagination of the web service only returning 10 IDs at once. If I had any control over the web service, I would want to try to change the contract so that I didn't need the current list.

I would certainly not use an in-memory data store like SQLITE, instead probably using a different relational database like PostgresQL on AWS RDS cluster. If the problem statement changed to doing text searches or something, I would probably consider implementing an Elasticsearch solution instead of RDBMS.

I set up the application using generators so that it would be very easy to use either coroutines with asyncio or a queue to asynchronously hit the web service to get the user data. That way, even if the above bottleneck still existed, getting the user details would still be very fast. 

If the problem space was very large and storage was less important than speed, I might move the downloading of the image out into the user detail step. 

I would probably use serverless microservice like Lambda in AWS to pick up the user URLs out of the queue and get user details that way, so they could all be running at once, depending on the contract with the web service. 

I didn't implement any exponential backoff or handling for rate-limits/honeypots, but would certainly add that in a production quality application. 


#### How I would create a testing framework for this application:
- _Unit tests_ I use pytest for unittests. I use pytest-coverage, which has an amazing html output that ensures that not only do you have coverage on each line, but it also flags a line as yellow if you only have accounted for part of the branching of the line.
- _Property-based testing_ I use hypothesis Python library to do property-based testing (in other words, it will hit the function with a bunch of integers if that is the input and sort of fuzz your function to get it to fail.) Hypothesis also persists metadata from these tests and will remember past runs of it in order to prioritize cases that didn't pass in the past.
- _Snapshot-testing_ I love using pytest with shapshot test turned on, especially in cases like this example where you are persisting and manipulating data. Instead of writing a bunch of assertions, you just take a snapshot of your objects in flight, inspect them manually to ensure that the output is not deviating from what your expectations are. In the future, if a change is made that alters the values in the snapshot, the tests will fail and you have to run them with `--snapshot-update` flag if you expected the result to change.
- _Pytest fixtures_ Using fixtures in Pytest would make sense in this case, to spin up a session of the SQLite DB and tear it down after running the tests
- _Mock_ Pytest mock would be used for mocking out interactions with the web service
- _Integration test pipeline_ After unit-test coverage is as complete as possible, I would build out an integration test in a docker container that builds and runs the app end to end. For that I would use the snapshot approach as well
- _Load testing_ I would add metrics into my logging and use a tool like logstash with Kibana to provide observability into the system at each point. NOTE: I did not do as many logs as I would need for this. For the sake of time, I decided not to do as many logs nor add tests
- _Continuous integration_ Version control hooks on Github to ensure all tests pass before merging into master
- _Linting and MyPy_ I would also run Pylint over the solution as well as MYPy to ensure type annotations are followed throughout the solution