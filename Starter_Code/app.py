# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from flask import Flask

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
    print('For Precipitation Data, please route to /precipitation')
    print('For Stations Data, please route to /stations')
    print('For Tobs Data, please route to /tobs')
    return """Welcome! 
    For Precipitation Data, please route to /precipitation. For Stations Data, 
    please route to /stations. For Tobs Data, please route to /tobs"""

@app.route("/precipitation")
def home():
    print("Server received request for 'Home' page...")
    return "Hello! If you would like to "

if __name__ == '__main__':
    app.run(debug=True)