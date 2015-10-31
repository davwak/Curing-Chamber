#!/usr/bin/python

import ouimeaux
import time
import picamera
import logging
import datetime as dt
import mysql.connector

from time import sleep
from fractions import Fraction
from ouimeaux.environment import Environment
from subprocess import Popen, PIPE
from os.path import expanduser
from mysql.connector import errorcode

def main ():
    # head vampire function
    logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', 
            datefmt='%m/%d/%Y %I:%M:%S %p', 
            level=logging.INFO,
            filename='CURINGLOG',
            filemode='w')
    logging.info("Starting new capture.")

    env = startWeMoEnvironment()
    
    # WeMo switch names
    humidity = 'humidifier'
    temperature = 'temperature'

    # Connect to both WeMo Insight Switches
    discoverWeMoDevices(env)
    switchTemperature = connectToWeMo(env, temperature)
    switchHumidity = connectToWeMo(env, humidity)

    # Get the temp and humidity.
    home = expanduser("~")
    p = Popen(["sudo", home+"/raspi-rht/th_2"], stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()

    if err != '':
        logging.critical("th_2 returned error "+str(err))
        raise SystemExit(1)

    currentTemp, currentRH = output.split()

    # The temp gets changed to Celcius.
    currentTemp = (float(currentTemp) - 32) * 5 / 9
    currentRH = float(currentRH)

    # Control Temp & Humidity - actions (on|off|no action)
    tempAction = controlTemp(env, switchTemperature, currentTemp)
    humidityAction = controlHumidity(env, switchHumidity, currentRH)
    
    # Write logs & take picture
    writeDB(currentTemp, currentRH, tempAction, humidityAction)
    #takePicture(currentTemp, currentRH)

    logging.info("Capture complete.")
    return;

def startWeMoEnvironment():
    
    env = Environment()
    env.start()

    return env;

def discoverWeMoDevices(env):
    # find both WeMo Insight switches
    
    env.discover(seconds=3)
    
    return; 

def connectToWeMo(env, switchName):
    
    return env.get_switch(switchName)


def controlTemp (env, switch, currentTemp):
    # turns the fridge on or off via WeMo
    state = switch.basicevent.GetBinaryState()['BinaryState']
    logging.info("Fridge switch state: %s", state)
    tempAction = "";

    if currentTemp < 13:
        if state == '0':
            # do nothing, fridge is off
            logging.info("Fridge is already off.")
            tempAction = "no action"
        else:
            switch.basicevent.SetBinaryState(BinaryState=0)
            logging.info("Fridge was turned off.")
            tempAction = "off"
    elif currentTemp > 16:
        if state == '1':
            # do nothing, fridge is on
            logging.info("Fridge is already on.")
            tempAction = "no action"
        elif state == '8':
            # this shouldn't happen - log it
            logging.info("Fridge isn't plugged in?")
            tempAction = "no action"
        elif state == '0':
            switch.basicevent.SetBinaryState(BinaryState=1)
            logging.info("Fridge was turned on.")
            tempAction = "on"
    else:
        # everything is good - let's turn it off if on (TESTING)
        logging.info("Fridge is within optimal range - %s.", currentTemp)
        tempAction = "no action"
        if state == '1':
            #fridge is still on, but we're in optimal range, turn it off
            switch.basicevent.SetBinaryState(BinaryState=0)
            logging.info("Fridge is on, turning off.")
            tempAction = "off"
    return tempAction;


def controlHumidity (env, switch, currentHumidity):
    # turns the humidifier on or off via WeMo
    # Binary state 1 = on, 8 = on but not running, 0 = off

    # check if out of water
    state = switch.basicevent.GetBinaryState()['BinaryState']
    logging.info("Humidity switch state: %s", state)
    humidityAction = ""

    if currentHumidity < 62:
        # needs to turn on
        if state == '8':
            # humidifier is on, but out of water.
            logging.info("Humidifier is out of water.")
            humidityAction = "no action"
        elif state == '1':
            # do nothing
            # humidifier is already on
            logging.info("Humidifier is already on.")
            humidityAction = "no action"
        elif state == '0':
            switch.basicevent.SetBinaryState(BinaryState=1)
            logging.info("Humidifier was turned on.")
            humidityAction = "on"
    elif currentHumidity > 66:
        # needs to turn off
        if state == '0':
            # do nothing
            logging.info("Humidifer is already off.")
            humidityAction = "no action"
        else:
            switch.basicevent.SetBinaryState(BinaryState=0)
            logging.info("Humidifier was turned off.")
            humidityAction = "off"
    else:
        logging.info("Humidifier is within optimal range - %s.", currentHumidity)
        if state == '1':
            # humidifier is still on, but we're in optimal range, turn it off
            switch.basicevent.SetBinaryState(BinaryState=0)
            logging.info("Humidifier is on, turning off.")
            humidityAction = "off"
    return humidityAction;
    
def writeDB (temp, humidity, tempAction, humidityAction):
    # write data to MySQL DB - chamberlog database
    # switchname, temp, humdity, time, action

    currentDateTime = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # connect to our datbase
    db = mysql.connector.connect(host='HOSTNAME',user='USERNAME',passwd='PASSWORD',db='curing')

    cursor = db.cursor()
    
    add_log = ("INSERT INTO chamberlog "
            "(date, temp, humidity, tempaction, humidityaction) "
            "VALUES (%s, %s, %s, %s, %s)" )
    
    data = (currentDateTime, temp, humidity, tempAction, humidityAction)

    cursor.execute(add_log, data)
    
    db.commit()
    
    cursor.close()
    db.close()

    return;


def takePicture (temp, humidity):
    # take a picture of the curing chamber - check for bad mold.
    logging.info("Taking a picture.")

    camera = picamera.PiCamera()
    camera.resolution = (2592, 1944)
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = "Temp:%sc RelHum:%s - %s" % (temp, humidity, dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # LOW LIGHT SETTINGS
    #camera.framerate = Fraction(1, 6)
    #camera.shutter_speed = 6000000
    #camera.exposure_mode = 'off'
    #camera.iso = 800

    # give the camera time to measure AWD
    sleep(3)

    camera.hflip = True
    camera.vflip = True
    camera.capture('fridge.jpg')
    
    return;

main()
