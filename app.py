import numpy as np
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float



# Establish connection with the database


#Reflect Database into ORM classes
Base = declarative_base()

#Save references to each table
#Measurement = Base.classes.measurement
#Station = Base.classes.station
#session = Session(bind=engine)

class Measurement(Base):
    __tablename__ = 'Measurement'
    station = Column(String, primary_key=True)
    date = Column(String(255))
    prcp = Column(Float(255))
    tobs = Column(Integer)

class Stations(Base):
    __tablename__ = 'Station'
    stations = Column(String, primary_key=True)
    name = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    elevation = Column(Float(255))

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
session = Session(engine)
Base.metadata.create_all(engine)

app = Flask(__name__)

# Establish routes
@app.route("/")
def home_page():
	return(
		f"Home Page</br>"
		f"/api/v1.0/precipitation</br>"
		f"/api/v1.0/stations</br>"
		f"/api/v1.0/tobs</br>"
		f"/api/v1.0/<start></br>"
		f"/api/v1.0/<start>/<end></br>"
    )

@app.route("/api/v1.0/precipitation") # date & prcp
def precipitation():
    prcp_list = []
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_returns = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

    for prcp in prcp_returns:
        date, temperature = prcp
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["temperature"] = temperature
        prcp_list.append(prcp_dict)
        
    return jsonify(prcp_list)




    #precip = {date: prcp for date, prcp in precipitation}

    
    #return jsonify(prcp_returns)


	# Convert it into dictionary values


@app.route("/api/v1.0/stations") # stations
def stations():
    stations = session.query(Measurement.station).all()
    #stations_list = {}
    #for station in stations:
    #    stations_list.append(station)
    # station_dict_list = []
    # for station in stations:
    #     station_id = station[0]
    #     station_dict_list.append(station_id)

    stations_list = list(np.ravel(stations))

    return jsonify(stations_list)




@app.route("/api/v1.0/tobs") # tobs
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_year).all()

    tobs_maped = []
    # parsing means processing
    for temperature_observation in tobs:
        date, temperature = temperature_observation
        
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = temperature
        tobs_maped.append(temp_dict)


    #date, temperature = tobs
    #tobs = {}

    #tobs["date"] = date
    #tobs["temperate observation"] = temperature

    #for date, tobs in tobs:
    #    obs_dict.setdefault(date, []).append(tobs)

    return jsonify(tobs_maped)



 # End & Beginning
@app.route("/api/v1.0/<startDate>/<endDate>")
def date(startDate=None, endDate=None):
    # minimum temperature, 
    # average temperature,
    # max temperature 

    if not endDate:
        print("dont have end date1")
        start_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startDate).all()
        

        print("dont have end date 2")
        start_sort = list(np.ravel(start_date))
        return jsonify(start_sort)
    
    else:
        print("startDate")
        print(startDate) 
        print("endDate")
        print(endDate)
        temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date <= endDate).all()
        temperature_stats_list = list(np.ravel(temperature_stats))


        min_temp, avg_temp, max_temp = temperature_stats_list

        stats = {}

        stats["min_temp"] = min_temp
        stats["avg_temp"] = avg_temp
        stats["max_temp"] = max_temp

        print(stats)

        return jsonify(stats)





if __name__ == "__main__":
    app.run(debug=True)


