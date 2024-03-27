

### Full Project Demo Video (5 mins)  
https://www.loom.com/share/075a2c4ad7984c8ab295e1107402e207?sid=64ed78f2-3383-4884-88e5-3167ca47008b  

### Tech Stack  
Language: Python  
API Framework: FastAPI  
Database: PostgreSQL  
Model: SQLAlchemy(Asynchronous I/O (asyncio))  
Data Validation/Serialization: Pydantic  
Database Migration: Alembic  
Authorization: JWT   
SaaS Provider:   
Plaid(sandbox)  

#### Front-end repo  
https://github.com/ScottsGit/T7CnC-Frontend


## API Documentation    
https://app.clickup.com/9014187266/v/dc/8cmk582-114/8cmk582-314  
![image](https://github.com/ScottsGit/T7CnC-Backend/assets/17536863/9a2e50cf-58b0-4c57-bae8-90496eea4753)



## Setup Project
Python 3.12  
Install Python  

### PostgreSQL
Install PostgreSQL if you have not yet: https://www.postgresql.org/download/  

### PGAdmin  
PGAdmin is for PostgreSQL management.  

### Setup Backend Using Poetry  
Poetry is like 'npm' for packages management for Python projects.  
Install Poetry: https://python-poetry.org/docs/  
poetry install  
poetry run start  

### Setup Backend Using virtual environment  
python3 -m venv env  
On Windows:  
env\Scripts\activate  
On macOS/Linux:  
source env/bin/activate  
pip install -r .\requirements.txt  
uvicorn app.main:start  


http://localhost:8888/helloworld/  
Go to http://localhost:8888/docs, you should see:  
![image](https://github.com/ScottsGit/T7CnC-Backend/assets/17536863/a5593d1f-58d5-40a8-bb9f-7d40a8d6058d)  


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

