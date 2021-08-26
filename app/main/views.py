from flask_wtf import FlaskForm
from wtforms import  StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required
from flask_login import login_required, current_user
from flask import render_template, request, Blueprint, redirect, url_for, abort
from app.models import User, Post
from . import main
from app import db
import urllib.request

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5)
    return render_template('home.html', posts=posts)


@main.route('/profile/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    title = "User"
    return render_template("profile.html", user = user,title=title)