#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  HtREST - Heliotherm heat pump REST API
#  Copyright (C) 2023  Daniel Strigl

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

import atexit
import logging
from typing import Final, Optional

from flask import Flask, current_app
from flask_basicauth import BasicAuth
from htheatpump import HtHeatpump, VerifyAction

from . import settings

_LOGGER: Final = logging.getLogger(__name__)


def create_app(
    device: str = "/dev/ttyUSB0",
    baudrate: int = 115200,
    user: Optional[str] = None,
    bool_as_int: bool = False,
    read_only: bool = False,
    no_param_verification: bool = False,
) -> Flask:
    # try to connect to the heat pump
    ht_heatpump: Final = HtHeatpump(device, baudrate=baudrate)
    if no_param_verification:
        ht_heatpump.verify_param_action = VerifyAction.NONE()
    _LOGGER.info("open connection to heat pump (%s)", ht_heatpump)
    try:
        ht_heatpump.open_connection()
        ht_heatpump.login()
        _LOGGER.info("successfully connected to heat pump #%d", ht_heatpump.get_serial_number())
        _LOGGER.info("software version = %s (%d)", *ht_heatpump.get_version())
    except Exception as ex:
        _LOGGER.error(ex)
        raise
    finally:
        ht_heatpump.logout()

    def on_exit_app(ht_hp: HtHeatpump):
        _LOGGER.debug("*** @on_exit_app -- %s -- %s", __file__, ht_hp)
        # ht_hp.logout()
        ht_hp.close_connection()

    atexit.register(on_exit_app, ht_hp=ht_heatpump)

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
        _ = BasicAuth(app)
    _LOGGER.info("*** created Flask app %s with config %s", app, app.config)

    settings.BOOL_AS_INT = bool_as_int
    settings.READ_ONLY = read_only

    with app.app_context():
        current_app.ht_heatpump = ht_heatpump  # type: ignore[attr-defined]

        from htrest.apiv1 import blueprint as apiv1

        app.register_blueprint(apiv1)
        # _LOGGER.info(apiv1.url_prefix)
        _LOGGER.info(app.url_map)

        return app
