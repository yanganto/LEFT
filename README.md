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

- (optionnal) set up Twitter api token as environment varable for the server
  - `export TWITTER_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Run test
  - run test case at project root
  - `python3 -m pytest`


## Run Service
### run with TWITTER\_TOKEN environment varlable
- run service on 8080 (default) port
  - `python3.6 left.py`

- run service on specific port
  - `python3.6 left.py -p [port number]`

### run without environment varlable setting
- run service with Twitter API Token option
  - `python3.6 left.py -t [api token]`

- run service with Twitter API Keys options
  - `python3.6 left.py -k [api key] -s [api secret key]`


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
