Fixer.cy - my side business webpage source code
-09.06.2023 - fixer.cy page is down due to hosting change -

 Q: Why do I share it to you?

 A: Actually, I am sharing it to my potential PRIMARY business partners (who are looking for skilled DevOPS engineers) to show them my Python/SQLAlchemy/Postgres skills level :) But if you find my code useful, feel free to explore and use it!


# Prerequisites:
0. Linux/MacOS/WSL 2
1. Python3
2. PostgreSQL database up and running

# Installation and configuration of Postgres Database :
1. Install and configure docker
2. Create linux user 'postgres', ensure it has the '/home/postgres' directory
3. Add the 'postgres' user to the 'docker' group 
```
sudo usermod -aG docker postgres
```
4. Create the 'postgres_data' directory as we will obey the 'immutable infrastructure' approach
```
mkdir -p /home/postgres/postgres_data
```
6. Check the linux id of the 'postgres' user
 ```
$ id
uid=1001(postgres) gid=1002(postgres) groups=1002(postgres),1001(docker)
```
7. Create the 'postgres_container' directory, and navigate to it
```
mkdir -p /home/postgres/postgres_container
cd /home/postgres/postgres_container
```
9. Create the 'docker-compose.yml' file, remember to put your values instead of the <...> fields:
```
version: '3.1'

services:
  db:
    user: "<POSTGRES_USER_UID>:<POSTGRES_USER_GID>"
    image: postgres
    restart: always
    environment:
      POSTGRES_PASSWORD: <FIXER_USER_PASSWORD>
      POSTGRES_USER: fixer
      POSTGRES_DB: fixer_db
    ports:
     - 5432:5432
    volumes:
     - /home/postgres/postgres_data:/var/lib/postgresql/data

  adminer:
    image: adminer
    restart: always
    ports:
      - 8080:8080
```
8. Run the container by launching the following command inside the 'postgres_container' directory:
```
docker compose up
```


# Installation and configuration of Flask :
Create virtual environment in your python setup:
0. pwd -> (should return): ||SOMETHING||/Fixer
```pwd```
1. Create and navigate to the './run' directory
```
mkdir -p ./run
cd ./run
```
2. Create, configure and activate the virtual environment:
```
python3 -m venv venv
virtualenv -p python3 venv
source venv/bin/activate
```
8. Install dependencies:
```
(venv) $ pip install flask flask-wtf flask-sqlalchemy flask-migrate psycopg2-binary flask-login email-validator flask-socketio python-dotenv elasticsearch
```
9. Set database URL - create a new environment variable called DATABASE_URL as below, but put your database credential inside <...> fields
```
(venv) $ export DATABASE_URL="postgresql://fixer:<FIXER_USER_PASSWORD>@<DATABASE_IP>:5432/fixer_db"
```
10. Initialize the database in the main directory
```
cd ..
(venv) flask db upgrade
```



# Run
```
(venv) $ flask run --host=0.0.0.0 -p 1990
```
use the port 1990 or the other that you choose :)
