from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5



# just table without backend class
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    


    followed = db.relationship(
        'User', #right side is entity of relationship - left side is a parent class, I am using the same because I am pairing users to users
        secondary=followers, #name of our followers table
        primaryjoin=(followers.c.follower_id == id), #we are matching follower_id from followers table to the id field of user who follows  (left side entity)
        secondaryjoin=(followers.c.followed_id == id), # we are matching followed_id to the id field of user who will be followed (right side entity) 
        backref=db.backref('followers', lazy='dynamic'), #how relationship will be accessed from the right side entity (from left side relationship is named followed)
        lazy='dynamic') #not to run until specifically requested
    
    #for debugging
    def __repr(self):
        return '<User {}>'.format(self.username)
        
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
            ).count() > 0
            
    def followed_posts(self):
        followed_post_list = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed_post_list.union(own).order_by(Post.timestamp.desc())
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        
     
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # in db.ForeignKey we are using DATABASE names not MODEL names
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)
 


 
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    
 