#!/usr/bin/python3
""" DIYHA Application Configuration Initializer """

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

import argparse
import logging
import logging.config

class ConfigModel:
    """ Command line argument model which expects an MQTT broker hostname or IP address,
        the location topic for the device and an option mode for the switch.
    """

    def __init__(self, logging_file):
        """ Parse the command line args """
        logging.config.fileConfig(fname=logging_file, disable_existing_loggers=False)
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)
        parser = argparse.ArgumentParser('Command Line Parser')
        parser.add_argument('--g', help='MQTT feed group name')
        parser.add_argument('--d', help='Display type or NA')
        args = parser.parse_args()

        # command line args for the MQTT feed group name
        if args.g is None:
            self.logger.error("Terminating --MQTT group not provided")
            exit()  # mandatory
        self.group = args.g

        # command line args for the optional display device
        if args.d is None:
            self.logger.error("Terminating --Display not provided")
            exit()  # mandatory
        self.display_name = args.d

        self.logger.info('Group={0} Display={1}'.format(self.group, self.display_name))
