#!/usr/bin/python3
""" DIYHA sensor hardware abstraction layer """

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

import logging
import logging.config

import board
import adafruit_bme680
import adafruit_veml7700

from Adafruit_IO import MQTTClient

class SensorHAL:
    """ Collect sensor data, publish and log the information. """

    def __init__(self, logging_file, group_name, temperature_offset):
        ''' Setup MQTT topics and initialize data elements '''
        logging.config.fileConfig(fname=logging_file, disable_existing_loggers=False)
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)

        self.group_name = group_name
        self.temperature_offset = temperature_offset

        self.connected = False

        # Create sensor objects, communicating over the board's default I2C bus
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
        self.bme680.sea_level_pressure = 1015.0
        '''
        # Set up the sensor
        self.bme680._humidity_oversample(self.bme680.OS_2X)
        self.bme680._pressure_oversample(self.bme680.OS_4X)
        self.bme680.set_temperature_oversample(self.bme680.OS_8X)
        self.bme680.set_filter(self.bme680.FILTER_SIZE_3)
        self.bme680.set_gas_status(self.bme680.ENABLE_GAS_MEAS)

        # Set the gas heater temperature and duration
        self.bme680.set_gas_heater_temperature(320)
        self.bme680.set_gas_heater_duration(150)
        self.bme680.select_gas_heater_profile(0)
        '''
        self.veml7700 = adafruit_veml7700.VEML7700(i2c)

        self.temperature = 77.7
        self.humidity = 77.7
        self.lux = 77.7

    def calculate_iaq(self, gas_resistance, humidity):
        humidity_weighting = 0.25
        gas_reference = 350000  # This is a reference value, adjust as necessary

        # Calculate humidity score
        humidity_score = 0
        if 38 <= humidity <= 42:
            humidity_score = 0.25 * 100  # ideal humidity
        elif humidity < 38:
            humidity_score = (humidity_weighting / 38) * humidity * 100
        else:
            humidity_score = max(0, (humidity_weighting / (42 - 38)) * (42 - humidity)) * 100

        # Calculate gas score
        gas_score = (1 - (gas_resistance / gas_reference)) * (100 - humidity_weighting * 100)

        # Calculate IAQ index
        iaq = humidity_score + gas_score
        return iaq

    def connection(self, client):
        self.client = client
        self.connected = True

    def collect_and_publish(self):

        if not self.connected:
            return

        try:
            self.temperature = 9.0 / 5.0 * self.bme680.temperature + 32 + self.temperature_offset
            self.client.publish('temperature', self.temperature, self.group_name)
        except IOError as e:
            self.logger.info('IO Error on BME680: {0}'.format(e))
        except Exception as e:
            self.logger.info('Exception Error - Not IOError - on BME680: {0}'.format(e))

        try:
            self.humidity = self.bme680.humidity
            self.client.publish('humidity', self.humidity, self.group_name)
        except IOError as e:
            self.logger.info('IO Error on BME680: {0}'.format(e))
        except Exception as e:
            self.logger.info('Exception Error - Not IOError - on BME680: {0}'.format(e))

        try:
            gas_resistance = self.bme680.gas
            humidity = self.bme680.humidity
            iaq = self.calculate_iaq(gas_resistance, humidity)
            # print(f"IAQ: {iaq:.2f}, Gas Resistance: {gas_resistance} Ohms, Humidity: {humidity:.2f} %")
            self.client.publish('iaq', iaq, self.group_name)

        except IOError as e:
            self.logger.info('IO Error on BME680: {0}'.format(e))
        except Exception as e:
            self.logger.info('Exception Error - Not IOError - on BME680: {0}'.format(e))

        try:
            self.lux = self.veml7700.lux
            self.client.publish('lux', self.lux, self.group_name)
        except IOError as e:
            self.logger.info('IO Error on VEML7700: {0}'.format(e))
        except Exception as e:
            self.logger.info('Exception Error - Not IOError - on VEML7700: {0}'.format(e))

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_lux(self):
        return self.lux
