import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
import calendar
from datetime import datetime


app = Flask(__name__, static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    client = db.Column(String(50))
    priority = db.Column(Integer)
    target_date = db.Column(DateTime)
    product_area = db.Column(String(50)) 
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)  
    
    def __repr__(self):
        return '<Title %r>' % self.title



class ResponseJSON(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000 +
                    obj.microsecond / 1000
                )
                return millis
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)



def check_if_priority_already_exist(priority, client):
    '''
    Check if the given combination record exists in the table.

        @return interger
    '''
    
    return Feature.query.filter_by(priority=priority, client=client).count()


def get_existing_priority_record(priority, client):
    '''
    Pick the record with given priority and client name.


        return <Feature>

    '''
    return Feature.query.filter_by({'priority':priority, 'client': client }).first()



# endpoint to return the base template
@app.route('/')
def index():
    return render_template('index.html')


# endpoint to insert and retrieve features
@app.route('/api/feature', methods=['GET','POST'])
def feature():

    if request.method == 'POST':


        # check if the given client has priority already existing
        if check_if_priority_already_exist(request.form['priority'], request.form['client']) > 0:

            # fetch entire task for the client
            features = Feature.query.filter_by(client=request.form['client']).\
            filter(Feature.priority >= request.form['priority'])

            # Update all row with less priority
            for feature in features:
                feature.priority = feature.priority + 1
                db.session.commit()



        target_date = datetime.strptime(request.form['target_date'], '%Y-%m-%d')

        feature = Feature(title=request.form['title'],\
         description=request.form['description'], client=request.form['client'],\
         priority=request.form['priority'], target_date=target_date,\
         product_area=request.form['product_area'])

        db.session.add(feature)

        db.session.commit()

        features = Feature.query.filter_by(client=request.form['client']).order_by('priority').all()

        all_features = [{'title':row.title,'id':row.id,'priority':row.priority,\
        'product_area':row.product_area, 'client':row.client, 'description':row.description} for row in features]

        return jsonify(all_features)


    if request.method == 'GET':

        features = Feature.query.all()

        all_features = [{'title':row.title,'id':row.id,'priority':row.priority,\
        'product_area':row.product_area, 'client':row.client, 'description':row.description} for row in features]

        return jsonify(all_features)


# endpoint to fetch one record or update one record
@app.route('/api/feature/priority', methods=['GET', 'POST'])
def set_priority():

    if request.method == 'GET':
        return "GET"
    
    if request.method == 'POST':

        if request.form['mode'] == 'up':


            current_row = Feature.query.get(request.form['id'])

            previous_row = Feature.query.filter_by(client=request.form['client'])\
                            .filter(Feature.priority == current_row.priority - 1).first()

            
            current_row.priority = current_row.priority - 1
            previous_row.priority = previous_row.priority + 1

            db.session.commit()
            
            features = Feature.query.filter_by(client=request.form['client']).order_by('priority').all()
            
            all_features = [{'title':row.title,'id':row.id,'priority':row.priority,\
            'product_area':row.product_area, 'client':row.client, 'description':row.description} for row in features]

            return jsonify(all_features)


        if request.form['mode'] == 'down':


            current_row = Feature.query.get(request.form['id'])

            previous_row = Feature.query.filter_by(client=request.form['client'])\
                            .filter(Feature.priority == current_row.priority + 1).first()

            
            current_row.priority = current_row.priority + 1
            previous_row.priority = previous_row.priority - 1

            db.session.commit()
            
            features = Feature.query.filter_by(client=request.form['client']).order_by('priority').all()
            
            all_features = [{'title':row.title,'id':row.id,'priority':row.priority,\
            'product_area':row.product_area, 'client':row.client, 'description':row.description} for row in features]

            return jsonify(all_features)
            



    



if __name__ == "__main__":  
    app.json_encoder = ResponseJSON 
    db.create_all()
    app.run(debug=True, port=5000)
