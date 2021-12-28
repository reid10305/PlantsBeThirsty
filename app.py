''' Created by Daniel Pifer for a home plant watering system.
    Uses Flask to run a front end web application to be able 
    to monitor the machine status, as well as keep track of 
    plant growth over time. Individual plant objects are stored
    in a local .csv file for data backup purposes. 
    
    The backend is run simultaneously to control the watering 
    hardware. Plants are watered every two days. All components
    are controlled via the GPIO pins on a Raspberry Pi 3 Model B.
    On the first startup, the plants are automatically watered after
    2 minutes of runtime, then every 2 days thereafter.
    
    (c) Daniel Pifer 2021 '''

''' ***************************************************************** '''

# import packages
import multiprocessing as mp

import constants
from flask import Flask, request, render_template, session
import csv
import time
import os

# import local classes
import Plant
import Tank 
import Pump

# initialize the flask application
app = Flask(__name__)

# intialize pump object
PUMP = Pump.Pump(False, 480)

# initialize tank object
TANK = Tank.Tank(5, 100)

SAVE_FILE = "plants.csv"

Plants = []


@app.route("/addplant", methods=["POST"])
def addPlant(): 
    ''' adds a plant to the chain'''

    # get the information from the form
    species = request.form.get("species")
    nickname = request.form.get("nickname")
    size = request.form.get("size")

    # create new plant object
    newPlant = Plant.Plant(species, nickname, size)

    # add new plant to list
    if not Plants.append(newPlant):
        print("New plant added!")

        # add to backup .csv file
        with open(SAVE_FILE, 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([newPlant.species, newPlant.nickname, newPlant.size])

            csvfile.close()

        return render_template("myplants.html", Plants = Plants)

    # if anything goes wrong 
    else:
        print("Error, new plant not added to chain.")
        return render_template("error.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/todo")
def todo():
    return render_template("todo.html")

@app.route("/myplants")
def myplants():
    return render_template("myplants.html", Plants = Plants)

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/help")
def readme():
    return render_template("help.html")

@app.route("/status")
def status():
    # get tank status from the status file    
    currStatus = getStatusFromFile("status.csv")

    config = importDictFromTxtFile("config.txt")
        
    return render_template("status.html", currentPerc = currStatus[0], config = config)

def frontend():
    ''' main method for the front end '''
    
    app.secret_key = 'BAD_SECRET_KEY'

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def importDictFromTxtFile(file):
    ''' returns dictionary imported from passed file '''
    dictionary = {}
    with open (file, "r") as txtfile:
        for row in txtfile:
            (key, value) = row.split('=')
            dictionary[key] = value
        txtfile.close()

    print(dictionary)
    return dictionary

def getStatusFromFile(file):
    ''' gets status from status file '''

    with open ("status.csv", newline= '\n') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            currentPerc = row[0]
            empty = row[1]
        csvfile.close()

    return (currentPerc, empty)

''' ***************************************************************** '''

def water(TANK, PUMP, waterTime):
    ''' commence watering of the system '''

    # test if the tank is empty
    if (not (TANK.empty_light)) and ((waterTime / constants.HOUR) * PUMP.pump_rate < TANK.currentVol):
        # water if the tank is not empty
        PUMP.pump_flag = True
        print("Watering...")

        time.sleep(waterTime)

        # subtract ammount used from the tank
        TANK.subtractVol((waterTime / constants.HOUR) * PUMP.pump_rate)

        # turn pump off
        PUMP.pump_flag = False
        print("Done watering.")
        print("New tank volume: ")
        print(str(TANK.currentPerc) + " %")
        print(str(TANK.currentVol) + " G")

        # write to save file 
        TANK.saveToFile()
        return 

    else:
        print("Please refill tank")

        return

def refillTank(TANK):
    ''' refills tank when refill button is pressed '''
    
    TANK.reset()
    
    # write new status to save file
    TANK.saveToFile()
    # put perc onto mp queue

    return

def backend():
    ''' main method for the back end '''

    # initialize the main plant chain from the backup save file
    with open (SAVE_FILE, newline= '\n') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            newplant = Plant.Plant(row[0], row[1], row[2])
            Plants.append(newplant)
        
        csvfile.close

    FRONT = mp.Process(target=frontend)

    FRONT.start()

    # set the initial water time to 1 minute after startup
    nextWater = 1 * constants.MINUTE

    while True:
        
        # wait until next water time
        time.sleep(nextWater)

        water(TANK, PUMP, 30)

        nextWater = 2 * constants.DAY

''' **************************************************************** '''

if __name__ == '__main__':
    ''' run on startup '''

    backend()