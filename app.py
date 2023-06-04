# Import the dependencies.
from datetime import datetime, timedelta
import datetime as dt
from matplotlib import style
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np
import pandas as pd


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return """Welcome! 
    For Precipitation Data, please route to /api/v1.0/precipitation. For Stations Data, 
    please route to /api/v1.0/stations. For Tobs Data, please route to /api/v1.0/tobs"""

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a new session for this route function
    session = Session(engine)
    
    # Adding code from notebook
    latest_date_row = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = latest_date_row[0]

    # Calculate the date one year from the last date in data set.
    latest_date = datetime.strptime(latest_date, '%Y-%m-%d')
    one_year_ago = latest_date - timedelta(days=365)
    
    # Perform a query to retrieve the date and prcp columns
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    # Create a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in results}

    # Close the session
    session.close()

    # Return the JSON response
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create a new session for this route function
    session = Session(engine)
    
    # Query the station names from the database
    results = session.query(Station.station).all()

    # Convert the station names to a list
    station_list = [station[0] for station in results]

    # Close the session
    session.close()

    # Return the JSON response
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a new session for this route function
    session = Session(engine)
    
    station_id = 'USC00519281'

    # Design a query to calculate the lowest, highest, and average temperature for the specified station
    temperature_query = session.query(func.min(Measurement.tobs).label('lowest_temp'),
                                      func.max(Measurement.tobs).label('highest_temp'),
                                      func.avg(Measurement.tobs).label('avg_temp')).filter(Measurement.station == station_id)

    # Execute the query and fetch the result
    temp_result = temperature_query.one()

    # Extract the temperature values
    lowest_temp = temp_result.lowest_temp
    highest_temp = temp_result.highest_temp
    avg_temp = temp_result.avg_temp

    # Create a dictionary with the temperature values
    temperature_dict = {
        'lowest_temp': lowest_temp,
        'highest_temp': highest_temp,
        'avg_temp': avg_temp
    }

    # Close the session
    session.close()

    # Return the JSON response
    return jsonify(temperature_dict)

@app.route("/api/v1.0/<start>")
def temperature_start(start):
    # Convert the start date string to a datetime object
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")

    temperature_query = session.query(func.min(Measurement.tobs).label('lowest_temp'),
                                            func.max(Measurement.tobs).label('highest_temp'),
                                            func.avg(Measurement.tobs).label('avg_temp')).filter(Measurement.date >= start_date)

    # Execute the query and fetch the result
    temp_result = temperature_query.one()

    # Extract the temperature values
    lowest_temp = temp_result.lowest_temp
    highest_temp = temp_result.highest_temp
    avg_temp = temp_result.avg_temp

    # Create a dictionary with the temperature values
    temperature_dict = {
        'start_date': start_date.strftime("%Y-%m-%d"),
        'TMIN': lowest_temp,
        'TMAX': highest_temp,
        'TAVG': avg_temp
    }

    # Close the session
    session.close()

    # Return the JSON response
    return jsonify(temperature_dict)

@app.route("/api/v1.0/<start>/<end>")
def temperature_startandend(start, end):
    # Convert the start and end date strings to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    temperature_query = session.query(func.min(Measurement.tobs).label('lowest_temp'),
                                      func.max(Measurement.tobs).label('highest_temp'),
                                      func.avg(Measurement.tobs).label('avg_temp')).filter(
        Measurement.date >= start_date, Measurement.date <= end_date)

    # Execute the query and fetch the result
    temp_result = temperature_query.one()

    # Extract the temperature values
    lowest_temp = temp_result.lowest_temp
    highest_temp = temp_result.highest_temp
    avg_temp = temp_result.avg_temp

    # Create a dictionary with the temperature values
    temperature_dict = {
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
        'TMIN': lowest_temp,
        'TMAX': highest_temp,
        'TAVG': avg_temp
    }

        # Close the session
    session.close()

    # Return the JSON response
    return jsonify(temperature_dict)

if __name__ == '__main__':
    app.run(debug=True)