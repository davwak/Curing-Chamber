# Curing-Chamber
Build an automated system to monitor and control the temperature and relative humidity of a curing chamber.  Main file runs as a cron job every 10 minutes.

![Curing Chamber](http://i.imgur.com/PM0CppD.jpg)

# Usage
The main Python file curingControl.py should run as a cron job every 10 minutes.  It reads the current temperature and relative humidity inside your curing chamber.  Depending on the results, it will adjust power to the fridge and the humidifier, via the WeMo Insight switches, to keep both the temperature and humidity within your range.  It can also detect when your humidifier is out of water.  Optionally you can log all this data to a database, and also use the Raspberry Pi camera to take a picture inside the chamber.

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
