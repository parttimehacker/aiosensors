#!/usr/bin/python3
""" DIYHA MQTT CPU and OS monitor """

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

import socket
import logging
import logging.config
import subprocess

class StatusModel:
    """ Collect CPU and OS metrics. Publish and log the information every 15 minutes. """

    def __init__(self, logging_file):
        ''' Setup MQTT topics and initialize data elements '''
        logging.config.fileConfig(fname=logging_file, disable_existing_loggers=False)
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)
        self.host_name = socket.gethostname()
        self.os_version = self.get_os_version()
        self.pi_version = self.get_pi_version()
        self.ip_address = self.get_ip_address()
        self.logger.info('Host Name={0} IP={1}'.format(self.host_name, self.ip_address))
        self.logger.info('OS={0}'.format(self.os_version))
        self.logger.info('PI={0}'.format(self.pi_version))

    def get_os_version(self, ):
        ''' get the current os version and make available to observers '''
        cmd = subprocess.Popen('cat /etc/os-release', shell=True, stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if b'=' in line:
                key, value = line.split(b'=')
                if b'VERSION' == key:
                    data, chaff = value.split(b'\n')
                    strData = str(data, 'utf-8')
                    return "Raspbian " + strData.replace('"', '')

    def get_pi_version(self, ):
        ''' get the current pi version and make available to observers '''
        cmd = subprocess.Popen('cat /proc/device-tree/model', shell=True, stdout=subprocess.PIPE)
        for line in cmd.stdout:
            key, value = line.split(b' Pi ')
            data, chaff = value.split(b'\x00')
            return str(data, 'utf-8')

    def get_ip_address(self, ):
        ''' get the current ip address and make available to observers '''
        ip = subprocess.check_output(["hostname", "-I"])
        ips = ip.decode("utf-8")
        ipss = ips.split(" ", 1)
        return ipss[0]
