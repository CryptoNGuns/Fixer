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

# Run
(venv) $ flask run --host=0.0.0.0
