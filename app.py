#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  HtREST - Heliotherm heat pump REST API
#  Copyright (C) 2020  Daniel Strigl

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" TODO """

import os
import argparse
import textwrap
import logging.config
from htrest import create_app


def main():
    parser = argparse.ArgumentParser(
        description = textwrap.dedent('''\
            *** TODO ***
            '''),
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog = textwrap.dedent('''\
            DISCLAIMER
            ----------

              Please note that any incorrect or careless usage of this program as well as
              errors in the implementation can damage your heat pump!

              Therefore, the author does not provide any guarantee or warranty concerning
              to correctness, functionality or performance and does not accept any liability
              for damage caused by this program or mentioned information.

              Thus, use it on your own risk!
            ''') + "\r\n")

    parser.add_argument(
        "-d", "--device",
        default = "/dev/ttyUSB0",
        type = str,
        help = "the serial device on which the heat pump is connected, default: %(default)s")

    parser.add_argument(
        "-b", "--baudrate",
        default = 115200,
        type = int,
        # the supported baudrates of the Heliotherm heat pump (HP08S10W-WEB):
        choices = [9600, 19200, 38400, 57600, 115200],
        help = "baudrate of the serial connection (same as configured on the heat pump), default: %(default)s")

    parser.add_argument(
        "-s", "--server",
        default = "localhost:8888",
        type = str,
        help = "the name and port number of the server in the form <hostname>:<port>, default: %(default)s")

    parser.add_argument(
        "-l", "--logging-config",
        default = os.path.normpath(os.path.join(os.path.dirname(__file__), "logging.conf")),
        type = str,
        help = "the filename under which the logging configuration can be found, default: %(default)s")

    parser.add_argument(
        "--debug",
        action = "store_true",
        help = "enable Flask debug mode, default: %(default)s")

    args = parser.parse_args()
    #print(args)

    # load logging config from file
    logging.config.fileConfig(args.logging_config, disable_existing_loggers=False)

    # create and start the Flask application
    app = create_app(args.device, args.baudrate, args.server)
    app.run(debug=args.debug, use_reloader=False)


if __name__ == "__main__":
    main()
