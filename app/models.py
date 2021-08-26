from datetime import datetime
from flask import current_app
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    encryptedpassword = db.Column(db.String(255),index=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic') 

    @property
    def password(self):
        raise AttributeError('Encrypted')

    @password.setter
    def password(self,password):
        self.encryptedpassword = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.encryptedpassword,password) 
    
    def save(self):
        db.session.add(self)
        db.session.commit()
       

    def __repr__(self):
        return f"User('{self.username}', '{self.email}'"



class Post(db.Model):
    __tablename__="posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def get_post(cls,id):
        post = Post.query.filter_by(id=id).first()

        return post

    @classmethod
    def count_posts(cls,uname):
        user = User.query.filter_by(username=uname).first()
        posts = Post.query.filter_by(user_id=user.id).all()

        posts_count = 0
        for post in posts:
            posts_count += 1

        return posts_count


    def __repr__(self):
        return f"Post('{self.title}'"


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,post):
        comments = Comment.query.filter_by(post_id=post).all()
        return comments

    def __repr__(self):
        return f"Comment('{self.comment}'"