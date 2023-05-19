# EnvironMeet
Application Security Project on Environment Sustainability

## Setup
In your virtual environment type 
`pip install -r requirements.txt`
`set FLASK_APP=run.py`
`set FLASK_ENV=development`

### Creating your own local database.    
In the MySQL command line, execute the following commands:                 
`CREATE DATABASE environmeet_db;`     
`CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'fake_password';`         
`GRANT ALL PRIVILEGES ON environmeet_db.* TO 'test_user'@'localhost';
FLUSH PRIVILEGES;`

Create your own .env file with the contents
`DB_PASSWORD='fake_password'`

## Run
Finally to run you application, in your virtual environment type:
`flask run`
