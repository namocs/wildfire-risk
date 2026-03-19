# Wildfire Prediction Model

This program collects data concurrently every 15 minutes due to Open-Meteo's API since the latest weather comes every 15 minutes. There are three different types of data,

> publicWeather -> This gets the weather from API and stores it in publicData.csv

> simulatedData -> This randomly simulates data and stores it in simulatedData.csv

> sensorData -> This gets data from  sensors and API and stores it in sensorData.csv


We also run the csv dataset's into my risk prediction model and then store the results in the json file,


> each_row -> Gets  risk of wildfire occurring in per row for 1 or 2 datasets combined 

> every_thirty-> Gets  risk of wildfire occurring every 2 rows same as "each_row"

> sim_thirty -> Gets risk of wildfire every 30 mins for the simulated dataset.






# Getting Started

 Its is recommend to create a python virtual environment by doing
```sh
python3 -m venv venv
```
Inside the folder active the virtual environment

For **Windows** do this in powershell :
```sh
.\venv\Scripts\Activate.ps1
```
Or in the command line:
```sh
.\venv\Scripts\activate.bat
```

For **Mac OS** and **Linux** users run this in the terminal :
```sh
source venv/bin/activate
```

Once activated you have to install the required packages:
```sh
pip3 install -r requirments.txt
```

Then you can run the main python fileto run the model
```sh
python3 main.py
```

**Make sure to change .env.example  to .env and enter the correct info about your flask server!!!!!**

## Running the Feedback System

You have to go into the server folder and do the following to run the python flask server
```sh
python3 server.py
```

***Look at the IP address and the Port of your flask server and enter this into your .env***


