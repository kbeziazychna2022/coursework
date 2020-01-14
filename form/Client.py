from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms import validators


class EditClient (FlaskForm):
    place_name = StringField("place_name: ", [
        validators.DataRequired("Please enter place name."),
        validators.Length(0,15, "0<place name<15")])

    client_fullname = StringField("client_fullname: ", [
        validators.DataRequired("Please enter your info.")

    ])

    client_documents = StringField("client_documents: ", [
        validators.DataRequired("Please enter your doc.")

    ])
    date = DateField("date: ", [
        validators.DataRequired("Please enter date in format yyyy-mm-dd.")

    ])
    submit = SubmitField("Save")


class CreateClient (FlaskForm):
    place_name = StringField("place_name: ", [
        validators.DataRequired("Please enter place name."),
        validators.Length(0,15, "0<place name<15")])

    client_fullname = StringField("client_fullname: ", [
        validators.DataRequired("Please enter your info.")

    ])

    client_documents = StringField("client_documents: ", [
        validators.DataRequired("Please enter your doc.")

    ])
    date = DateField("date: ", [
        validators.DataRequired("Please enter date in format yyyy-mm-dd.")

    ])
    submit = SubmitField("Save")

