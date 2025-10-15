from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .models import MessageModel

messages = Blueprint('messages', __name__)

@messages.route("/msg", methods=['GET', 'POST'])
def msg():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        subject = request.form.get('subject')  # Optional

        # Insert into MongoDB
        MessageModel.insert_message(name, email, message, subject)

        flash("Message sent successfully!", "success")
        return redirect(url_for('messages.msg'))

    return render_template('base.html')
