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

""" Heliotherm heat pump REST API Flask application. """

import logging
from flask import Flask
from htrest import settings
import htrest.version as __version
__version__ = __version.version.short()
__author__ = "Daniel Strigl"


_logger = logging.getLogger(__name__)


def create_app(device="/dev/ttyUSB0", baudrate=115200, server="localhost:8888"):
    # try to connect to the heat pump
    try:
        from htheatpump.htheatpump import HtHeatpump
        global ht_heatpump
        ht_heatpump = HtHeatpump(device, baudrate=baudrate)
        _logger.info("open connection to heat pump ({!s})".format(ht_heatpump))
        ht_heatpump.open_connection()
        ht_heatpump.login()
        _logger.info("successfully connected to heat pump #{:d}".format(ht_heatpump.get_serial_number()))
        _logger.info("software version = {} ({:d})".format(*ht_heatpump.get_version()))
        ht_heatpump.logout()
    except Exception as ex:
        _logger.error(ex)
        raise

    # create the Flask app
    app = Flask(__name__)
    app.config["SERVER_NAME"] = server
    app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config["RESTPLUS_VALIDATE"] = settings.RESTPLUS_VALIDATE
    app.config["RESTPLUS_MASK_SWAGGER"] = settings.RESTPLUS_MASK_SWAGGER
    app.config["ERROR_404_HELP"] = settings.RESTPLUS_ERROR_404_HELP
    app.config["BUNDLE_ERRORS"] = settings.RESTPLUS_BUNDLE_ERRORS
    _logger.info("*** created Flask app {!s} with config {!s}".format(app, app.config))

    @app.before_first_request
    def before_first_request():
        #_logger.info("*** @app.before_first_request -- {}".format(__file__))
        pass

    from htrest.apiv1 import blueprint as apiv1
    app.register_blueprint(apiv1)

    return app
