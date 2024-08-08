#!/usr/bin/python3
""" DIYHA MQTT CPU and OS monitor """

# The MIT License (MIT)
#
# Copyright (c) 2019 parttimehacker@gmail.com
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

import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import logging
import logging.config

# Set up GPIO pin for interrupt
BUTTON_PIN_A = board.D23  # Change to the appropriate pin

class ST7789HAL:
    """ Manage an st7789 LCD display with a hardware abstraction layer. """

    def __init__(self, logging_file):
        ''' initialize hardware and data elements '''
        logging.config.fileConfig(fname=logging_file, disable_existing_loggers=False)
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)
        self.set_data_structures()
        self.init_st7789_display()

    def set_data_structures(self, ):
        self.row_text = ["", "", "", ""]
        self.row_Y_cord = [0, 30, 60, 90]
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        self.row_font = [self.font, self.font, self.font, self.font]
        self.row_fill = ["#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF"]

    def init_st7789_display(self, ):
        # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = None

        # Config for display baudrate (default max is 24mhz):
        BAUDRATE = 64000000

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()

        # Create the ST7789 display:
        self.disp = st7789.ST7789(
            spi,
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
            width=135,
            height=240,
            x_offset=53,
            y_offset=40,
        )

        # self.buttonA = digitalio.DigitalInOut(board.D23)
        # self.buttonB = digitalio.DigitalInOut(board.D24)
        # self.buttonA.switch_to_input()
        # self.buttonB.switch_to_input()

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        self.height = self.disp.width  # we swap height/width to rotate it to landscape!
        self.width = self.disp.height
        self.image = Image.new("RGB", (self.width, self.height))
        self.rotation = 90

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(self.image, self.rotation)
        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        bottom = self.height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        # Turn on the backlight
        backlight = digitalio.DigitalInOut(board.D22)
        backlight.switch_to_output()
        backlight.value = True
    '''         
    def get_buttona_status(self):
        print(self.buttonA.value)
        return self.buttonA.value

    def get_buttonb_status(self):
        print(self.buttonB.value)
        return self.buttonB.value
    '''
    def clear_display(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(self.image, self.rotation)

    def display_text(self, row=0, text="", font="Default", fill="#FFFFFF"):
        # print(row, text, font, fill)
        self.row_text[row] = text
        if font == "Default":
            self.row_font[row] = self.font
        else:
            self.row_font[row] = font
        self.row_fill[row] = fill

    def update_display(self):
        self.clear_display()
        for i in range(0, 4):
            self.draw.text((0, self.row_Y_cord[i]), self.row_text[i], font=self.row_font[i], fill=self.row_fill[i])
        self.disp.image(self.image, self.rotation)