from application.email import send_email
from flask import current_app, render_template

def send_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[MyPage] Reset your password',
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email],
        text_body=render_template('email/reseet_password.txt', user=user, token=token),
        html_body=render_template('email/reseet_password.html', user=user, token=token))
