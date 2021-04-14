from datetime import datetime
from application import db
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import UserMixin
from application import login

from hashlib import md5

from time import time
import jwt
from flask import current_app

followers = db.Table('followers',
db.Column("follower_id", db.Integer, db.ForeignKey('user.id')),
db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(64), index=True, unique=True)
    email= db.Column(db.String(120), index=True, unique=True)
    password_hash= db.Column(db.String(128))
#Relationship with Posts table.
    posts= db.relationship('Post', backref='author', lazy='dynamic')

    about_me= db.Column(db.String(200))
    LS= db.Column(db.DateTime, default=datetime.utcnow)

#Relationship with followers table.
    followed = db.relationship('User', secondary=followers,
    primaryjoin=(followers.c.follower_id==id),
    secondaryjoin=(followers.c.followed_id==id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

#Relationship with Messages.
    messages_sent= db.relationship('Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received= db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    last_message_read_time= db.Column(db.DateTime)

#Relationship with Active_Chats.
    one_id= db.relationship('Active_Chats', foreign_keys='Active_Chats.one_id', backref='oneC', lazy='dynamic')
    two_id= db.relationship('Active_Chats', foreign_keys='Active_Chats.two_id', backref='twoC', lazy='dynamic')
#Messages functionality.
    def Get_Chats(self):
        EvChat= Message.query.filter_by(recipient_id=self.id).group_by(Message.sender_id).all()
        SevChat= Message.query.filter_by(sender_id=self.id).group_by(Message.recipient_id).all()
        Chats= set()
        for x in EvChat:
            Chats.add(x.author)
        for x in SevChat:
            Chats.add(x.recipient)
        return Chats
    def Get_Active_Chats(self, all_or='all'):
        if all_or == 'all':
            All_A_C= self.one_id.union(self.two_id).all()
            return All_A_C
        else:
            One_A_C= self.one_id.filter_by(two_id=all_or.id).union(self.two_id.filter_by(one_id=all_or.id)).first()
            return One_A_C
    def Get_Messages(self, other):
        Messages= self.messages_sent.filter_by(recipient_id=other.id).union(self.messages_received.filter_by(sender_id= other.id)).order_by(Message.timestamp)
        return Messages
#Following functionality.
    def is_following(self, user):
        return self.followed.filter(
        followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        followed= Post.query.join(followers, (followers.c.followed_id==Post.user_id)).filter(followers.c.follower_id==self.id)
        own= Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

#End of stuff about followers

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#The db.relationship is not an actual database field, but a high-level view of the
#relationship between users and postso, For a one-to-many relationship,
#this field is normally defined on the "one" side, its a convenient way to acess the "many".
#For example u.posts ('u' being a User) will return all the posts made by u.

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
        current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id=jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    def avatar(self, size):
        digest= md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    body= db.Column(db.String(140))
    timestamp= db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
#db.ForeignKey references a model by its database table name, for which SQLAlchemy
#automatically, uses lowercase and snake case (for multi-word model names)
#While for example db.relationship() calls the model referenced by the model class.
#This inconsistency is why the key is referenced with lowercase here, but upper in the user class.
    def __repr__(self):
        return '<Post {}>'.format(self.body)

#You can use User.query.all() to retrieve all users.
#If you know the id, you can use User.query.get(x)

#To access to example the posts of user u, you can use u.posts or u.posts.all().
class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(300))
    sender_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    read=db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

class Active_Chats(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    one_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    two_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    active= db.Column(db.Integer, nullable=False, default=0)
#Now the loading functions.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
