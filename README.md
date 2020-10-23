# FreeMemo

## Don't pay for the ability to learn!

# Prerequisites:
0. Linux
1. Python3
2. PostgreSQL database up and running


# Installation:
Create virtual environment in your python setup:

0. pwd -> (should return): ||SOMETHING||/FreeMemo  
1. cd ./run
2. python3 -m venv venv
3. virtualenv venv
4. source venv/bin/activate
5. (venv) $ pip install flask
6. (venv) $ pip install flask-wtf
7. (venv) $ pip install flask-sqlalchemy
8. (venv) $ pip install flask-migrate
9. (venv) $ pip install psycopg2-binary

10.(venv) $pip install flask-login

Set database URL (you need to install and create PostgresSQL database named 'freememo_db', expose its port and create user 'freememo' who has all privileges granted to 'freememo_db' database ), after that create new environment variable called DATABASE_URL as below, but put your database credential inside <...> fields

(venv) $ DATABASE_URL="postgresql://freememo:<FREEMEMO_USER_PASSWORD>@<DATABASE_IP>:<DATABASE_PORT>/freememo_db"

# Run
(venv) $ flask run --host=0.0.0.0
