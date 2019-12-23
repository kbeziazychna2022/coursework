from flask import Flask, request, render_template, redirect, url_for
import json
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from form.Queue import CreateQueue, EditQueue
import plotly
import plotly.graph_objs as go
from form.Client import EditClient, CreateClient
from form.Place import CreatePlace, EditPlace
from form.Schedule import CreateSchedule, EditSchedule
from form.Country import EditCountry, CreateCountry

app = Flask(__name__)

ENV = 'prod'


if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:modern23@localhost/Kate'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://ajjmpfrdoqcwmk:e25f4619f12bf07b8d859269636062939dcee7d6f8334368c5a31e25d28a10fc@ec2-174-129-33-132.compute-1.amazonaws.com:5432/d562vtttjihdv'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


db = SQLAlchemy(app)


class ormPlace(db.Model):
    __tablename__ = 'place'

    place_name = db.Column(db.String(40), primary_key=True)
    place_site = db.Column(db.String(40), nullable=False)
    type_of_service = db.Column(db.String(40), nullable=False)
    client = db.relationship("ormClient")
    queues = db.relationship("ormQueue")

class ormClient(db.Model):
    __tablename__ = 'client'

    client_fullname = db.Column(db.String(40), nullable=False)
    client_documents = db.Column(db.String(40), primary_key=True)
    place_name = db.Column (db.String (40), db.ForeignKey('place.place_name'))
    date = db.Column(db.Date, db.ForeignKey('schedule.date'))
    country = db.relationship("ormCountry")

