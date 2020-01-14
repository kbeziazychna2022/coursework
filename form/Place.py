from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField


class CreatePlace (FlaskForm):
    place_name = StringField ("place_name: ", [
        validators.DataRequired ("Please enter place name."),
        validators.Length (3, 15, "3<Place name<15 .")

    ])

    place_site = EmailField ("place_site: ", [
        validators.DataRequired ("Please enter site."), validators.Length (min=6, max=50), validators.Email ()])

    type_of_service = StringField ("type_of_service: ", [
        validators.DataRequired ("Please enter your service."),
        validators.Length (0, 50, "0<Place name<50 .")

    ])

    submit = SubmitField ("Save")


class EditPlace (FlaskForm):
    place_name = StringField ("place_name: ", [
        validators.DataRequired ("Please enter place name."),
        validators.Length (3, 15, "3<Place name<15 .")

    ])

    place_site = EmailField ("place_site: ", [
        validators.DataRequired ("Please enter site."), validators.Length (min=6, max=50), validators.Email ()])

    type_of_service = StringField ("type_of_service: ", [
        validators.DataRequired ("Please enter your service."),
        validators.Length (0, 50, "0<Place name<50 .")

    ])
    submit = SubmitField ("Save")
