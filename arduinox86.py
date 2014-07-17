# -*- coding: utf-8 -*-
"""
 Copyright © 2014, Emutex Ltd.
 All rights reserved.
 http://www.emutex.com

 Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>
 Author: Dave Hunt <dave@emutex.com>

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:

 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

 3. All modifications to the source code must be clearly marked as
    such. Binary redistributions based on modified source code must
    be clearly marked as modified versions in the documentation and/or
    other materials provided with the distribution.

 4. The name of Emutex Ltd. may not be used to endorse or promote
    products derived from this software without specific prior written
    permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES INCLUDING,
 BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
"""

import datetime
import os

INPUT = 'in'
INPUT_PULLUP = 'in_pullup'
INPUT_PULLDOWN = 'in_pulldown'
OUTPUT = 'out'
LOW = 'low'
HIGH = 'high'
NONE = 'in'
DRIVE_STRONG = 'strong'
DRIVE_HIZ = 'hiz'


class GPIOGalileoGen2(object):

    """Class for managing GPIO pinout on Intel® Galileo Gen2 board

    TODO: longer description here
    """

    GPIO_MAPPING = {
        0: 11,
        1: 12,
        2: 61,
        3: 62,
        4: 6,
        5: 0,
        6: 1,
        7: 38,
        8: 40,
        9: 4,
        10: 10,
        11: 5,
        12: 15,
        13: 7,
        14: 48,
        15: 50,
        16: 52,
        17: 54,
        18: 56,
        19: 58,
    }

    GPIO_MUX_OUTPUT = {
        0: ((32, LOW), (33, NONE)),
        1: ((45, LOW), (28, LOW), (29, NONE)),
        2: ((77, LOW), (34, LOW), (35, NONE), (13, NONE)),
        3: ((64, LOW), (76, LOW), (16, LOW), (17, NONE), (14, NONE)),
        4: ((36, LOW), (37, NONE)),
        5: ((66, LOW), (18, LOW), (19, NONE)),
        6: ((68, LOW), (20, LOW), (21, NONE)),
        7: ((39, NONE), ),
        8: ((41, NONE), ),
        9: ((70, LOW), (22, LOW), (23, NONE)),
        10: ((74, LOW), (26, LOW), (27, NONE)),
        11: ((44, LOW), (72, LOW), (24, LOW), (25, NONE)),
        12: ((42, LOW), (43, NONE)),
        13: ((46, LOW), (30, LOW), (31, NONE)),
        14: ((49, NONE), ),
        15: ((51, NONE), ),
        16: ((53, NONE), ),
        17: ((55, NONE), ),
        18: ((78, HIGH), (60, HIGH), (57, NONE)),
        19: ((79, HIGH), (60, HIGH), (59, NONE)),
    }

    GPIO_MUX_INPUT = {
        0: ((32, HIGH), (33, NONE)),
        1: ((45, LOW), (28, HIGH), (29, NONE)),
        2: ((77, LOW), (34, HIGH), (35, NONE)),  # FIXME: input always connected
        3: ((64, LOW), (76, LOW), (16, HIGH), (17, NONE)),  # FIXME: input always connected
        4: ((36, HIGH), (37, NONE)),
        5: ((66, LOW), (18, HIGH), (19, NONE)),
        6: ((68, LOW), (20, HIGH), (21, NONE)),
        7: ((38, HIGH), (39, NONE)),  # TODO update for Fab-G # FIXME: input always connected
        8: ((40, HIGH), (41, NONE)),  # TODO update for Fab-G # FIXME: input always connected
        9: ((70, LOW), (22, HIGH), (23, NONE)),
        10: ((74, LOW), (26, HIGH), (27, NONE)),
        11: ((44, LOW), (72, LOW), (24, HIGH), (25, NONE)),
        12: ((42, HIGH), (43, NONE)),
        13: ((46, LOW), (30, HIGH), (31, NONE)),
        14: ((49, NONE), ),  # FIXME
        15: ((51, NONE), ),  # FIXME
        16: ((53, NONE), ),  # FIXME
        17: ((55, NONE), ),  # FIXME
        18: ((78, HIGH), (60, HIGH), (57, NONE)),  # FIXME: input always connected
        19: ((79, HIGH), (60, HIGH), (59, NONE)),  # FIXME: input always connected
    }

    GPIO_MUX_INPUT_PULLUP = {
        0: ((32, HIGH), (33, HIGH)),
        1: ((45, LOW), (28, HIGH), (29, HIGH)),
        2: ((77, LOW), (34, HIGH), (35, HIGH)),
        3: ((64, LOW), (76, LOW), (16, HIGH), (17, HIGH)),
        4: ((36, HIGH), (37, HIGH)),
        5: ((66, LOW), (18, HIGH), (19, HIGH)),
        6: ((68, LOW), (20, HIGH), (21, HIGH)),
        7: ((38, HIGH), (39, HIGH)),  # TODO update for Fab-G
        8: ((40, HIGH), (41, HIGH)),  # TODO update for Fab-G
        9: ((70, LOW), (22, HIGH), (23, HIGH)),
        10: ((74, LOW), (26, HIGH), (27, HIGH)),
        11: ((44, LOW), (72, LOW), (24, HIGH), (25, HIGH)),
        12: ((42, HIGH), (43, HIGH)),
        13: ((46, LOW), (30, HIGH), (31, HIGH)),
        14: ((49, HIGH), ),  # FIXME
        15: ((51, HIGH), ),  # FIXME
        16: ((53, HIGH), ),  # FIXME
        17: ((55, HIGH), ),  # FIXME
        18: ((78, HIGH), (60, HIGH), (57, HIGH)),
        19: ((79, HIGH), (60, HIGH), (59, HIGH)),
    }

    GPIO_MUX_INPUT_PULLDOWN = {
        0: ((32, HIGH), ),
        1: ((45, LOW), (28, HIGH), (29, LOW)),
        2: ((77, LOW), (34, HIGH), (35, LOW)),
        3: ((64, LOW), (76, LOW), (16, HIGH), (17, LOW)),
        4: ((36, HIGH), (37, LOW)),
        5: ((66, LOW), (18, HIGH), (19, LOW)),
        6: ((68, LOW), (20, HIGH), (21, LOW)),
        7: ((38, HIGH), (39, LOW)),  # TODO update for Fab-G
        8: ((40, HIGH), (41, LOW)),  # TODO update for Fab-G
        9: ((70, LOW), (22, HIGH), (23, LOW)),
        10: ((74, LOW), (26, HIGH), (27, LOW)),
        11: ((44, LOW), (72, LOW), (24, HIGH), (25, LOW)),
        12: ((42, HIGH), (43, LOW)),
        13: ((46, LOW), (30, HIGH), (31, LOW)),
        14: ((49, LOW), ),  # FIXME
        15: ((51, LOW), ),  # FIXME
        16: ((53, LOW), ),  # FIXME
        17: ((55, LOW), ),  # FIXME
        18: ((78, HIGH), (60, HIGH), (57, LOW)),
        19: ((79, HIGH), (60, HIGH), (59, LOW)),
    }

    def __init__(self, debug=False):
        self.debug = debug
        self.pins_in_use = []
        self.gpio_handlers = {}

    def digitalWrite(self, pin, state):
        """Write a value to a GPIO pin.

        The GPIO pin is assumed to be configured as OUTPUT

        Args:
            pin: Arduino pin number (0-20)
            state: pin state to be written (LOW-HIGH)

         """
        if pin not in self.GPIO_MAPPING:
            return
        handler = self.gpio_handlers[self.GPIO_MAPPING[pin]]
        value = '0' if state == LOW else '1'
        handler.write(value)
        handler.seek(0)

    def digitalRead(self, pin):
        """Read GPIO pin's state.

        The GPIO pin is assumed to be configured as INPUT

        Args:
            pin: Arduino pin number (0-20)

        Returns:
            Current value of the GPIO pin as an Integer

        """
        if pin not in self.GPIO_MAPPING:
            return
        linux_pin = self.GPIO_MAPPING[pin]
        return self.__read_value(linux_pin)

    def pinMode(self, pin, mode):
        """Set mode to GPIO pin`.

        This function must be called before doing any other operation on the
        pin. It also sets up the muxing needed in Intel® Galileo Gen2 board for
        the pin to behave as the user wants to.

        Args:
            pin: Arduino pin number (0-20)
            mode: pin mode must be:
                OUTPUT: pin used as output. Use to write into it
                INPUT: pin used as input (high impedance). Use to read from it
                INPUT_PULLUP: pin used as input (pullup resistor). Use to read from it
                INPUT_PULLDOWN: pin used as input (pulldown resistor). Use to read from it

        """
        if pin not in self.GPIO_MAPPING:
            return

        if mode == OUTPUT:
            mux = self.GPIO_MUX_OUTPUT[pin]
        elif mode == INPUT:
            mux = self.GPIO_MUX_INPUT[pin]
        elif mode == INPUT_PULLUP:
            mux = self.GPIO_MUX_INPUT_PULLUP[pin]
        elif mode == INPUT_PULLDOWN:
            mux = self.GPIO_MUX_INPUT_PULLDOWN[pin]
        else:
            return

        pin = self.GPIO_MAPPING[pin]
        self.__export_pin(pin)
        self.__open_handler(pin)

        for vpin, value in mux:
            self.__export_pin(vpin)

            self.__set_direction(vpin, value)
            if value == NONE:
                self.__set_drive(vpin, DRIVE_HIZ)
            elif value in (HIGH, LOW):
                self.__set_drive(vpin, DRIVE_STRONG)
                self.__write_value(vpin, value)

        if mode == OUTPUT:
            self.__set_direction(pin, OUTPUT)
            self.__set_drive(pin, DRIVE_STRONG)
            self.__write_value(pin, LOW)
        elif mode in (INPUT, INPUT_PULLUP, INPUT_PULLDOWN):
            self.__set_direction(pin, INPUT)

    def cleanup(self):
        """Do a general cleanup.

        Close all open handlers for reading and writing.
        Unexport all exported GPIO pins.

        Calling this function is not mandatory but it's recommended once you are
        done using the library if it's being used with a larger application
        that runs for a long period of time.
        """
        for pin in self.pins_in_use:
            self.__unexport_pin(pin)
        del self.pins_in_use[:]

        for handler in self.gpio_handlers.values():
            handler.close()
        self.gpio_handlers.clear()

    def __open_handler(self, linux_pin):
        try:
            f = open('/sys/class/gpio/gpio%d/value' % linux_pin, 'w')
            self.gpio_handlers[linux_pin] = f
        except:
            print "Failed opening value file for pin %d" % linux_pin

    def __write_value(self, linux_pin, state):
        value = 1
        if state == LOW:
            value = 0
        cmd = 'echo %d > /sys/class/gpio/gpio%d/value' % (value, linux_pin)
        self.__exec_cmd(self.__write_value.__name__, cmd)

    def __read_value(self, linux_pin):
        cmd = '/sys/class/gpio/gpio%d/value' % (linux_pin)
        self.__debug(self.__read_value.__name__, cmd)
        f = open(cmd, 'r')
        state = f.read()
        f.close()
        return int(state.strip())

    def __set_direction(self, linux_pin, direction):
        cmd = 'echo %s > /sys/class/gpio/gpio%d/direction' % (direction, linux_pin)
        self.__exec_cmd(self.__set_direction.__name__, cmd)

    def __export_pin(self, linux_pin):
        self.pins_in_use.append(linux_pin)
        cmd = 'echo %d > /sys/class/gpio/export' % linux_pin
        self.__exec_cmd(self.__export_pin.__name__, cmd)

    def __unexport_pin(self, linux_pin):
        cmd = 'echo %d > /sys/class/gpio/unexport' % linux_pin
        self.__exec_cmd(self.__unexport_pin.__name__, cmd)

    def __set_drive(self, linux_pin, drive):
        cmd = 'echo %s > /sys/class/gpio/gpio%d/drive' % (drive, linux_pin)
        self.__exec_cmd(self.__set_drive.__name__, cmd)

    def __debug(self, func_name, cmd):
        if self.debug:
            now = datetime.datetime.now().strftime("%B %d %I:%M:%S")
            print '{0} {1: <20}{2}'.format(now, func_name + ':', cmd)

    def __exec_cmd(self, caller, command):
        self.__debug(caller, command)
        os.system(command)

setattr(GPIOGalileoGen2, 'INPUT', INPUT)
setattr(GPIOGalileoGen2, 'INPUT_PULLUP', INPUT_PULLUP)
setattr(GPIOGalileoGen2, 'INPUT_PULLDOWN', INPUT_PULLDOWN)
setattr(GPIOGalileoGen2, 'OUTPUT', OUTPUT)
setattr(GPIOGalileoGen2, 'LOW', LOW)
setattr(GPIOGalileoGen2, 'HIGH', HIGH)
