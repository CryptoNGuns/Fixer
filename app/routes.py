from flask import render_template,flash , redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfile, EmptyForm, PostForm
from app.models import User, Post
from datetime import datetime
from flask_socketio import SocketIO
from flask import g
from app.forms import SearchForm
from flask_babel import get_locale
from flask_babel import _

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
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    number_of_pages=posts.pages
    pages_list = []
    for page_num in range(number_of_pages):
        pages_list.append(url_for('index', page=page_num+1))
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title='Home', posts=posts.items, form=form, next_url=next_url, prev_url=prev_url, number_of_pages=number_of_pages, pages_list=pages_list, current_page=page)
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
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

        #this try and catch block hides search window when elasticsearch is not working properly
        try:
            if app.elasticsearch.info() is None:
                g.search_form = None
            else:
                g.search_form = SearchForm()
        except Exception:
            pass
    g.locale = str(get_locale())

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
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    next_url = url_for('profile', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    number_of_pages = posts.pages
    pages_list = []
    for page_num in range(number_of_pages):
        pages_list.append(url_for('profile',username=user.username,page=page_num + 1))
    prev_url = url_for('profile', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None

    form = EmptyForm()
    return render_template('profile.html', user=user, posts=posts, form=form, next_url=next_url, prev_url=prev_url, number_of_pages=number_of_pages,
                           pages_list=pages_list, current_page=page)
    

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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    number_of_pages = posts.pages
    pages_list = []
    for page_num in range(number_of_pages):
        pages_list.append(url_for('explore', page=page_num + 1))
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html', title='Explore', posts=posts, next_url=next_url, prev_url=prev_url, number_of_pages=number_of_pages,
                           pages_list=pages_list, current_page=page)

@app.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               app.config['POSTS_PER_PAGE'])
    next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
        if total > page * app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


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