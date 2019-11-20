from flask import Flask, request, render_template, redirect, url_for
import json
import os
from sqlalchemy import func
from form.Queue import CreateQueue, EditQueue
from source.db import PostgresDb
import source.ormmodel
import plotly
import plotly.graph_objs as go
from form.Client import EditClient, CreateClient
from form.Place import CreatePlace, EditPlace
from form.Schedule import CreateSchedule, EditSchedule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gxfthbzreuxafu:4232142b2e416b2d402d06f521afd73c5c17b77d5c1f3527548b785ebeb23a12@ec2-54-225-195-3.compute-1.amazonaws.com:5432/d42524to5vhhjb'


db = PostgresDb()

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('main.html', action="/")

@app.route('/Client')
def all_Client():
    name = "Client"
    Client_db = db.sqlalchemy_session.query(source.ormmodel.ormClient).all()
    Client = []
    for row in Client_db:
        Client.append({"place_name": row.place_name, "client_fullname": row.client_fullname, "client_documents": row.client_documents, "date": row.date})
    return render_template('allClient.html', name=name, Client=Client, action="/Client")


@app.route('/Place')
def all_Place():
    name = "Place"

    Place_db = db.sqlalchemy_session.query(source.ormmodel.ormPlace).all()
    Place = []
    for row in Place_db:
        Place.append({"place_name": row.place_name, "place_site": row.place_site, "type_of_service": row.type_of_service})
    return render_template('allPlace.html', name=name, Place=Place, action="/Place")


@app.route('/Queue')
def all_Queue():
    name = "Queue"

    Queue_db = db.sqlalchemy_session.query(source.ormmodel.ormQueue).all()
    Queue = []
    for row in Queue_db:
        Queue.append({"date": row.date, "place_name": row.place_name, "queue_name": row.queue_name, "queue_number": row.queue_number, "number_of_people": row.number_of_people, "waiting_time": row.waiting_time})
    return render_template('allQueue.html', name=name, Queue=Queue, action="/Queue")


@app.route('/Schedule')
def all_Schedule():
    name = "Schedule"

    Schedule_db = db.sqlalchemy_session.query(source.ormmodel.ormSchedule).all()
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

            ids = db.sqlalchemy_session.query(source.ormmodel.ormClient).all()
            check = True
            for row in ids:
                if row.client_documents == form.client_documents.data:
                    check = False

            new_var = source.ormmodel.ormClient(
                place_name=form.place_name.data,
                client_fullname=form.client_fullname.data,
                client_documents=form.client_documents.data,
                date=form.date.data

            )
            if check:
                db.sqlalchemy_session.add(new_var)
                db.sqlalchemy_session.commit()
                return redirect(url_for('all_Client'))

    return render_template('CreateClient.html', form=form, form_name="New Client", action="createClient")


@app.route('/createPlace', methods=['GET', 'POST'])
def create_Place():
    form = CreatePlace()

    if request.method == 'POST':
        if not form.validate():
            return render_template('CreatePlace.html', form=form, form_name="New Place", action="createPlace")
        else:

            new_var = source.ormmodel.ormPlace(
                place_name=form.place_name.data,
                place_site=form.place_site.data,
                type_of_service=form.type_of_service.data,

            )

            db.sqlalchemy_session.add(new_var)
            db.sqlalchemy_session.commit()
            return redirect(url_for('all_Place'))

    return render_template('CreatePlace.html', form=form, form_name="New Place", action="createPlace")


@app.route('/createSchedule', methods=['GET', 'POST'])
def create_Schedule():
    form = CreateSchedule()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('CreateSchedule.html', form=form, form_name="New Schedule", action="createSchedule")
        else:

            ids = db.sqlalchemy_session.query(source.ormmodel.ormSchedule).all()
            check = True
            for row in ids:
                if row.date == form.date.data:
                    check = False

            new_var = source.ormmodel.ormSchedule(
                date=form.date.data,
                time_in_queue=form.time_in_queue.data,
                push_notification=form.push_notification.data

            )
            if check:
                db.sqlalchemy_session.add(new_var)
                db.sqlalchemy_session.commit()
                return redirect(url_for('all_Schedule'))

    return render_template('CreateSchedule.html', form=form, form_name="New Schedule", action="createSchedule")

@app.route('/createQueue', methods=['GET', 'POST'])
def create_Queue():
    form = CreateQueue()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('CreateQueue.html', form=form, form_name="New Queue", action="createQueue")
        else:

            ids = db.sqlalchemy_session.query(source.ormmodel.ormQueue).all()
            check = True
            for row in ids:
                if row.queue_name == form.queue_name.data:
                    check = False

            new_var = source.ormmodel.ormQueue(
                date=form.date.data,
                place_name=form.place_name.data,
                queue_name=form.queue_name.data,
                queue_number=form.queue_number.data,
                number_of_people=form.number_of_people.data,
                waiting_time=form.waiting_time.data
            )
            if check:
                db.sqlalchemy_session.add(new_var)
                db.sqlalchemy_session.commit()
                return redirect(url_for('all_Queue'))

    return render_template('CreateQueue.html', form=form, form_name="New Queue", action="createQueue")


@app.route('/deleteClient', methods=['GET'])
def delete_Client():
    client_documents = request.args.get('client_documents')

    result = db.sqlalchemy_session.query(source.ormmodel.ormClient).filter(source.ormmodel.ormClient.client_documents == client_documents).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('all_Client'))

