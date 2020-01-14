from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField
from wtforms import validators


class CreateSchedule (FlaskForm):
    time_in_queue = TimeField ("time: ", [
        validators.DataRequired ("Please enter your time in format xx:xx.")

    ])

    date = DateField ("date: ", [
        validators.DataRequired ("Please enter date in format xxxx-xx-xx.")

    ])
    push_notification = StringField ("not: ", [
        validators.DataRequired ("Please enter your not."),
        validators.Length (0, 50, "0<notification<50 .")
    ])

    submit = SubmitField ("Save")



class EditSchedule (FlaskForm):
    time_in_queue = TimeField ("time: ", [
        validators.DataRequired ("Please enter your time in format xx:xx.")

    ])
    push_notification = StringField ("not: ", [
        validators.DataRequired ("Please enter your not."),
        validators.Length (0, 50, "0<notification<50 .")
    ])

    submit = SubmitField ("Save")
