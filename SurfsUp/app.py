# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine,func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from datetime import datetime,timedelta

#################################################
# Database Setup
#################################################

engine= create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base= automap_base ()

Base.prepare(engine, reflect=True)
Station=Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Define a route for the home page
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

# Define a route for the precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the last 12 months of precipitation data and return as JSON
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

# Define a route for the list of stations
@app.route("/api/v1.0/stations")
def stations():
    # Query list of stations and return as JSON
    results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

# Define a route for the temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    # Query the last 12 months of temperature data for the most active station and return as JSON
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date >= one_year_ago).all()
    temperature_data = [temperature[0] for temperature in results]
    return jsonify(temperature_data)

# Define a route for the start date
@app.route("/api/v1.0/<start_date>")
def temperature_by_start(start_date):
    # Query the minimum, average, and maximum temperatures for dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    temperature_data = list(results[0])
    return jsonify(temperature_data)

# Define a route for the start and end date
@app.route("/api/v1.0/<start_date>/<end_date>")
def temperature_by_start_end(start_date, end_date):
    # Query the minimum, average, and maximum temperatures for dates between the start and end dates
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    temperature_data = list(results[0])
    return jsonify(temperature_data)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)