class ormQueue(db.Model):
    __tablename__ = 'queue'

    date = db.Column(db.Date, db.ForeignKey('schedule.date'))
    place_name = db.Column(db.String(40), db.ForeignKey('place.place_name'))
    queue_name = db.Column(db.String(40), primary_key=True)
    queue_number = db.Column(db.Integer, nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    waiting_time = db.Column(db.Time, nullable=False)

class ormSchedule(db.Model):
    __tablename__ = 'schedule'

    date = db.Column (db.Date, primary_key=True)
    time_in_queue = db.Column(db.Time, nullable=False)
    push_notification = db.Column(db.String(40), nullable=False)
    queue = db.relationship("ormQueue")
    clients = db.relationship("ormClient")

class ormCountry(db.Model):
    __tablename__ = 'country'

    name = db.Column(db.String(40),primary_key=True)
    population = db.Column(db.Integer(),nullable=False)
    goverment = db.Column (db.String (40),nullable=False)
    location = db.Column(db.String(),nullable=False)
    client_documents = db.Column(db.String(40), db.ForeignKey('client.client_documents'))


'''
Client1 = ormClient(client_fullname = 'Natalia Kim', client_documents = 'HR129083' ,place_name = 'Library', date = '2019-12-21')
Client2 = ormClient(client_fullname = 'Alisha Layne', client_documents = 'HR453209' ,place_name = 'Airport', date = '2019-11-12')
Client3 = ormClient(client_fullname = 'Harry Styles', client_documents = 'HR675408' ,place_name = 'Work', date = '2019-08-09r')
Place1 =ormPlace(place_name = 'Library', place_site = 'library@gmail.com', type_of_service='booking book ...')
Place2 =ormPlace(place_name = 'Airport', place_site = 'hotel@gmail.com', type_of_service='booking room ...')
Place3 =ormPlace(place_name = 'Work', place_site = 'mc@gmail.com', type_of_service='dr. Mart ...')
Queue1 = ormQueue(date = '2019-12-21', place_name = 'Library', queue_name = 'Queue1', queue_number = 23, number_of_people = 45, waiting_time ='14:00')
Queue2 = ormQueue(date = '2019-11-12', place_name = 'Airport', queue_name = 'Queue2', queue_number = 2, number_of_people = 23, waiting_time ='10:00')
Queue3 = ormQueue(date = '2019-08-09', place_name = 'Work', queue_name = 'Queue3', queue_number = 46, number_of_people = 192, waiting_time ='22:00')
Schedule1 = ormSchedule(date = '2019-12-21', time_in_queue = '00:15', push_notification = 'your queue1')
Schedule2 = ormSchedule(date = '2019-11-12', time_in_queue = '00:11', push_notification = 'your queue2' )
Schedule3 = ormSchedule(date = '2019-08-09', time_in_queue = '00:09', push_notification = 'your queue3')
Place1.client.append(Client1)
Place2.client.append(Client2)
Place3.client.append(Client3)
Place1.queues.append(Queue1)
Place2.queues.append(Queue2)
Place3.queues.append(Queue3)
Schedule1.queue.append(Queue1)
Schedule2.queue.append(Queue2)
Schedule3.queue.append(Queue3)
Schedule1.clients.append(Client1)
Schedule2.clients.append(Client2)
Schedule3.clients.append(Client3)
db.session.add_all([Client1,Client2,Client3])
db.session.add_all([Place1,Place2,Place3])
db.session.add_all([Queue1,Queue2,Queue3])
db.session.add_all([Schedule1,Schedule2,Schedule3])
'''

@app.route('/')
def index():
    return render_template('main.html', action="/")

@app.route('/get', methods=['GET'])
def get():
    db.session.query(ormCountry).delete()
    C1 = ormCountry(name="Italy",population=30234567,goverment='Goverment4',location='22.34.55,23.45.67', client_documents='HT213478')
    C2 = ormCountry(name="Spain",population=1200003,goverment='Goverment5',location='22.00.55,98.45.67', client_documents='HE231456')
    C3 = ormCountry(name="Ukraine",population=764321,goverment='Goverment6',location='23.34.55,76.45.67', client_documents='HR129083')

    db.session.add_all([C1, C2, C3])
    db.session.commit()

    return redirect('/')

@app.route('/Client')
def all_Client():
    name = "Client"
    Client_db = db.session.query(ormClient).all()
    Client = []
    for row in Client_db:
        Client.append({"place_name": row.place_name, "client_fullname": row.client_fullname, "client_documents": row.client_documents, "date": row.date})
    return render_template('allClient.html', name=name, Client=Client, action="/Client")


@app.route('/Place')
def all_Place():
    name = "Place"

    Place_db = db.session.query(ormPlace).all()
    Place = []
    for row in Place_db:
        Place.append({"place_name": row.place_name, "place_site": row.place_site, "type_of_service": row.type_of_service})
    return render_template('allPlace.html', name=name, Place=Place, action="/Place")



@app.route('/insert')
def all_Country():
    name = "Country"

    Country_db = db.session.query(ormCountry).all()
    Country = []
    for row in Country_db:
        Country.append({"name": row.name, "population": row.population, "goverment": row.goverment, "location": row.location,"client_documents": row.client_documents})
    return render_template('allCountry.html', name=name, Country=Country, action="/insert")

@app.route('/Queue')
def all_Queue():
    name = "Queue"

    Queue_db = db.session.query(ormQueue).all()
    Queue = []
    for row in Queue_db:
        Queue.append({"date": row.date, "place_name": row.place_name, "queue_name": row.queue_name, "queue_number": row.queue_number, "number_of_people": row.number_of_people, "waiting_time": row.waiting_time})
    return render_template('allQueue.html', name=name, Queue=Queue, action="/Queue")


@app.route('/Schedule')
def all_Schedule():
    name = "Schedule"

    Schedule_db = db.session.query(ormSchedule).all()
    Schedule = []
    for row in Schedule_db:
        Schedule.append({"time_in_queue": row.time_in_queue, "date": row.date, "push_notification": row.push_notification})
    return render_template('allSchedule.html', name=name, Schedule=Schedule, action="/Schedule")



@app.route('/createClient', methods=['GET', 'POST'])
def create_Client():
    form = CreateClient()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreateClient.html', form=form, form_name="New Client", action="createClient")
        else:

            ids = db.session.query(ormClient).all()
            check = True
            for row in ids:
                if row.client_documents == form.client_documents.data:
                    check = False

            new_var = ormClient(
                place_name=form.place_name.data,
                client_fullname=form.client_fullname.data,
                client_documents=form.client_documents.data,
                date=form.date.data

            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_Client'))

    return render_template('CreateClient.html', form=form, form_name="New Client", action="createClient")


@app.route('/createPlace', methods=['GET', 'POST'])
def create_Place():
    form = CreatePlace()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreatePlace.html', form=form, form_name="New Place", action="createPlace")
        else:

            new_var = ormPlace(
                place_name=form.place_name.data,
                place_site=form.place_site.data,
                type_of_service=form.type_of_service.data,

            )

            db.session.add(new_var)
            db.session.commit()
            return redirect(url_for('all_Place'))

    return render_template('CreatePlace.html', form=form, form_name="New Place", action="createPlace")


@app.route('/createSchedule', methods=['GET', 'POST'])
def create_Schedule():
    form = CreateSchedule()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('CreateSchedule.html', form=form, form_name="New Schedule", action="createSchedule")
        else:

            ids = db.session.query(ormSchedule).all()
            check = True
            for row in ids:
                if row.date == form.date.data:
                    check = False

            new_var = ormSchedule(
                date=form.date.data,
                time_in_queue=form.time_in_queue.data,
                push_notification=form.push_notification.data

            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_Schedule'))

    return render_template('CreateSchedule.html', form=form, form_name="New Schedule", action="createSchedule")

@app.route('/createCountry', methods=['GET', 'POST'])
def create_Country():
    form = CreateCountry()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('CreateCountry.html', form=form, form_name="New Country", action="createCountry")
        else:

            ids = db.session.query(ormCountry).all()
            check = True
            for row in ids:
                if row.name == form.name.data:
                    check = False

            new_var = ormCountry(
                name=form.name.data,
                population=form.population.data,
                goverment=form.goverment.data,
                location=form.location.data,
                client_documents=form.client_documents.data

            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_Country'))

    return render_template('CreateCountry.html', form=form, form_name="New Country", action="createCountry")

@app.route('/createQueue', methods=['GET', 'POST'])
def create_Queue():
    form = CreateQueue()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('CreateQueue.html', form=form, form_name="New Queue", action="createQueue")
        else:

            ids = db.session.query(ormQueue).all()
            check = True
            for row in ids:
                if row.queue_name == form.queue_name.data:
                    check = False

            new_var = ormQueue(
                date=form.date.data,
                place_name=form.place_name.data,
                queue_name=form.queue_name.data,
                queue_number=form.queue_number.data,
                number_of_people=form.number_of_people.data,
                waiting_time=form.waiting_time.data
            )
            if check:
                db.session.add(new_var)
                db.session.commit()
                return redirect(url_for('all_Queue'))

    return render_template('CreateQueue.html', form=form, form_name="New Queue", action="createQueue")


@app.route('/deleteClient', methods=['GET'])
def delete_Client():
    client_documents = request.args.get('client_documents')

    result = db.session.query(ormClient).filter(ormClient.client_documents == client_documents).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Client'))

@app.route('/deleteQueue', methods=['GET'])
def delete_Queue():
    queue_name = request.args.get('queue_name')

    result = db.session.query(ormQueue).filter(ormQueue.queue_name == queue_name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Queue'))


@app.route('/deleteCountry', methods=['GET'])
def delete_Country():
    name = request.args.get('name')

    result = db.session.query(ormCountry).filter(ormCountry.name == name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Country'))

@app.route('/deletePlace', methods=['GET'])
def delete_Place():
    place_name = request.args.get('place_name')

    result = db.session.query(ormPlace).filter(ormPlace.place_name == place_name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Place'))


@app.route('/deleteSchedule', methods=['GET'])
def delete_Schedule():
    date = request.args.get('date')

    result = db.session.query(ormSchedule).filter(ormSchedule.date == date).one()

    db.session.delete(result)
    db.session.commit()

    return redirect(url_for('all_Schedule'))

@app.route('/editClient', methods=['GET', 'POST'])
def edit_Client():
    form = EditClient()
    client_documents = request.args.get('client_documents')
    client = db.session.query (ormClient).filter (ormClient.client_documents == client_documents).one ()
    if request.method == 'GET':
        form.place_name.data = client.place_name
        form.client_fullname.data = client.client_fullname
        form.client_documents.data = client.client_documents
        form.date.data = client.date


        return render_template('EditClient.html', form=form, form_name="Edit Client",
                               action="editClient?client_documents=" + client.client_documents)


    else:

        if not form.validate():
            return render_template('EditClient.html', form=form, form_name="Edit Client", action="editClient")
        else:

            var = db.session.query(ormClient).filter(ormClient.client_documents == client_documents).one()
            print(var)

            # update fields from form data

            var.date = form.date.data
            var.client_fullname = form.client_fullname.data
            var.client_documents = form.client_documents.data
            var.place_name = form.place_name.data
            db.session.commit()

            return redirect(url_for('all_Client'))


@app.route('/update', methods=['GET', 'POST'])
def edit_Country():
    form = EditCountry()
    name = request.args.get('name')
    country = db.session.query (ormCountry).filter (ormCountry.name == name).one()

    if request.method == 'GET':

        form.name.data = country.name
        form.population.data = country.population
        form.goverment.data = country.goverment
        form.location.data = country.location
        form.client_documents.data = country.client_documents


        return render_template('editCountry.html', form=form, form_name="Edit Country",
                               action="update?name=" + country.name)


    else:

        if not form.validate():
            return render_template('editCountry.html', form=form, form_name="Edit Country", action="update")
        else:

            var = db.session.query(ormCountry).filter(ormCountry.name == name).one()
            print(var)

            # update fields from form data

            var.name = form.name.data
            var.population = form.population.data
            var.goverment = form.goverment.data
            var.location = form.location.data
            var.client_documents = form.client_documents.data
            db.session.commit()

            return redirect(url_for('all_Country'))


@app.route('/editPlace', methods=['GET', 'POST'])
def edit_Place():
    form = EditPlace()
    place_name = request.args.get('place_name')
    place = db.session.query (ormPlace).filter (ormPlace.place_name == place_name).one ()
    if request.method == 'GET':

        form.place_name.data = place.place_name
        form.place_site.data = place.place_site
        form.type_of_service.data = place.type_of_service

        return render_template('EditPlace.html', form=form, form_name="Edit Place",
                               action="editPlace?place_name=" + place.place_name)
    else:

        if form.validate() == False:
            return render_template('EditPlace.html', form=form, form_name="Edit Place", action="editPlace")
        else:


            var = db.session.query(ormPlace).filter(ormPlace.place_name == place_name).one()
            print(var)

            var.place_name = form.place_name.data
            var.place_site = form.place_site.data
            var.type_of_service = form.type_of_service.data

            db.session.commit()

            return redirect(url_for('all_Place'))


@app.route ('/editSchedule', methods=['GET', 'POST'])
def edit_Schedule():
    form = EditSchedule()
    date = request.args.get ('date')
    schedule = db.session.query (ormSchedule).filter (ormSchedule.date == date).one ()
    if request.method == 'GET':

        form.date.data = schedule.date
        form.time_in_queue.data = schedule.time_in_queue
        form.push_notification.data = schedule.push_notification

        return render_template ('EditSchedule.html', form=form, form_name="Edit Schedule",
                                action="editSchedule?date=" + schedule.date)
    else:

        if form.validate () == False:
            return render_template ('EditSchedule.html', form=form, form_name="Edit Schedule", action="EditSchedule")
        else:

            var = db.session.query (ormSchedule).filter (ormSchedule.date == date).one ()
            print (var)

            # update fields from form data

            var.date = form.date.data
            var.time_in_queue = form.time_in_queue.data
            var.push_notification = form.push_notification.data

            db.session.commit ()

            return redirect (url_for ('all_Schedule'))


@app.route ('/editQueue', methods=['GET', 'POST'])
def edit_Queue():
    form = EditQueue()
    queue_name = request.args.get ('queue_name')
    queue = db.session.query (ormQueue).filter (ormQueue.queue_name == queue_name).one ()
    if request.method == 'GET':

        form.date.data = queue.date
        form.place_name.data = queue.place_name
        form.queue_name.data = queue.queue_name
        form.queue_number.data = queue.queue_number
        form.number_of_people.data = queue.number_of_people
        form.waiting_time.data = queue.waiting_time

        return render_template ('EditQueue.html', form=form, form_name="Edit Queue",
                                action="editQueue?queue_name=" + queue.queue_name)
    else:

        if form.validate () == False:
            return render_template ('EditQueue.html', form=form, form_name="Edit Queue", action="EditQueue")
        else:

            var = db.session.query (ormQueue).filter (ormQueue.queue_name == queue_name).one ()
            print (var)


            var.date = form.date.data
            var.place_name = form.place_name.data
            var.queue_name = form.queue_name.data
            var.queue_number = form.queue_number.data
            var.number_of_people = form.number_of_people.data
            var.waiting_time = form.waiting_time.data

            db.session.commit ()

            return redirect (url_for ('all_Queue'))


@app.route('/plot')
def dashboard():
    query1 = (
        db.session.query(
            ormQueue.number_of_people,
            ormQueue.queue_name
        ).group_by(ormQueue.queue_name)
    ).all()

    query2 = (
        db.session.query (
            ormCountry.name,
            ormCountry.population
        ).group_by (ormCountry.name)
    ).all ()

    query = (
        db.session.query(
            func.count(ormClient.client_fullname),
            ormClient.place_name
        ).group_by(ormClient.place_name)
    ).all()

    place_name, count = zip(*query)
    bar = go.Bar(
        x=count,
        y=place_name
    )

    number_of_people, queue_name = zip(*query1)
    pie = go.Pie(
        labels=queue_name,
        values=number_of_people
    )

    name, population = zip (*query2)

    bar1 = go.Bar (
        x=name,
        y=population
    )
    print(place_name, count)
    print(queue_name, number_of_people)
    print (name, population)
    data = {
        "bar": [bar],
        "pie": [pie],
        "bar1": [bar1]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('Dashboard.html', graphsJSON=graphsJSON)



if __name__ == '__main__':
    app.run()
