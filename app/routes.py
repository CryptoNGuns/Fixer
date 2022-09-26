from flask import render_template,flash , redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfile, EmptyForm, PostForm
from app.models import User, Post
from datetime import datetime
from flask_socketio import SocketIO

socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        #new_post = Post(body=form.post.data, user_id=current_user.id) #both forms are working, but author use backends relationship instead of direct database modification
        new_post = Post(body=form.post.data, author=current_user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    posts = current_user.followed_posts().paginate(1, 10, False).items

    return render_template('index.html', title='Home', posts=posts, form=form)
#    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('User does not exist')
            return redirect(url_for('login'))
        elif not user.check_password(form.password.data):
            flash('Incorrect password provided')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.before_request
def before_request_func():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! You can login now')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    
@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    #posts = Post.query.filter_by(user_id=user.id) # this also works but below we are using relation
    posts = user.posts.all()
    form = EmptyForm()
    return render_template('profile.html', user=user, posts=posts, form=form)
    

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username_field.data
        current_user.about_me = form.about_me_field.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile',username=current_user.username))
    elif request.method == 'GET': 
        form.username_field.data = current_user.username
        form.about_me_field.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=current_user)
    
    
@app.route('/follow_frontend/<username>', methods=['POST'])
@login_required
def follow_frontend(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('profile', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('index'))
    
    
@app.route('/unfollow_frontend/<username>', methods=['POST'])
@login_required
def unfollow_frontend(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('profile', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You  unfollowing {}!'.format(username))
        return redirect(url_for('profile', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)


@app.route('/websocket')
def websocket():
    return render_template('websocket_temp.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

shared_variable = None

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@socketio.on('timer')
def handle_timer_event():
    global shared_variable
    shared_variable = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    socketio.emit('newnumber', {'date_now': shared_variable})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)