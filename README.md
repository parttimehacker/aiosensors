# aiosensors
Environment sensors updating feeds on adafruit.io MQTT server.
## Description: 
This **Raspberry Pi** based application collects data from several sensors and publishes the data to Adafruit's IO platform. Data feeds are used to publish and subscribe to relevant topics. Dashboards are used to display content. 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django)

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Architecture](#architecture)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->
## General Information
- *Provide general information about your project here.*
  - This is one of several Python applications used in my home automation system (**DIYHA**). I've used OOP, MVC, and MTV concepts in my DIYHA system.
- *What problem does it (intend to) solve?*
  - Two I2C based sensors collect environment data and publish several parameters.
- *What is the purpose of your project?*
  - My home automation system contains environment sensors, motion sensors, LED clocks, light switches, emergency sirens, a django web server, interfaces to Adafruit.io and a mosquitto MQTT broker.
- *Why did you undertake it?*
  - This was a fun project to learn about python, Raspberry Pi, Arduino processors, hardware and more.
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->
## Technologies Used
- python=3.7.3
- Adafruit-Blinka=7.1.0
- digitalio
- adafruit-circuitpython-rgb-display
- python3-pil
- adafruit-io

## Features
List the ready features here:
- Displays status and diagnostic information for the host raspberry pi server on an LCD display.
- Code passes pylint with a score of 10.0
## Screenshots
Not applicable.
<!-- ![Example screenshot](./diyhadiagram.png)-->
<!-- If you have screenshots you'd like to share, include them here. -->
## Architecture
This is a application that collects data about the host and potenitally presents information on some type of I2C or SPI bus display device. It posts topic data to an MQTT broker and to a web server. 
<!-- 
![Example screenshot](./diyhadiagram.png)
<!-- If you have screenshots you'd like to share, include them here. -->
## Setup
Clone the repository, followed by installation of the dependencies. The last step is to decide on automation.
### Clone the repository 
```
git clone https://github.com/parttimehacker/aiosensors.git
cd aiosensors
```
### Install dependencies
Note: The Raspberry Pi operating team made a change on pip installations prior to version 12 of Raspian.
- Prior to Raspian 12
```
sudo pip install psutil
sudo pip install Adafruit-Blinka 
sudo pip install adafruit-circuitpython-rgb-display
sudo pip3 install adafruit-circuitpython-bme680 
sudo pip3 install adafruit-circuitpython-veml7700 
```
- Raspian 12 and later
```
sudo pip install psutil --break-system-packages
sudo pip install Adafruit-Blinka --break-system-packages
sudo pip install adafruit-circuitpython-rgb-display --break-system-packages
sudo pip3 install adafruit-circuitpython-bme680 --break-system-packages
sudo pip3 install adafruit-circuitpython-veml7700 --break-system-packages
```
<!--
<div align="left">
    <img src="assettree.png" width="200px"</img> 
</div>
-->
## Usage
You need to decide whether you want to manually run the application or have it started as part of the boot process. I recommend making a **Raspbian OS systemd service**, so the application starts when rebooted or controled by **systemctl** commands. The **systemd_script.sh** creates a admin directory in **/usr/local directory**. The application files are then copied to this new directory. The application will also require a log file in **/var/log directory** named asset.log.
### Manual or Command Prompt
To manually run the application enter the following command (sudo may be required on your system)
```
sudo python3 aiosensors.py --g GROUOP --d DISPLAY --w
```
- GROUP : Data feeds use this arguement to identify feed membership and naming conventions are used to identify its location.
- DISPLAY : An optional display type determines version support for ssd1306 and st7789 devices. NA is the default.
- w : Boolean to indicate access to the Apple weather API based on location.
### Raspbian systemd Service
First edit the **asset systemd service** and replace the MQTT broker, room values and django web server with their host names or IP addresse. A systemd install script will move files and enable the applicaiton via **systemctl** commands.
- Run the script and provide the application name **asset** to setup systemd (the script uses a file name argument to create the service). 
```
vi aiosensors.service
./systemd_script.sh aiosensors
```
This script also adds four aliases to the **.bash_aliases** in your home directory for convenience.
```
sudo systemctl start aiosensors
sudo systemctl stop aiosensors
sudo systemctl restart aiosensors
sudo systemctl -l status aiosensors
```
- You will need to login or reload the **.bashrc** script to enable the alias entries. For example:
```
cd
source .bashrc
```
### MQTT Topics and Messages
The application subscribes to two MQTT topics and publishes six status messages. Three are are sent at initialization and then handled by a **diy/system/who** message. Three other messages are sent every 15 minutes after calculating an average. The first three are:
```
self.host = socket.gethostname()
self.os_version_topic = "diy/" + self.host + "/os"
self.pi_version_topic = "diy/" + self.host + "/pi"
self.ip_address_topic = "diy/" + self.host + "/ip"
```
The timed messages are:
```
self.host = socket.gethostname()
self.cpu_topic = "diy/" + self.host + "/cpu"
self.celsius_topic = "diy/" + self.host + "/cpucelsius"
self.disk_topic = "diy/" + self.host + "/disk"
```
- The **diy/system/who** sends local server information to the MQTT Broker. 
## Implementation Status
![Status](https://progress-bar.dev/80/?title=progress)
## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Further refactoring to more generalize the class

To do:
- Integrate into other DIYHA applications and repositories
- Develop a new installation process for seperate repositories
## Acknowledgements
Give credit here.
- My "do it yourself home automation" system leverages the work from the Eclipse IOT Paho project. https://www.eclipse.org/paho/
- Many thanks to...
- Adafruit supplies most of my hardware. http://www.adafruit.com
- I use the PyCharm development environment https://www.jetbrains.com/pycharm/
## Contact
Created by [@parttimehacker](http://parttimehacker.io/) - feel free to contact me!
### Repository Stats
![Your Repository’s Stats](https://github-readme-stats.vercel.app/api?username=parttimehacker&show_icons=true)
### Repository Languages
![Your Repository's Stats](https://github-readme-stats.vercel.app/api/top-langs/?username=parttimehacker&theme=blue-green)
### HITS
![Hits](https://hitcounter.pythonanywhere.com/count/tag.svg?url=https://github.com/parttimehacker)
<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
