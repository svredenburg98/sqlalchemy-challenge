import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"-------------------<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/START_DATE<br/>"
        f"/api/v1.0/START_DATE/ENDDATE"
    )

@app.route('/api/v1.0/precipitation')
def prcp():
    ############### Database Block ###################
    # Start session
    session = Session(engine)

    # Query the database
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    # close the session to end communication with the server
    session.close()
    ###################################################

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


@app.route('/api/v1.0/tobs')
def temp():

    ############### Database Block ###################
    # Start session
    session = Session(engine)

    # Query the database
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()


    # close session
    session.close()
    ###################################################

    return jsonify(tobs_results)

@app.route('/api/v1.0/<start_date>')
def start(start_date):
    ############### Database Block ###################
    # Start session
    session = Session(engine)

    # Query the database
    #highest temp
    high = session.query(Measurement.tobs).filter(Measurement.date >= start_date).order_by(Measurement.tobs.desc()).first()
    #lowest temp
    low = session.query(Measurement.tobs).filter(Measurement.date >= start_date).order_by(Measurement.tobs).first()
    #avg temp
    avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    # close session
    session.close()
    ###################################################
    infolist = [{"TMIN": low}, {"TAVG": avg}, {"TMAX": high}]
    return jsonify(infolist)
    
@app.route('/api/v1.0/<start_date>/<end_date>')
def startend(start_date, end_date):
    ############### Database Block ###################
    # Start session
    session = Session(engine)

    # Query the database
    #highest temp
    high_end = session.query(Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).order_by(Measurement.tobs.desc()).first()
    #lowest temp
    low_end = session.query(Measurement.tobs).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).order_by(Measurement.tobs).first()
    #avg temp
    avg_end = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    # close session
    session.close()
    ###################################################
    infolist_end = [{"TMIN": low_end}, {"TAVG": avg_end}, {"TMAX": high_end}]
    return jsonify(infolist_end)
if __name__ == '__main__':
    app.run(debug=True)