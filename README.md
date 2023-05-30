# Fixer.cy - my side business webpage source code

 Q: Why I share it to you?

 A: Actually, I am sharing it to my potential PRIMARY business partners (who are looking for DevOPS engineers) to let them know my  Python skills level xD But if you find my code useful, feel free to explore!


# Prerequisites:
0. Linux/MacOS/WSL 2
1. Python3
2. PostgreSQL database up and running


# Installation:
Create virtual environment in your python setup:

0. pwd -> (should return): ||SOMETHING||/Fixer  
1. cd ./run
2. python3 -m venv venv
3. virtualenv -p python3 venv
4. source venv/bin/activate
5. (venv) $ pip install flask
6. (venv) $ pip install flask-wtf
7. (venv) $ pip install flask-sqlalchemy
8. (venv) $ pip install flask-migrate
9. (venv) $ pip install psycopg2-binary
10. (venv) $ pip install flask-login
11. (venv) $ pip install email-validator
12. (venv) $ pip install flask-socketio
13. (venv) $ pip install python-dotenv


Set database URL (you need to install and create PostgresSQL database named 'fixer_db', expose its port and create user 'fixer' who has all privileges granted to 'fixer_db' database ), after that create new environment variable called DATABASE_URL as below, but put your database credential inside <...> fields

(venv) $ DATABASE_URL="postgresql://fixer:<FREEMEMO_USER_PASSWORD>@<DATABASE_IP>:<DATABASE_PORT>/fixer_db"

# Run
(venv) $ flask run --host=0.0.0.0
