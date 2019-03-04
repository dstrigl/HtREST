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
#from htrest import settings
from htrest.apis.faultlist import api as ns1


log = logging.getLogger(__name__)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

@blueprint.before_request
def before_request():
    log.info("*** before_request: " + __file__ + " " + str(request))

@blueprint.after_request
def after_request(response):
    log.info("*** after_request: " + __file__ + " " + str(response))
    return response

api = Api(blueprint,
          title="HtREST",
          version="1.0",
          description="Heliotherm heat pump REST API",
          # All API metadatas
          )
api.add_namespace(ns1)

@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    log.exception("*** message: " + message)
    #if not settings.FLASK_DEBUG:
    #    return {"message": message}, 500
