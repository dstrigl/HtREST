#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  HtREST - Heliotherm heat pump REST API
#  Copyright (C) 2021  Daniel Strigl

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

""" Heliotherm heat pump REST API server APIv1. """

import logging

from flask import Blueprint  # , request
from flask_restx import Api

from .apis.date_time import api as ns3
from .apis.device import api as ns1
from .apis.fast_query import api as ns5
from .apis.fault_list import api as ns2
from .apis.param import api as ns4
from .apis.time_prog import api as ns6

_LOGGER = logging.getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    title="HtREST",
    version="1.0",
    description="Heliotherm heat pump REST API",
    # All API metadatas
)
api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
api.add_namespace(ns4)
api.add_namespace(ns5)
api.add_namespace(ns6)


@blueprint.before_request
def before_request():
    # _LOGGER.debug("*** @blueprint.before_request -- %s -- %s", __file__, request)
    #
    # Not necessary, since login() will automatically try a reconnect on failure:
    #
    # try:
    #    ht_heatpump.reconnect()
    # except Exception as ex:
    #    _LOGGER.error(ex)
    #    raise
    pass


@blueprint.after_request
def after_request(response):
    # _LOGGER.debug("*** @blueprint.after_request -- %s -- %s", __file__, response)
    return response


@blueprint.teardown_request
def teardown_request(exc):
    # _LOGGER.debug("*** @blueprint.teardown_request -- %s -- %s", __file__, exc)
    pass


@api.errorhandler
def default_error_handler(ex):
    msg = str(ex)
    # remove leading and trailing '"' in case of a KeyError
    #   see: https://stackoverflow.com/questions/24998968/why-does-strkeyerror-add-extra-quotes
    if isinstance(ex, KeyError) and msg.startswith('"') and msg.endswith('"'):
        msg = msg[1:-1]
    _LOGGER.error("*** @api.errorhandler -- %s", msg)
    return {"message": str(msg)}, 500
