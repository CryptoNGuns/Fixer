from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Przemek'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Poland!'
        },
        {
            'author': {'username': 'Arthur'},
            'body': 'I dont like Micah'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
#    return render_template('index.html', user=user)
