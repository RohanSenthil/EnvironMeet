# EnvironMeet
Application Security Project on Environment Sustainability

## Setup
In your virtual environment type     
`pip install -r requirements.txt`                
`set FLASK_APP=run.py`                              
`set FLASK_ENV=development`                        

### Docker Setup                       
Download Docker Desktop, Restart                               
Open Docker Desktop
Open your command line (windows) as administrator and type                      
`wsl --update --web-download`                                            
`wsl -d docker-desktop`                  
`sysctl -w vm.max_map_count=262144`             

### Creating your own local database.    
In the MySQL command line, execute the following commands:                 
`CREATE DATABASE environmeet_db;`     
`CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'fake_password';`         
`GRANT ALL PRIVILEGES ON environmeet_db.* TO 'test_user'@'localhost';
FLUSH PRIVILEGES;`

Create your own .env file with the appropriate contents

## Run
To run, in your project terminal type:                 
`docker-compose up --build`                   
                        
Finally, in your virtual environment type:                                     
`flask run`
