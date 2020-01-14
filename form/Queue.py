from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, TimeField, IntegerField
from wtforms import validators


class CreateQueue (FlaskForm):
    date = DateField ("date: ", [
        validators.DataRequired ("Please enter date in format yyyy-mm-dd.")

    ])

    place_name = StringField ("place_name: ", [
        validators.DataRequired ("Please enter place_name."),
        validators.Length(0,15, "0<place name<15")

    ])

    queue_name = StringField ("queue_name: ", [
        validators.DataRequired ("Please enter queue name."),
        validators.Length (0, 15, "0<queue name<15")

    ])
    queue_number = IntegerField ("queue_number: ", [
        validators.DataRequired ("Please enter your queue number.")

    ])
    number_of_people = IntegerField ("number_of_people: ", [
        validators.DataRequired ("Please enter count people.")

    ])
    waiting_time = TimeField ("waititng_time: ", [
        validators.DataRequired ("Please enter waiting_time in format xx:xx.")

    ])

    submit = SubmitField ("Save")


class EditQueue (FlaskForm):
    date = DateField ("date: ", [
        validators.DataRequired ("Please enter date in format yyyy-mm-dd.")

    ])

    place_name = StringField ("place_name: ", [
        validators.DataRequired ("Please enter place_name."),
        validators.Length(0,15, "0<place name<15")

    ])

    queue_name = StringField ("queue_name: ", [
        validators.DataRequired ("Please enter queue name."),
        validators.Length (0, 15, "0<queue name<15")

    ])
    queue_number = IntegerField ("queue_number: ", [
        validators.DataRequired ("Please enter your queue number.")

    ])
    number_of_people = IntegerField ("number_of_people: ", [
        validators.DataRequired ("Please enter count people.")

    ])
    waiting_time = TimeField ("waititng_time: ", [
        validators.DataRequired ("Please enter waiting_time in format xx:xx.")

    ])
    submit = SubmitField ("Save")
