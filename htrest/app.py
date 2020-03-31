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
from flask_basicauth import BasicAuth
from htrest import settings
from htheatpump.htheatpump import HtHeatpump, VerifyAction


_logger = logging.getLogger(__name__)

ht_heatpump = None  # type: HtHeatpump


def create_app(
    device="/dev/ttyUSB0",
    baudrate=115200,
    user=None,
    bool_as_int=False,
    read_only=False,
    no_param_verification=False,
):
    # try to connect to the heat pump
    global ht_heatpump
    try:
        ht_heatpump = HtHeatpump(device, baudrate=baudrate)
        if no_param_verification:
            ht_heatpump.verify_param_action = VerifyAction.NONE()
        _logger.info("open connection to heat pump ({!s})".format(ht_heatpump))
        ht_heatpump.open_connection()
        ht_heatpump.login()
        _logger.info(
            "successfully connected to heat pump #{:d}".format(
                ht_heatpump.get_serial_number()
            )
        )
        _logger.info("software version = {} ({:d})".format(*ht_heatpump.get_version()))
    except Exception as ex:
        _logger.error(ex)
        raise
    finally:
        ht_heatpump.logout()

    # create the Flask app
    app = Flask(__name__)
    app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.RESTX_SWAGGER_UI_DOC_EXPANSION
    app.config["RESTX_VALIDATE"] = settings.RESTX_VALIDATE
    app.config["RESTX_MASK_SWAGGER"] = settings.RESTX_MASK_SWAGGER
    app.config["ERROR_404_HELP"] = settings.RESTX_ERROR_404_HELP
    app.config["BUNDLE_ERRORS"] = settings.RESTX_BUNDLE_ERRORS
    if user:
        username, _, password = user.partition(":")
        app.config["BASIC_AUTH_USERNAME"] = username
        app.config["BASIC_AUTH_PASSWORD"] = password
        app.config["BASIC_AUTH_FORCE"] = True
        basic_auth = BasicAuth(app)  # noqa: F841
    _logger.info("*** created Flask app {!s} with config {!s}".format(app, app.config))

    @app.before_first_request
    def before_first_request():
        # _logger.debug("*** @app.before_first_request -- {}".format(__file__))
        pass

    settings.BOOL_AS_INT = bool_as_int
    settings.READ_ONLY = read_only

    from htrest.apiv1 import blueprint as apiv1

    app.register_blueprint(apiv1)
    # print(apiv1.url_prefix)
    print(app.url_map)

    return app
