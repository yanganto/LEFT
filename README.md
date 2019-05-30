# LEFT
Listen Everything  From Tweets [![Build Status](https://travis-ci.org/yanganto/LEFT.svg?branch=master)](https://travis-ci.org/yanganto/LEFT)

# Usage
## Install Python 3.6+ and python packages

- install python3.6+
  - please refer [https://www.python.org/](https://www.python.org/)

- install python packages 
  - `pip install -r requirements.txt`
  - if you have multiple python, you may use following command to avoid problem
  - `python3.6 -m pip install -r requirements.txt`

## Run test
  - `py.test`


## Run Service

- run service on 8080 (default) port
  - `python3.6 main.py`

- run service on specific port
  - `python3.6 main.py [port number]`

## Make a query

- cRUL command
  - `curl -H "Accept: application/json" -X GET http://localhost:8080/hashtags/Python?limit=40`

- try the API by living swagger document
  - `firefox http://localhost:8080/doc`
  - [swagger document page](/doc)


## Notes

The api need to be query with accept header, 
and the accept header is not suitable for flask-restplus framework.  
so I did a PR on this.  
[https://github.com/di/flask-accept/pull/8](https://github.com/di/flask-accept/pull/8)  
If there is any bug or issue, please kindly to tell me.  
Thanks.  
