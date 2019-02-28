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
from flask import request
from flask_restplus import Namespace, Resource


log = logging.getLogger(__name__)

api = Namespace("faultlist", description="Operations related to the heat pump fault list")


@api.route("/")
class FaultList(Resource):
    def get(self):
        """ TODO """
        log.info("*** {!s}".format(request.url))
        return "test"


@api.route("/<int:id>")
@api.param("id", "The fault list index")
@api.response(404, "Fault list item not found")
class FaultItem(Resource):
    def get(self, id):
        """ TODO """
        log.info("*** {!s}".format(request.url))
        #api.abort(404)
        return {"message": "Fault list item #{:d} not found".format(id)}, 404
