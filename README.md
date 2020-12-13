# Full Stack Nanodegree Capstone Project - GNSS API

**TBD/TODO: change all 127.0.0.1 to heroku URL**

## Table of Contents

1. [Background Information](#background-info)
2. [Local Setup](#local-setup)
3. [Heroku Deployment](#heroku-deployment)
3. [Roles and API Access](#roles-and-api-access)
4. [API Documentation](#api-documentation)
5. [Testing](#testing)

<a name="background-info"></a>
## Background Information

This project provides a ```RESTful``` and ```RBAC``` based ```API``` to provide data of ```GNSS satellite constellations``` [(Global Navigation Satellite Systems)](https://en.wikipedia.org/wiki/Satellite_navigation).  Data includes:
* Information about each GNSS, such as owner and number of satellites
* Information on signals names for a specific GNSS

### Strategies and Techniques Implemented

This project summarizes the concepts learned from the various courses in the Full Stack Nanodegree program: 

* Utilizing a database with models based on the [Postgres](https://www.postgresql.org/) client.  
    - The ```ORM``` used is python's ```SQLAlchemy``` (combined with ```Flask```) that contains ```CRUD``` operations.
* Generating ```REST``` APIs containing GNSS and Signals data.
* Enabling RBAC on the API endpoints using [Auth0](https://auth0.com/).
    - A role of ```GNSS Director``` can view GNSS and Signals, plus add, modify and delete GNSS and Signals.
    - A role of ```GNSS Client``` can view GNSS and Signals, but not add, modify or delete GNSS and Signals.
    - No role can only view GNSS (not view Signals).
* Deploying the project on [Heroku](https://www.heroku.com/).

<a name="local-setup"></a>
## Local Project Setup

**Note: The instructions below are for a Windows 10 platform using Python 3.8.X.**

### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Python 3.8 Addendum

Install https://visualstudio.microsoft.com/visual-cpp-build-tools.

### Project Directory

Create a folder on your PC to host the project files.  Navigate to the ```\backend``` folder (**TBD/TODO check path**) and open a command window ```(Windows Key + cmd.exe)``` at this location.

### Virtual Environment

Create the virtual environment in hte \backend folder (**TBD/TODO check path**) by running the following command:

```
python -m virtualenv env
```

For Windows 10, this means going into the ```backend\env\Scripts``` folder and running ```activate.bat``` via command prompt.  Now this command prompt has ```(env)``` in it and is the virtual environment for this project, only containing the dependencies required for it (i.e. those from requirements.txt).

### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

Also based on the Python 3.8 Addendum, a small fix is required to work with Python 3.8:

Go into ```backend\env\Lib\site-packages\sqlalchemy\util\compat.py``` and follow the instructions here: https://knowledge.udacity.com/questions/132762#132817

Also update Werkzeug:

```
pip install --upgrade Werkzeug
```

## Running the backend Flask server

Navigate to the root folder of the project (where manage.py is located) (**TBD/TODO check path**) with the virtual environment activated (```(env)``` should appear in the command prompt).

To run the server, execute:

```python manage.py runserver```

The server will start at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Database Setup

Download Postgres [Postgres](https://www.postgresql.org/).  Note the version of Postgres (e.g. 13) and perform the following commands:

#### Create the databases

```
pg_ctl -D "C:\Program Files\PostgreSQL\<Version>\data" start
dropdb -U postgres gnss
createdb -U postgres gnss
dropdb -U postgres gnss_test
createdb -U postgres gnss_test
```

Note: The ```gnss``` database is for production, ```gnss_test``` is for testing (via ```test_gnssapi.py``` script).

#### Create the gnss database tables schema

Navigate to the ```backend\src\``` folder (**TBD/TODO check path**) with the virtual environment activated (```(env)``` should appear in the command prompt) and run the following commands to create the postgres db schema (no GNSS data will be populated yet):

```
flask db init
flask db migrate
flask db upgrade
```

#### Populating the gnss database with initial data
Navigate to the ```backend\src\database``` folder (**TBD/TODO check path**) with the virtual environment activated (```(env)``` should appear in the command prompt) and run the following:

```
python populate_gnss.py
```

<a name="heroku-deployment"></a>
## Heroku Deployment

The app is located at: TBD

<a name="roles-and-api-access"></a>
## Roles and API Access

* A role of ```GNSS Director``` can view GNSS and Signals, plus add, modify and delete GNSS and Signals.
* A role of ```GNSS Client``` can view GNSS and Signals, but not add, modify or delete GNSS and Signals.
* No role (not signed into Auth0) can only view GNSS (not view Signals).

<a name="testing-accounts"></a>
### Auth0 Testing Accounts

These are fake accounts used for testing purposes to obtain JWTs to test the RBAC of the API.

| User              | Password        |
|-------------------|-----------------|
| director@gnss.com | Director1atgnss |
| client@gnss.com   | Client1atgnss   |

<a name="api-documentation"></a>
## API Documentation

Available API endpoints:

* [GET /gnss](#get-gnss)
* [GET /gnss-signals](#get-gnss-signals)
* [POST /gnss](#post-gnss)
* [POST /gnss-signals](#post-gnss-signals)
* [PATCH /gnss/gnss_id](#patch-gnss)
* [PATCH /gnss-signals/signal_id](#patch-gnss-signal)
* [DELETE /gnss/gnss_id](#delete-gnss)
* [DELETE /gnss-signals/signal_id](#delete-gnss-signal)
* [Errors](#api-errors)

<a name="get-gnss"></a>
### GET /gnss

- Fetches a dictionary of all gnss.
- Request Arguments: none
- Returns: An object with:
    - key: ```"gnss"```, value is a ```list``` of key value pairs containing:
        - key: ```"id" (str)```, value: ```int```
        - key: ```"name" (str)```, value: ```str```
        - key: ```"num_frequencies" (str)```, value: ```int```
        - key: ```"num_satellites" (str)```, value: ```int```
        - key: ```"owner" (str)```, value: ```str```
    - key: ```"success"```, value: ```true``` or ```false``` ```(boolean)```

```
curl -X GET http://127.0.0.1:5000/gnss
```

```
{
  "gnss": [
    {
      "id": 1,
      "name": "GPS",
      "num_frequencies": 3,
      "num_satellites": 32,
      "owner": "USA"
    },
    {
      "id": 2,
      "name": "Galileo",
      "num_frequencies": 4,
      "num_satellites": 36,
      "owner": "EU"
    }
  ],
  "success": true
}
```

<a name="get-gnss-signals"></a>
### GET /gnss-signals

- Fetches a dictionary of all gnss signals.
- Request Arguments: none
- Returns: An object with:
    - key ```"signal"```, value is a ```list``` of key value pairs containing:
        - key: ```"gnss_id" (str)```, value: ```int```
        - key: ```"id" (str)```, value: ```int```
        - key: ```"signal" (str)```, value: ```str```
    - key: ```"success"```, value: ```true``` or ```false``` ```(boolean)```

```
curl -X GET http://127.0.0.1:5000/gnss-signals --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZDhhYjI3ZDhhMDA2OGE5MTAzNCIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE4NjcsImV4cCI6MTYwNzg4ODI2NywiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpnbnNzIiwiZGVsZXRlOnNpZ25hbCIsImdldDpzaWduYWxzIiwicGF0Y2g6Z25zcyIsInBhdGNoOnNpZ25hbCIsInBvc3Q6Z25zcyIsInBvc3Q6c2lnbmFsIl19.eBUOWs7MowemhFsXk2Zz9oFHtdjJKTzz1GZ55osOrDpQflnvOEcF551nI0qCfyYLekLXddMdJdPGk6FmLeaahLRZbvdmKb6vENxpuUZbae9ftwSt7OnQniskAdwebyobIPFILjG1b_hIFzU9VWk9gnO2ZWRVpp0x__EAKay08ix0S8KL2ct_sA5lH6W6xg23y91PJyfEe5XnFxLUb5QVso663HdPt3o57i7teMYgM25oJkmIblnUACCc5o4cmJJKE8pQg5YQxOZah4Na16f_RNEu0OuVVU2toyg0WQrVJErI1unkJLtij81iJvmHxZIFIUDO2cS8v8602lQl3eTTRQ"
```

```
{
  "signal": [
    {
      "gnss_id": 1,
      "id": 1,
      "signal": "L1 C/A"
    },
    {
      "gnss_id": 1,
      "id": 2,
      "signal": "L1C"
    },
    {
      "gnss_id": 1,
      "id": 3,
      "signal": "L2 P(Y)"
    },
    {
      "gnss_id": 1,
      "id": 4,
      "signal": "L2C"
    },
    {
      "gnss_id": 1,
      "id": 5,
      "signal": "L5"
    },
    {
      "gnss_id": 2,
      "id": 6,
      "signal": "E1"
    },
    {
      "gnss_id": 2,
      "id": 7,
      "signal": "E5A"
    },
    {
      "gnss_id": 2,
      "id": 8,
      "signal": "E5B"
    },
    {
      "gnss_id": 2,
      "id": 9,
      "signal": "E5AltBOC"
    }
  ],
  "success": true
}
```
<a name="post-gnss"></a>
### POST /gnss

- Adds an additional gnss to the database
- Request Arguments: dictionary: ```{'name': str, 'owner': str, 'num_satellites': int, 'num_frequencies': int}```
- Returns: An object with:
    - key: ```"gnss"```, value is a ```list``` of key value pairs containing:
        - key: ```"id" (str)```, value: ```int```
        - key: ```"name" (str)```, value: ```str```
        - key: ```"num_frequencies" (str)```, value: ```int```
        - key: ```"num_satellites" (str)```, value: ```int```
        - key: ```"owner" (str)```, value: ```str```
    - key: ```"success"```, value: ```true``` or ```false``` ```(boolean)```

```
curl -X POST http://127.0.0.1:5000/gnss --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZDhhYjI3ZDhhMDA2OGE5MTAzNCIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE4NjcsImV4cCI6MTYwNzg4ODI2NywiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpnbnNzIiwiZGVsZXRlOnNpZ25hbCIsImdldDpzaWduYWxzIiwicGF0Y2g6Z25zcyIsInBhdGNoOnNpZ25hbCIsInBvc3Q6Z25zcyIsInBvc3Q6c2lnbmFsIl19.eBUOWs7MowemhFsXk2Zz9oFHtdjJKTzz1GZ55osOrDpQflnvOEcF551nI0qCfyYLekLXddMdJdPGk6FmLeaahLRZbvdmKb6vENxpuUZbae9ftwSt7OnQniskAdwebyobIPFILjG1b_hIFzU9VWk9gnO2ZWRVpp0x__EAKay08ix0S8KL2ct_sA5lH6W6xg23y91PJyfEe5XnFxLUb5QVso663HdPt3o57i7teMYgM25oJkmIblnUACCc5o4cmJJKE8pQg5YQxOZah4Na16f_RNEu0OuVVU2toyg0WQrVJErI1unkJLtij81iJvmHxZIFIUDO2cS8v8602lQl3eTTRQ" --header "Content-Type: application/json"  --data-raw "{'name': 'GLONASS', 'owner': 'Russia', 'num_satellites': 24, 'num_frequencies': 2}"
```

```
{
  "gnss": [
    {
      "id": 3,
      "name": "GLONASS",
      "num_frequencies": 2,
      "num_satellites": 24,
      "owner": "Russia"
    }
  ],
  "success": true
}
```

<a name="post-gnss-signals"></a>
### POST /gnss-signals

- Adds an additional gnss signal to the database
- Request Arguments: dictionary: ```{'signal': str, 'gnss_id': int}```
- Returns: An object with:
    - key ```"signal"```, value is a ```list``` of key value pairs containing:
        - key: ```"gnss_id" (str)```, value: ```int```
        - key: ```"id" (str)```, value: ```int```
        - key: ```"signal" (str)```, value: ```str```
    - key: ```"success"```, value: ```true``` or ```false``` ```(boolean)```

```
curl -X POST http://127.0.0.1:5000/gnss-signals --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZDhhYjI3ZDhhMDA2OGE5MTAzNCIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE4NjcsImV4cCI6MTYwNzg4ODI2NywiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpnbnNzIiwiZGVsZXRlOnNpZ25hbCIsImdldDpzaWduYWxzIiwicGF0Y2g6Z25zcyIsInBhdGNoOnNpZ25hbCIsInBvc3Q6Z25zcyIsInBvc3Q6c2lnbmFsIl19.eBUOWs7MowemhFsXk2Zz9oFHtdjJKTzz1GZ55osOrDpQflnvOEcF551nI0qCfyYLekLXddMdJdPGk6FmLeaahLRZbvdmKb6vENxpuUZbae9ftwSt7OnQniskAdwebyobIPFILjG1b_hIFzU9VWk9gnO2ZWRVpp0x__EAKay08ix0S8KL2ct_sA5lH6W6xg23y91PJyfEe5XnFxLUb5QVso663HdPt3o57i7teMYgM25oJkmIblnUACCc5o4cmJJKE8pQg5YQxOZah4Na16f_RNEu0OuVVU2toyg0WQrVJErI1unkJLtij81iJvmHxZIFIUDO2cS8v8602lQl3eTTRQ" --header "Content-Type: application/json"  --data-raw "{'signal': 'G1', 'gnss_id': 3}"
```

```
{
  "signal": [
    {
      "gnss_id": 3,
      "id": 10,
      "signal": "G1"
    }
  ],
  "success": true
}
```

<a name="patch-gnss"></a>
### PATCH /gnss/gnss_id

- Modifies an existing gnss
- URL Arguments: ```gnss_id``` is an ```int```
- Request Arguments: Any of the following key/value pairs: ```{'name': str, 'owner': str, 'num_satellites': int, 'num_frequencies': int}```
- Returns: An object with:
    - key: ```"gnss"```, value is a ```list``` of key value pairs containing:
        - key: ```"id" (str)```, value: ```int```
        - key: ```"name" (str)```, value: ```str```
        - key: ```"num_frequencies" (str)```, value: ```int```
        - key: ```"num_satellites" (str)```, value: ```int```
        - key: ```"owner" (str)```, value: ```str```
    - key: ```"success"```, value: ```true``` or ```false``` ```(boolean)```


```
curl -X PATCH http://127.0.0.1:5000/gnss/1 --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZDhhYjI3ZDhhMDA2OGE5MTAzNCIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE4NjcsImV4cCI6MTYwNzg4ODI2NywiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpnbnNzIiwiZGVsZXRlOnNpZ25hbCIsImdldDpzaWduYWxzIiwicGF0Y2g6Z25zcyIsInBhdGNoOnNpZ25hbCIsInBvc3Q6Z25zcyIsInBvc3Q6c2lnbmFsIl19.eBUOWs7MowemhFsXk2Zz9oFHtdjJKTzz1GZ55osOrDpQflnvOEcF551nI0qCfyYLekLXddMdJdPGk6FmLeaahLRZbvdmKb6vENxpuUZbae9ftwSt7OnQniskAdwebyobIPFILjG1b_hIFzU9VWk9gnO2ZWRVpp0x__EAKay08ix0S8KL2ct_sA5lH6W6xg23y91PJyfEe5XnFxLUb5QVso663HdPt3o57i7teMYgM25oJkmIblnUACCc5o4cmJJKE8pQg5YQxOZah4Na16f_RNEu0OuVVU2toyg0WQrVJErI1unkJLtij81iJvmHxZIFIUDO2cS8v8602lQl3eTTRQ" --header "Content-Type: application/json"  --data-raw "{'owner': 'America'}"
```

```
{
  "gnss": [
    {
      "id": 1,
      "name": "GPS",
      "num_frequencies": 3,
      "num_satellites": 32,
      "owner": "America"
    }
  ],
  "success": true
}
```

<a name="patch-gnss-signal"></a>
### PATCH /gnss-signals/signal_id

- Modifies an existing gnss signal
- URL Arguments: ```signal_id``` is an ```int```
- Request Arguments: Any of the following key/value pairs: ```{'signal': str, 'gnss_id': int}```
- Returns: An object with:
    - key ```"signal"```, value is a ```list``` of key value pairs containing:
        - key: ```"gnss_id" (str)```, value: ```int```
        - key: ```"id" (str)```, value: ```int```
        - key: ```"signal" (str)```, value: ```str```
    - key: ```"success"```, value: ```true``` or ```false``` ```(boolean)```

```
curl -X PATCH http://127.0.0.1:5000/gnss-signals/1 --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZDhhYjI3ZDhhMDA2OGE5MTAzNCIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE4NjcsImV4cCI6MTYwNzg4ODI2NywiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpnbnNzIiwiZGVsZXRlOnNpZ25hbCIsImdldDpzaWduYWxzIiwicGF0Y2g6Z25zcyIsInBhdGNoOnNpZ25hbCIsInBvc3Q6Z25zcyIsInBvc3Q6c2lnbmFsIl19.eBUOWs7MowemhFsXk2Zz9oFHtdjJKTzz1GZ55osOrDpQflnvOEcF551nI0qCfyYLekLXddMdJdPGk6FmLeaahLRZbvdmKb6vENxpuUZbae9ftwSt7OnQniskAdwebyobIPFILjG1b_hIFzU9VWk9gnO2ZWRVpp0x__EAKay08ix0S8KL2ct_sA5lH6W6xg23y91PJyfEe5XnFxLUb5QVso663HdPt3o57i7teMYgM25oJkmIblnUACCc5o4cmJJKE8pQg5YQxOZah4Na16f_RNEu0OuVVU2toyg0WQrVJErI1unkJLtij81iJvmHxZIFIUDO2cS8v8602lQl3eTTRQ" --header "Content-Type: application/json"  --data-raw "{'signal': 'F1'}"
```

```
{
  "signal": [
    {
      "gnss_id": 1,
      "id": 1,
      "signal": "F1"
    }
  ],
  "success": true
}
```

<a name="delete-gnss"></a>
### DELETE /gnss/gnss_id

- Deletes an existing gnss
- URL Arguments: ```gnss_id``` is an ```int```
- Request Arguments: None
- Returns: An object with:
    - key: ```delete```, value: ```gnss_id``` ```(int)```
    - key: ```"success"```, value: ```true``` or ```false``` ```(boolean)```

```
curl -X DELETE http://127.0.0.1:5000/gnss/1 --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZDhhYjI3ZDhhMDA2OGE5MTAzNCIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE4NjcsImV4cCI6MTYwNzg4ODI2NywiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpnbnNzIiwiZGVsZXRlOnNpZ25hbCIsImdldDpzaWduYWxzIiwicGF0Y2g6Z25zcyIsInBhdGNoOnNpZ25hbCIsInBvc3Q6Z25zcyIsInBvc3Q6c2lnbmFsIl19.eBUOWs7MowemhFsXk2Zz9oFHtdjJKTzz1GZ55osOrDpQflnvOEcF551nI0qCfyYLekLXddMdJdPGk6FmLeaahLRZbvdmKb6vENxpuUZbae9ftwSt7OnQniskAdwebyobIPFILjG1b_hIFzU9VWk9gnO2ZWRVpp0x__EAKay08ix0S8KL2ct_sA5lH6W6xg23y91PJyfEe5XnFxLUb5QVso663HdPt3o57i7teMYgM25oJkmIblnUACCc5o4cmJJKE8pQg5YQxOZah4Na16f_RNEu0OuVVU2toyg0WQrVJErI1unkJLtij81iJvmHxZIFIUDO2cS8v8602lQl3eTTRQ"
```

```
{
  "delete": 1,
  "success": true
}
```

<a name="delete-gnss-signal"></a>
### DELETE /gnss-signals/signal_id

- Deletes an existing gnss signal
- URL Arguments: ```signal_id``` is an ```int```
- Request Arguments: None
- Returns: An object with:
    - key: ```delete```, value: ```signal_id``` ```(int)```
    - key: ```"success"```, value: ```true``` or ```false``` ```(boolean)```

```
curl -X DELETE http://127.0.0.1:5000/gnss-signals/1 --header "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ikh5VC1aRk1qdkVoaTNRVUJMLW44QiJ9.eyJpc3MiOiJodHRwczovL2NiaHViZXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZDUwZDhhYjI3ZDhhMDA2OGE5MTAzNCIsImF1ZCI6Imduc3MiLCJpYXQiOjE2MDc4MDE4NjcsImV4cCI6MTYwNzg4ODI2NywiYXpwIjoibkhaWllLMXJ2RTVBSG81dHdjTGd2dXNoSDl2YnhpQTAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpnbnNzIiwiZGVsZXRlOnNpZ25hbCIsImdldDpzaWduYWxzIiwicGF0Y2g6Z25zcyIsInBhdGNoOnNpZ25hbCIsInBvc3Q6Z25zcyIsInBvc3Q6c2lnbmFsIl19.eBUOWs7MowemhFsXk2Zz9oFHtdjJKTzz1GZ55osOrDpQflnvOEcF551nI0qCfyYLekLXddMdJdPGk6FmLeaahLRZbvdmKb6vENxpuUZbae9ftwSt7OnQniskAdwebyobIPFILjG1b_hIFzU9VWk9gnO2ZWRVpp0x__EAKay08ix0S8KL2ct_sA5lH6W6xg23y91PJyfEe5XnFxLUb5QVso663HdPt3o57i7teMYgM25oJkmIblnUACCc5o4cmJJKE8pQg5YQxOZah4Na16f_RNEu0OuVVU2toyg0WQrVJErI1unkJLtij81iJvmHxZIFIUDO2cS8v8602lQl3eTTRQ"
```

```
{
  "delete": 1,
  "success": true
}
```

<a name="api-errors"></a>
### API Errors

If an error happens, a response will be returned as follows:
- key: ```"error"```, value is ```int```
- key: ```"message"```, value is ```str```
- key: ```"success"```, value is ```false``` ```(boolean)```

Example:
```
{
  "error": 401,
  "message": "Unauthorized",
  "success": false
}
```

<a name="testing"></a>
## Testing

**TBD/TODO - perhaps the JWTs can be stored in env variables**

The following steps allow unit testing of the end points with the local build:

1. Start the local flask server by navigating to the root directory of the project (where manage.py is located):

```python manage.py runserver```

2. Go to http://127.0.0.1:5000/ and log in using the [testing accounts](#testing-accounts).  Log out when capturing the JWT (return to the home page and log out).

3. Capture the JWT after logging in (will be on the post-log in page or in the URL under access_token).

4. In ```test_gnssapi.py```, in the ```setUp``` method, paste the JWTs for the client and director.

5. Open a command window in the ```backend\src``` folder (**TBD/TODO: folder may change**) and run the ```python test_gnssapi.py```.  Test results will be reported as OK if all tests pass.