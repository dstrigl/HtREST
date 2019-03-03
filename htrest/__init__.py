#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  HtREST - Heliotherm heat pump REST API
#  Copyright (C) 2019  Daniel Strigl

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

from flask import Flask
from htrest import settings
import htrest.version as __version
__version__ = __version.version.short()
__author__ = "Daniel Strigl"


def configure_app(app):
    app.config["SERVER_NAME"] = settings.FLASK_SERVER_NAME
    app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config["RESTPLUS_VALIDATE"] = settings.RESTPLUS_VALIDATE
    app.config["RESTPLUS_MASK_SWAGGER"] = settings.RESTPLUS_MASK_SWAGGER
    app.config["ERROR_404_HELP"] = settings.RESTPLUS_ERROR_404_HELP


def create_app():
    from htheatpump.htheatpump import HtHeatpump
    global hthp
    hthp = HtHeatpump("/dev/ttyUSB0", baudrate=115200)
    hthp.open_connection()
    hthp.login()
    rid = hthp.get_serial_number()
    print("connected successfully to heat pump with serial number {:d}".format(rid))
    ver = hthp.get_version()
    print("software version = {} ({:d})".format(ver[0], ver[1]))
    #hthp.logout()
    #hthp.close_connection()

    app = Flask(__name__)
    configure_app(app)

    from htrest.apiv1 import blueprint as apiv1
    app.register_blueprint(apiv1)

    return app
