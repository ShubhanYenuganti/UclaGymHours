# Ucla Gym Occupancy

An extension of my Bruin Active CS35L project that now attempts to dynamically collect occupancy data on an hour to hour basis and display this in real-time.

## To Use Backend
From the directory of app.py
```shell
pip install flask flask-cors pymongo python-dotenv
python app.py
```
It should display the latest entry of occupancy data displayed in the mongodb cluster in json.

## Future Goals
Implement a frontend and then test the app locally by running the script that logs occupancy data into mongodb manually per hour.
Afterwards deploy it into AWS to run the backend and hour-by-hour basis automatically.
