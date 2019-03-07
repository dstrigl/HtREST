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
from flask_restplus import Namespace, Resource, fields
from htrest import ht_heatpump


log = logging.getLogger(__name__)

api = Namespace("faultlist", description="Operations related to the heat pump fault list")

# Single fault list entry of the heat pump, e.g.:
#
#   { "index"   : 29,                      # fault list index
#     "error"   : 20,                      # error code
#     "datetime": datetime.datetime(...),  # date and time of the entry
#     "message" : "EQ_Spreizung",          # error message
#     }
#
fault_list_entry = api.model("fault_list_entry", {  # TODO
    "index":    fields.Integer(min=0),
    "error":    fields.Integer(min=0),
    "datetime": fields.DateTime(dt_format="rfc822"),  # TODO
    "message":  fields.String,
})


@api.route("/")
class FaultList(Resource):
    @api.marshal_list_with(fault_list_entry)
    def get(self):
        """ Returns the fault list of the heat pump. """
        log.info("*** {!s}".format(request.url))
        return ht_heatpump.get_fault_list()


@api.route("/<int:id>")
@api.param("id", "The fault list index")
@api.response(404, "Fault list entry not found")
class FaultEntry(Resource):
    @api.marshal_with(fault_list_entry)
    def get(self, id):
        """ Returns the fault list entry with the given index. """
        if id not in range(0, ht_heatpump.get_fault_list_size()):
            api.abort(404, "Fault list entry #{:d} not found".format(id))
        log.info("*** {!s} -- id={:d}".format(request.url, id))
        return ht_heatpump.get_fault_list(id)


@api.route("/last")
class LastFault(Resource):
    @api.marshal_with(fault_list_entry)
    def get(self):
        """ Returns the last fault list entry of the heat pump. """
        log.info("*** {!s}".format(request.url))
        idx, err, dt, msg = ht_heatpump.get_last_fault()
        #idx, err, dt, msg = (29, 20, datetime.datetime.now(), "EQ_Spreizung")
        return {"index": idx, "error": err, "datetime": dt, "message": msg}
