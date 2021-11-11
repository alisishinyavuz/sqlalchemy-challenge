from flask import Flask, jsonify
import numpy as np
import datetime as dt
import re
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

###############################
#Data Setup
###############################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect engine into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################
#Falsk Setup
#################################

app = Flask(__name__)


##################################
#Flask Route
##################################


##################################
#Create index route
@app.route("/")
def welcome():
    # """List all available api routes"""
    print("Server requested climate app home page")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"<br/>"
    )
###################################################################
#Create precipitaion route

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server requested climate app precipitation page...")
    #Create session (link) from python to DB
    session = Session(engine)
    # Query for the dates and precipitation values
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    session.close()           

    # Convert to list of dictionaries to jsonify
    prcp_date_list = []

    for date, prcp in prcp_data:
        prcp_dic = {}
        prcp_dic["date"] = date
        prcp_dic["prcp"] = prcp
        prcp_date_list.append(prcp_dic)

    return jsonify(prcp_date_list)
###################################################################
#Create station route
@app.route("/api/v1.0/stations")
def stations():
    print("Server requested climate app stations page...")
    #Create session (link) from python to DB
    session = Session(engine)
    # Query for the dates and precipitation values
    station_data = session.query(Station.name, Station.station).all()
    session.close()

    station_list = []

    for name, station in station_data:
        station_dic = {}
        station_dic["name"] = name
        station_dic[ "station"] = station
        station_list.append(station_dic)

    return jsonify(station_list)    
###################################################################
 #Create temp route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all TOBs"""
    # Query all tobs

    results = session.query(Measurement.date,  Measurement.tobs, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

   

    # Convert the list to Dictionary
    tobs_list = []
    for date,tobs, prcp in results:
        tobs_dic = {}
        tobs_dic["date"] = date
        tobs_dic["tobs"] = tobs
        tobs_dic["prcp"] = prcp
        
        tobs_list.append(tobs_dic)

    return jsonify(tobs_list)


##############################################################################






if __name__ == "__main__":
    app.run(debug=True)


