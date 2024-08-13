#!/usr/bin/python3
""" DIYHA aiosensors
    Send environment sensor data to to adafruit.io MQTT broker
"""
# The MIT License (MIT)
#
# Copyright (c) 2024 parttimehacker@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time
import logging.config
import json

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

from pkg_classes.configmodel import ConfigModel
from pkg_classes.statusmodel import StatusModel
from pkg_classes.sensorhal import SensorHAL
from pkg_classes.st7789hal import ST7789HAL

# Set to your Adafruit IO key.
# Key is a secret,
ADAFRUIT_IO_KEY = 'fdcd42503dd94c22ee5b5bb165ce87c13ddc5251'

# Set to your Adafruit IO username.
ADAFRUIT_IO_USERNAME = 'pthacker'

# Start logging and enable imported classes to log appropriately.

LOGGING_FILE = '/usr/local/aiosensors/logging.ini'
logging.config.fileConfig(fname=LOGGING_FILE, disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Application started')

# get the command line args
CONFIG = ConfigModel(LOGGING_FILE)

# get server information
STATUS = StatusModel(LOGGING_FILE)

# initialize sensors
TEMPERATURE_OFFSET = -1.5
SENSORS = SensorHAL(LOGGING_FILE, CONFIG.group, TEMPERATURE_OFFSET )

DISPLAY = ST7789HAL(LOGGING_FILE)

# Define callback functions which will be called when certain events happen.
def connected(client):
    """ Connected function will be called when the client is connected to Adafruit IO.
    This is a good place to subscribe to topic changes.  The client parameter
    passed to this function is the Adafruit IO MQTT client so you can make
    calls against it easily.
    """
    LOGGER.info('Connected to Adafruit.io')
    # Subscribe to changes on a group, `group_name`
    client.subscribe(CONFIG.group+".power")
    if CONFIG.weather_station:
        print("subscribing to weather")
        client.subscribe_weather("2734","current")

def disconnected(client):
    """ Disconnected function will be called when the client disconnects."""
    LOGGER.info('Disconnected from Adafruit.io')
    # Try to reconnect to the Adafruit IO server
    not_connected = True
    while not_connected:
        time.sleep(5)
        try:
            LOGGER.info('Attempting connection to Adafruit.io')
            client.connect()
            client.loop_background()
            not_connected = False
        except BaseException as error:
            LOGGER.info('Exception: MQTT connection failed e={0}'.format(error))
    # sys.exit(1)

def message(client, topic_id, payload):
    # Message function will be called when a subscribed topic has a new value.
    # The topic_id parameter identifies the topic, and the payload parameter has
    # the new value.
    if topic_id == CONFIG.group + "power":
        LOGGER.info('Topic {0} received new value: {1}'.format(topic_id, payload))
    else:
        parseForecast(client, payload)

def parseForecast(client,forecast_data):
    """Parses and prints incoming forecast data
    """
    # incoming data is a utf-8 string, encode it as a json object
    forecast = json.loads(forecast_data)
    # Print out the forecast
    # print("parsing weather")
    # print(forecast_data)
    try:
        fahrenheit = 9.0 / 5.0 * forecast['temperature'] + 32
        client.publish('temperature', fahrenheit, 'outside')
        # print(forecast['conditionCode'])
        client.publish('conditions', forecast['conditionCode'], 'outside')
    except:
        LOGGER.info('Exception: MQTT Weather connection failed')



if __name__ == '__main__':

    # Create an MQTT client instance.
    CLIENT = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    # Setup the callback functions defined above.
    CLIENT.on_connect = connected
    CLIENT.on_disconnect = disconnected
    CLIENT.on_message = message

    # Connect to the Adafruit IO server.
    CLIENT.connect()

    # Now the program needs to use a client loop function to ensure messages are
    # sent and received.  There are a few options for driving the message loop,
    # depending on what your program needs to do.

    # The first option is to run a thread in the background so you can continue
    # doing things in your program.
    CLIENT.loop_background()

    SENSORS.connection(CLIENT)

    CPU_DISPLAY = True

    while True:
        time.sleep(60)
        try:
            SENSORS.collect_and_publish()
            DISPLAY.clear_display()
            if CPU_DISPLAY:
                DISPLAY.display_text(0, STATUS.host_name + ":  " + CONFIG.group , fill="#00FF00")
                DISPLAY.display_text(1, STATUS.ip_address)
                DISPLAY.display_text(2, STATUS.pi_version)
                DISPLAY.display_text(3, STATUS.os_version)
                CPU_DISPLAY = False
            else:
                DISPLAY.display_text(0, "Environment", fill="#00FF00")
                msg = "TEMP:  {:.1f} F".format(SENSORS.get_temperature())
                DISPLAY.display_text(1, msg)
                msg = "HUMID: {:.1f} %".format(SENSORS.get_humidity())
                DISPLAY.display_text(2, msg)
                msg = "LIGHT: {:.1f} lux".format(SENSORS.get_lux())
                DISPLAY.display_text( 3, msg)
                CPU_DISPLAY = True
            DISPLAY.update_display()

        except BaseException as error:
            LOGGER.info('Exception Error - SENSORS collect_and_publish: {0}'.format(error))
