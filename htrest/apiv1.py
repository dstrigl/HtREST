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

import logging
from flask import Blueprint, request
from flask_restplus import Api
from htrest import ht_heatpump
from htrest.apis.fault_list import api as ns1
from htrest.apis.device import api as ns2
from htrest.apis.date_time import api as ns3


_logger = logging.getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(blueprint,
          title="HtREST",
          version="1.0",
          description="Heliotherm heat pump REST API",
          # All API metadatas
          )
api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)


@blueprint.before_request
def before_request():
    _logger.info("*** @blueprint.before_request -- {} -- {!s}".format(__file__, request))
    try:
        ht_heatpump.reconnect()
        ht_heatpump.login()
    except Exception as ex:
        _logger.error(ex)
        #raise  # TODO
    # TODO call reconnect/login ONLY for registered routes!


@blueprint.after_request
def after_request(response):
    _logger.info("*** @blueprint.after_request -- {} -- {!s}".format(__file__, response))
    return response


@blueprint.teardown_request
def teardown_request(exc):
    _logger.info("*** @blueprint.teardown_request -- {} -- {!s}".format(__file__, exc))
    ht_heatpump.logout()
    # TODO call logout ONLY for registered routes!


@api.errorhandler
def default_error_handler(ex):
    msg = str(ex)
    # remove leading and trailing '"' in case of a KeyError
    #   see: https://stackoverflow.com/questions/24998968/why-does-strkeyerror-add-extra-quotes
    if isinstance(ex, KeyError) and msg.startswith('"') and msg.endswith('"'):
        msg = msg[1:-1]
    #_logger.exception("*** @api.errorhandler -- {}".format(msg))
    _logger.error("*** @api.errorhandler -- {}".format(msg))
    #if not current_app.debug:
    return {"message": str(msg)}, 500