@app.route('/deleteQueue', methods=['GET'])
def delete_Queue():
    queue_name = request.args.get('queue_name')

    result = db.sqlalchemy_session.query(source.ormmodel.ormQueue).filter(source.ormmodel.ormQueue.queue_name == queue_name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('all_Queue'))


@app.route('/deletePlace', methods=['GET'])
def delete_Place():
    place_name = request.args.get('place_name')

    result = db.sqlalchemy_session.query(source.ormmodel.ormPlace).filter(source.ormmodel.ormPlace.place_name == place_name).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('all_Place'))


@app.route('/deleteSchedule', methods=['GET'])
def delete_Schedule():
    date = request.args.get('date')

    result = db.sqlalchemy_session.query(source.ormmodel.ormSchedule).filter(source.ormmodel.ormSchedule.date == date).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()

    return redirect(url_for('all_Schedule'))

@app.route('/editClient', methods=['GET', 'POST'])
def edit_Client():
    form = EditClient()
    client_documents = request.args.get('client_documents')
    if request.method == 'GET':

        client = db.sqlalchemy_session.query(source.ormmodel.ormClient).filter(source.ormmodel.ormClient.client_documents == client_documents).one()

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

            var = db.sqlalchemy_session.query(source.ormmodel.ormClient).filter(source.ormmodel.ormClient.client_documents == client_documents).one()
            print(var)

            # update fields from form data

            var.date = form.date.data
            var.client_fullname = form.client_fullname.data
            var.client_documents = form.client_documents.data
            var.place_name = form.place_name.data
            db.sqlalchemy_session.commit()

            return redirect(url_for('all_Client'))


@app.route('/editPlace', methods=['GET', 'POST'])
def edit_Place():
    form = EditPlace()
    place_name = request.args.get('place_name')
    if request.method == 'GET':

        place = db.sqlalchemy_session.query(source.ormmodel.ormPlace).filter(source.ormmodel.ormPlace.place_name == place_name).one()

        form.place_name.data = place.place_name
        form.place_site.data = place.place_site
        form.type_of_service.data = place.type_of_service

        return render_template('EditPlace.html', form=form, form_name="Edit Place",
                               action="editPlace?place_name=" + place.place_name)
    else:

        if form.validate() == False:
            return render_template('EditPlace.html', form=form, form_name="Edit Place", action="editPlace")
        else:


            var = db.sqlalchemy_session.query(source.ormmodel.ormPlace).filter(source.ormmodel.ormPlace.place_name == place_name).one()
            print(var)

            var.place_name = form.place_name.data
            var.place_site = form.place_site.data
            var.type_of_service = form.type_of_service.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('all_Place'))


@app.route ('/editSchedule', methods=['GET', 'POST'])
def edit_Schedule():
    form = EditSchedule()
    date = request.args.get ('date')
    if request.method == 'GET':

        schedule = db.sqlalchemy_session.query (source.ormmodel.ormSchedule).filter (source.ormmodel.ormSchedule.date == date).one ()

        form.date.data = schedule.date
        form.time_in_queue.data = schedule.time_in_queue
        form.push_notification.data = schedule.push_notification

        return render_template ('EditSchedule.html', form=form, form_name="Edit Schedule",
                                action="editSchedule?date=" + schedule.date)
    else:

        if form.validate () == False:
            return render_template ('EditSchedule.html', form=form, form_name="Edit Schedule", action="EditSchedule")
        else:

            var = db.sqlalchemy_session.query (source.ormmodel.ormSchedule).filter (source.ormmodel.ormSchedule.date == date).one ()
            print (var)

            # update fields from form data

            var.date = form.date.data
            var.time_in_queue = form.time_in_queue.data
            var.push_notification = form.push_notification.data

            db.sqlalchemy_session.commit ()

            return redirect (url_for ('all_Schedule'))


@app.route ('/editQueue', methods=['GET', 'POST'])
def edit_Queue():
    form = EditQueue()
    queue_name = request.args.get ('queue_name')
    if request.method == 'GET':

        queue = db.sqlalchemy_session.query (source.ormmodel.ormQueue).filter (source.ormmodel.ormQueue.queue_name == queue_name).one ()

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

            var = db.sqlalchemy_session.query (source.ormmodel.ormQueue).filter (source.ormmodel.ormQueue.queue_name == queue_name).one ()
            print (var)


            var.date = form.date.data
            var.place_name = form.place_name.data
            var.queue_name = form.queue_name.data
            var.queue_number = form.queue_number.data
            var.number_of_people = form.number_of_people.data
            var.waiting_time = form.waiting_time.data

            db.sqlalchemy_session.commit ()

            return redirect (url_for ('all_Queue'))


@app.route('/Dashboard')
def dashboard():
    query1 = (
        db.sqlalchemy_session.query(
            source.ormmodel.ormQueue.number_of_people,
            source.ormmodel.ormQueue.queue_name
        ).group_by(source.ormmodel.ormQueue.queue_name)
    ).all()

    query = (
        db.sqlalchemy_session.query(
            func.count(source.ormmodel.ormClient.client_fullname),
            source.ormmodel.ormClient.place_name
        ).group_by(source.ormmodel.ormClient.place_name)
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
    print(place_name, count)
    print(queue_name, number_of_people)

    data = {
        "bar": [bar],
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('Dashboard.html', graphsJSON=graphsJSON)



if __name__ == '__main__':
    app.run()
