from flask import render_template, current_app, flash, redirect, url_for, request
from application import db
from application.main.forms import RegisForm, EditInf, EmptyForm, PostForm
from werkzeug.urls import url_parse

from flask_login import current_user, login_user, logout_user, login_required
from application.models import User, Post

from datetime import datetime
from application.main import bp

#This deals with the pagination of the posts.
def page(url, needs, username1=False):
    page= request.args.get('page', 1, type=int)
    posts = needs.paginate(page, current_app.config['POSTS_PER_PAGE'], False)
#This is so this function can be reused for user's pages
    if username1 != False:
        next_url= url_for(url, username=username1, page=posts.next_num) \
            if posts.has_next else None
        prev_url= url_for(url, username=username1, page=posts.prev_num) \
            if posts.has_prev else None
        return posts.items, next_url, prev_url
    next_url= url_for(url, page=posts.next_num) \
        if posts.has_next else None
    prev_url= url_for(url, page=posts.prev_num) \
        if posts.has_prev else None
    return posts.items, next_url, prev_url

@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    form= PostForm()
    if form.validate_on_submit():
        post= Post(body=form.post.data, author= current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created!')
        return redirect(url_for('main.index'))
    if current_user.is_authenticated:
        posts, next_url, prev_url= page('main.index', current_user.followed_posts())
    else:
        posts= [{
        'author': {'username':'admin'},
        'body': "You're not logged in"
        }]
        next_url= None
        prev_url= None
    return render_template("index.html", title="Awful", form=form, posts=posts, next_url=next_url, prev_url=prev_url)

@bp.route("/explore")
def explore():
    posts, next_url, prev_url= page('main.explore', Post.query.order_by(Post.timestamp.desc()))
    return render_template("index.html", title="Exploration", posts=posts, next_url=next_url, prev_url=prev_url)

@bp.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form=RegisForm()
    if form.validate_on_submit():
        user= User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats u registered")
        return redirect(url_for('auth.loginn'))
    return render_template("register.html", form=form)

@bp.route('/secret')
@login_required
def secret():
    return render_template("secret.html")

@bp.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    posts, next_url, prev_url= page('main.user', user.posts.order_by(Post.timestamp.desc()), username1=user.username)
    form= EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form, next_url=next_url, prev_url=prev_url)

#This is for the profile editor
@bp.route('/profileEdit', methods=['GET','POST'])
def Edit_Profile():
    form= EditInf(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Changes saved')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.about_me.data=current_user.about_me
    return render_template('editp.html', title='Edit Profile', form=form)

@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form= EmptyForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form= EmptyForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not longer following {}!'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

#Now a function that records the last visit time for an User.
#The @before_request decorater registers the decorated function to be executed right
#before the view function.


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.LS = datetime.utcnow()
        db.session.commit()
