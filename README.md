# Curing-Chamber
Build an automated system to monitor and control the temperature and relative humidity of a curing chamber.  Main file runs as a cron job every 10 minutes.

![Curing Chamber](http://i.imgur.com/PM0CppD.jpg)

# Usage
The main Python file curingControl.py should run as a cron job every 10 minutes.  

This reads the current temperature and relative humidity inside your curing chamber from the AM2302 sensor.  You can set ranges for your optimal temperature and humidity within the fridge.  The program will then adjust the power to your fridge and humidifier when it gets outside of these ranges (via the WeMo Insight switches).

All data is logged to a MySQL database, as well as a "last run" CURINGLOG file that you can check for last actions.  Optionally you can also use the Raspberry Pi camera to take a picture inside the fridge for display on a webpage.

# Getting Started
* Install and configure all the software in the Software section below.
* Name your WeMo switches "humidifier" and "temperature" (or you can edit the names in main()).
* I put my [/raspi-rht/th_2](https://github.com/FiZiX/raspi-rht) in /home/pi.  If you want something else, edit the location in main().
* You can turn on/off the writeDB() and takePicture() functions within main().
* Edit the connection options (hostname, username, password) in the writeDB() function.
* Create a crontab entry for the curingControl.py file. I have mine run every 10 minutes:

`*/10 * * * * /home/pi/curingControl.py`

# Hardware Requirements
* Wine fridge.
* Raspberry Pi 2 B.
* WeMo Insight Switch x 2.
* Humidifier (ultrasonic) - - important that your humidifier will immediately turn on once power is restored (stays "on").  If it has a digital on/off switch that needs to be pushed after being plugged in, it is no good for our purposes.
* AM2302 (wired DHT22) temperature-humidity sensor - From [https://www.adafruit.com/products/393](https://www.adafruit.com/products/393).
* Standalone temperature and humidity sensor (optional).
* Home WiFi network.

![Raspberry Pi](http://imgur.com/HuszHjj.jpg)

# Software
* Raspbian.
* Python.
* Ouimeaux (Python API for Belkin WeMo devices).
* MySQL
* Apache
* RASPI-RHT.
* MySQL connector.

![Temperature and humidity sensor.](http://imgur.com/CggsLWZ.jpg)

# MySQL Schema
	mysql> describe chamberlog;
	+----------------+--------------+------+-----+---------+----------------+
	| Field          | Type         | Null | Key | Default | Extra          |
	+----------------+--------------+------+-----+---------+----------------+
	| entry_id       | int(11)      | NO   | PRI | NULL    | auto_increment |
	| date           | datetime     | YES  |     | NULL    |                |
	| temp           | decimal(4,2) | YES  |     | NULL    |                |
	| humidity       | decimal(4,2) | YES  |     | NULL    |                |
	| tempaction     | varchar(20)  | YES  |     | NULL    |                |
	| humidityaction | varchar(20)  | YES  |     | NULL    |                |
	+----------------+--------------+------+-----+---------+----------------+
	6 rows in set (0.01 sec)


![WeMo Insight Switch](http://i.imgur.com/k4dbe1n.png)

# To Do
* Send SMS alerts for various events (out of water, can't connect to WeMo devices).
* Create graphs with HTML5 based on MySQL data.

# References
* [https://github.com/FiZiX/raspi-rht](https://github.com/FiZiX/raspi-rht) - I basically forked my project from this (before I setup git).  Amazing project and ideas.
* [https://hackaday.io/project/3766/instructions](https://hackaday.io/project/3766/instructions) - Helped a lot with the wiring of the sensor.
* [http://ouimeaux.readthedocs.org/en/latest/readme.html](http://ouimeaux.readthedocs.org/en/latest/readme.html)
* [http://iada.nl/en/blog/article/temperature-monitoring-raspberry-pi](http://iada.nl/en/blog/article/temperature-monitoring-raspberry-pi)
