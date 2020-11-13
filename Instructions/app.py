import numpy as np
import datetime as dt

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
# reflect the tables
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

#Home page route

@app.route("/")
def homepage():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#Precipitation route

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date 1 year ago from the last data point in the database
    #Last Date
    descendingdate=session.query(Measurement).order_by(Measurement.date.desc()).first()
    descendingdate.__dict__
    #1 Year from Last Date
    year_ago=dt.date(2017,8,23)-dt.timedelta(days=365)
    year_ago

    # Query all passengers
    results_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date>=year_ago).\
        order_by(Measurement.date.desc()).all()
   
    session.close()

  # Create a dictionary from the row data and append to a list of all_passengers
    precip_values = []
    for date, prcp in results_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precip_values.append(prcp_dict)

    return jsonify(precip_values)

#Station route

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    "Return a list of all stations"

    # Query all stations
    station_query = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_query))

    return jsonify(all_stations)



#Temperature route

@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Calculate the date 1 year ago from the last data point in the database
    #Last Date
    descendingdate=session.query(Measurement).order_by(Measurement.date.desc()).first()
    descendingdate.__dict__
    
    #1 Year from Last Date
    year_ago=dt.date(2017,8,23)-dt.timedelta(days=365)
    year_ago


    # Query most active station
    most_active = session.query(Measurement.date, Measurement.tobs) .\
                filter(Measurement.station == 'USC00519281').filter(Measurement.date>=year_ago)


    session.close()

  # Create a dictionary from the row data and append to a list of all_passengers
    temperature_list = []
    for date, tobs in most_active:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["temp obs"] = tobs
        temperature_list.append(temperature_dict)

    return jsonify(temperature_list)


#Start route only

@app.route("/api/v1.0/<start>")
def start_only(start):

    #Create our session (link) from Python to the DB
    session = Session(engine)

    #Query start info
    start_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
           filter(Measurement.date >= start)

    session.close()

    start_t_list = []
    for min_temp, max_temp, avg_temp in start_query:
        dict_s = {}
        dict_s["Min"] = min_temp
        dict_s["Max"]= max_temp
        dict_s["Avg"]= avg_temp
        start_t_list.append(dict_s)


    return jsonify(start_t_list)



#Start and end route

# @app.route("/api/v1.0/<start>/<end>")
# def startend(startandend):

 #Create our session (link) from Python to the DB
    #session = Session(engine)






if __name__ == '__main__':
    app.run(debug=True)





# @app.route("/")
# def welcome():
#     """List all available api routes."""
#     return (
#         f"Available Routes:<br/>"
#         f"/api/v1.0/names<br/>"
#         f"/api/v1.0/passengers"
#     )


# @app.route("/api/v1.0/names")
# def names():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(Passenger.name).all()

#     session.close()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))

#     return jsonify(all_names)


# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


# if __name__ == '__main__':
#     app.run(debug=True)
