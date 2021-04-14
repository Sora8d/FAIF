from flask import render_template, flash, redirect, url_for, request
from application.messages import bp
from application import db
from flask_login import current_user, login_required
from application.models import User, Message, Active_Chats
from application.main.forms import EmptyForm, PostForm

@bp.route('/user/<username>/chattomg', methods=['GET','POST'])
@login_required
def messaging(username):
    user=User.query.filter_by(username=username).first_or_404()
    Mform= PostForm()
    if Mform.validate_on_submit():
        Msg= Message(body=form.post.data, author= current_user, recipient= user)
        db.session.add(Msg)
        db.session.commit()
    return 'Hello'
