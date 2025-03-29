# Ucla Gym Occupancy

An extension of my Bruin Active CS35L project that now attempts to dynamically collect occupancy data on an hour to hour basis and display this in real-time.

## Current Features
* Can view hourly occupancy rates for both Wooden and BFit in the current day. For hours that haven't occurred yet in the day, it will contain occupancy rates from the previous day.
* Can view historically the average occupancy rates across the hours of each weekday for both Wooden and BFit. 

## To Use Locally
From the directory of app.py
```shell
pip install flask flask-cors pymongo python-dotenv
python app.py
```

## Future Goals
Optimize the frontend for mobile use. 
Afterwards deploy it into AWS to run the backend on an hour-by-hour basis automatically.
