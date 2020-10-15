import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def Home_Page():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
    )

@app.route('/api/v1.0/precipitation')
def prcp():
    
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    # close the session to end communication with the server
    session.close()
    #prcp_dict = {'date': 'prcp'}
    #for row in results:
    #    prcp_dict['date'] = row.date
    #    prcp_dict['prcp'] = row.prcp

    #return jsonify(prcp_dict)
    prcp_list = []
    for date in results:
        prcp_dict = {}
        prcp_dict['date'] = date.date
        prcp_dict['prcp'] = date.prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route('/api/v1.0/stations')
def stat():

    ############### Database Block ###################
    # Start session
    session = Session(engine)

    # Query the database
    results_station = session.query(Station.station, Station.name).all()

    # close session
    session.close()
    ###################################################

    return jsonify(results_station)

if __name__ == '__main__':
    app.run(debug=True)