from flask_wtf import FlaskForm
from wtforms import  StringField,SelectField,TextAreaField,SubmitField
from wtforms.validators import Required
from flask_login import login_required, current_user
from flask import render_template, request, Blueprint, redirect, url_for, abort, flash
from app.models import User, Post, Comment
from . import main
from app import db
import urllib.request
from .forms import PostForm, CommentForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    #page = request.args.get('page',1,type=int)
    #posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5)
    posts = Post.query.all()

    title = "Home"
    return render_template('home.html', posts=posts, title=title)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    posts_count = Post.count_posts(uname)

    if user is None:
        abort(404)

    title = "User"

    return render_template("profile.html", user = user,title=title, posts=posts, posts_count=posts_count)


@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post(): 
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,user=current_user)

        #new_post = Post(title=title,post=post,user = current_user)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')

        return redirect(url_for('main.home')) 

    return render_template('create_post.html',form=form)


@main.route('/user/<uname>/posts')
def user_posts(uname):
    user = User.query.filter_by(username=uname).first()
    posts = Post.query.filter_by(user_id = user.id).all()
    posts_count = Post.count_posts(uname)

    return render_template("posts.html", user=user,posts=posts,posts_count=posts_count)


@main.route('/posts/all_posts')
def all_posts():

    #posts = Post.get_post()
    posts = Post.query.all()

    return render_template("all_posts.html", posts = posts)


@main.route('/post/<int:id>', methods = ['POST','GET'])
@login_required
def posts(id):
    post = Post.get_post(id)

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment = comment,user = current_user,post_id = post.id)

        new_comment.save_comment()


    comments = Comment.get_comments(post)

    return render_template("post.html", post = post, form = form, comments = comments)