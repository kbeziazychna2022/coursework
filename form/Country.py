from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, ValidationError
from wtforms import validators


def valid(FlaskForm, field):
    if int (field.data) <= 1000:
        raise ValidationError ('Only more than 1000')
class EditCountry (FlaskForm):
    name = StringField("name: ", [
        validators.DataRequired("Please enter name."),
        validators.Length(3,10, "you should input 2<name<10")

    ])

    population = StringField("population: ", [
        validators.DataRequired("Please enter your population."), valid
    ])

    client_documents = StringField("client_documents: ", [
        validators.DataRequired("Please enter your doc.")

    ])
    goverment = StringField("goverment: ", [
        validators.DataRequired("Please enter goverment.")
    ])
    location = StringField ("location: ", [
        validators.DataRequired ("Please enter location.")
    ])
    submit = SubmitField("Save")


class CreateCountry (FlaskForm):
    name = StringField("name: ", [
        validators.DataRequired("Please enter name.")

    ])

    population = StringField("population: ", [
        validators.DataRequired("Please enter your population.")

    ])

    client_documents = StringField("client_documents: ", [
        validators.DataRequired("Please enter your doc.")

    ])
    goverment = StringField("goverment: ", [
        validators.DataRequired("Please enter goverment.")
    ])
    location = StringField ("location: ", [
        validators.DataRequired ("Please enter location.")
    ])
    submit = SubmitField("Save")