# Tasks - simple API on fastAPI
Practice project for CRUD operations with **only** authenticated users.
![Test](coverage.svg)

-------------------------
Functionally allows:
 - creating users
 - create JWT tokens and authenticate users with it
 - create and associate tasks with authenticated users
 - CRUD operations with created tasks for authenticated users

For documentation add - **/docs** at the end of a path after setting it up 
(based on [:blue_book:](https://fastapi.tiangolo.com/features/#automatic-docs))

# Setup
locally with Docker 

    docker-compose up

locally with Uvicorn 

1. install dependencies

   
     python -m pip install -r requirements.txt

2. start uvicorn

    
    python -m uvicorn main:app



tests with Pytest

    python -m pytest

for coverage

    python -m pytest --cov