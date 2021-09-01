
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
##############DATABASE SETUP#####################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect= True)

con = engine.connect
# Save reference to the table
Measurement = Base.classes.measurement
Station= Base.classes.station
session= Session(engine)

##############################################
#Flask Set up
##############################################

app= Flask(__name__)

@app.route("/")
def Welcome():
    print("List all available api routes")
    return(
        "Welcome: <br/>"
        f"Here are the Availeble Routs: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end <br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_twelve_months = '2016-08-23'
    prcp_result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > last_twelve_months ).all()
    rain_totals = []
    for date, prcp in prcp_result:
        row = {}
        row["date"] = date
        row["prcp"] = prcp
        rain_totals.append(row)
    return jsonify(rain_totals)

@app.route("/api/v1.0/stations")
def station():
    stations= session.query(Station.station, Station.name).all()
    all_stations=[]
    for station, name in stations:
        stations_dict={}
        stations_dict["station"]= station
        stations_dict["name"]= name
        all_stations.append(stations_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #active_station = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).\
               #order_by(func.count(Measurement.id).desc()).first()
    stats = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')
    active_stats=[]
    for date,tobs in stats:
        stats_dict={}
        stats_dict["date"]= date
        stats_dict["tobs"] = tobs
        active_stats.append(stats_dict)
    return jsonify(active_stats)

   
    

@app.route("/api/v1.0/<start>")
def startOnly(start):
    start = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    min = func.min(Measurement.tobs)
    avg = func.avg(Measurement.tobs)
    max = func.max(Measurement.tobs)
    day_temp_results = session.query(min, avg, max).filter(Measurement.date >= start).all()
    trips=[]
    for min, avg, max in day_temp_results:
        trips_dict={}
        trips_dict["min"]= min
        trips_dict["avg"]=avg
        trips_dict["max"]=max 
        trips.append(trips_dict)
    return jsonify(trips)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    start = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    end = dt.date(2017, 8, 23)
    min = func.min(Measurement.tobs)
    avg = func.avg(Measurement.tobs)
    max = func.max(Measurement.tobs)
    multi_day_temp_results = session.query(min, avg, max).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    trips=[]
    for min, avg, max in multi_day_temp_results:
        trips_dict={}
        trips_dict["min"]= min
        trips_dict["avg"]=avg
        trips_dict["max"]=max 
        trips.append(trips_dict)
    return jsonify(trips)
    



if __name__ == '__main__':
    app.run(debug=True)