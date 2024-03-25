## API Documentation    
https://app.clickup.com/9014187266/v/dc/8cmk582-114/8cmk582-314  



## Setup Project
Install Python  

### Poetry  
Poetry is like 'npm' for packages management for Python projects.  
Install Poetry: https://python-poetry.org/docs/  

### PostgreSQL
Install PostgreSQL if you have not yet: https://www.postgresql.org/download/  

### PGAdmin  
PGAdmin is for PostgreSQL management.  

### Setup Backend
poetry install  
poetry run start  

http://localhost:8888/helloworld/  
Go to http://localhost:8888/docs, you should see:  
![image](https://github.com/ScottsGit/T7CnC-Backend/assets/17536863/221d30d1-0c4f-4ea8-98e1-8168be13444b)  

### Database migration  
python3 -m venv env  

On Windows:  
env\Scripts\activate  
On macOS/Linux:  
source env/bin/activate  

Set Up Alembic Configuration: Initialize Alembic in your project by running the following command in your project directory:  
(env) alembic init -t async migrations  

Configure Alembic: Edit the alembic.ini file to specify your database connection URI. Modify the sqlalchemy.url parameter to point to your database.  

Generate Initial Migration: Generate an initial migration script based on your existing SQLAlchemy models.  
(env) alembic revision --autogenerate -m "initial migration"   

Apply Migration: Apply the migration to your database by running the following command:  
(env) alembic upgrade head  

Leave virtual env:  
deactivate  
You should see the tables in db:
![image](https://github.com/ScottsGit/T7CnC-Backend/assets/17536863/e4b79a89-7b47-4809-9a70-16b4b92aeed2)
