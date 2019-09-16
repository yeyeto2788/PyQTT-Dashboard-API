# PyQTT-Dashboard-API
Python dashboard and API for MQTT messages stored in a database.

This Python application let's you record messages from a given `server:port`  
into a SQLite database when each message is received.

At the same time you can do multiple operations through the web page and also
by the application.

## Changelog
All changes on the application are reflected on the [CHANGELOG](./CHANGELOG.md)
file on the root directory of this repository.

## Installation

## Running the application
There are several way to run the application depending on how you want to run the application.

### Running it on a local machine

- Clone this repository.

  `git clone https://github.com/yeyeto2788/PyQTT-Dashboard-API.git`
    
- Create a virtual environment.

  `python3 -m virtualenv venv`
    
- Activate the virtual environment.

  - Linux: `source ./bin/activate` 
  
  - Windows: `.\venv\Scripts\activate`
    
- Install required dependencies.

  `pip install -r requirements.txt`

- Start celery

  - Linux:
    
    `celery worker -A pyqtt_application.extensions.celery --loglevel=info`
  
  - Windows:
    `celery worker -A pyqtt_application.extensions.celery --pool=solo --loglevel=info`
    
- Create the database.

  `manage.py db create`
    
- Run the server on development mode.

  - Development mode.
    
    `manage.py dev run`
  
  - Production mode.
  
    `manage.py runserver`

### Running it on Docker

- Docker step 1
- Docker step 2
- Docker step 3

## Contributing
If you're interested on contributing on this project you're more that welcome as
 long as you follow our [contributing](./CONTRIBUTING.md) guide.

## See any issue?
Please, if you see any issue on the app or you want us to implement a new
feature please open up an
[issue](https://github.com/yeyeto2788/PyQTT-Dashboard-API/issues/new/choose)
