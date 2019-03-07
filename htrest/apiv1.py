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
from htrest.apis.faultlist import api as ns1
from htrest.apis.device import api as ns2


log = logging.getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(blueprint,
          title="HtREST",
          version="1.0",
          description="Heliotherm heat pump REST API",
          # All API metadatas
          )
api.add_namespace(ns1)
api.add_namespace(ns2)


@blueprint.before_request
def before_request():
    log.info("*** @blueprint.before_request -- {} -- {!s}".format(__file__, request))
    ht_heatpump.reconnect()
    ht_heatpump.login()
    # TODO exception handling?


@blueprint.after_request
def after_request(response):
    log.info("*** @blueprint.after_request -- {} -- {!s}".format(__file__, response))
    return response


@blueprint.teardown_request
def teardown_request(exc):
    log.info("*** @blueprint.teardown_request -- {} -- {!s}".format(__file__, exc))
    ht_heatpump.logout()


@api.errorhandler
def default_error_handler(ex):
    #log.exception("*** @api.errorhandler -- {!s}".format(ex))
    log.error("*** @api.errorhandler -- {!s}".format(ex))
    #if not current_app.debug:
    return {"message": str(ex)}, 500
