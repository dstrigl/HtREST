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

""" REST API for operations related to the heat pump fault list. """

import logging
from flask import request
from flask_restx import Namespace, Resource, fields
from htrest.app import ht_heatpump  # type: ignore


_logger = logging.getLogger(__name__)

api = Namespace("faultlist", description="Operations related to the heat pump fault list.")

# Single fault list entry of the heat pump, e.g.:
#
#   { "index"   : 28,                      # fault list index
#     "error"   : 19,                      # error code
#     "datetime": datetime.datetime(...),  # date and time of the entry
#     "message" : "EQ_Spreizung",          # error message
#     }
#
fault_list_entry_model = api.model("fault_list_entry_model", {
    "index":    fields.Integer(min=0, description="fault list index", required=True, readonly=True, example=28),
    "error":    fields.Integer(min=0, description="error code", required=True, readonly=True, example=19),
    "datetime": fields.DateTime(dt_format="iso8601", description="date and time of the error",
                                required=True, readonly=True, example="2014-09-14T02:08:56"),
    "message":  fields.String(description="error message", required=True, readonly=True, example="EQ_Spreizung"),
})

fault_list_size_model = api.model("fault_list_size_model", {
    "size": fields.Integer(min=0, description="fault list size", required=True, readonly=True, example=62),
})


@api.route("/")
class FaultList(Resource):
    @api.marshal_list_with(fault_list_entry_model)
    def get(self):
        """ Returns the fault list of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s}".format(request.url))
        return ht_heatpump.get_fault_list()


@api.route("/size")
class FaultListSize(Resource):
    @api.marshal_with(fault_list_size_model)
    def get(self):
        """ Returns the fault list size of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s}".format(request.url))
        return {"size": ht_heatpump.get_fault_list_size()}


@api.route("/<int:id>")
@api.param("id", "The fault list index")
@api.response(404, "Fault list entry not found")
class FaultEntry(Resource):
    @api.marshal_with(fault_list_entry_model)
    def get(self, id: int):
        """ Returns the fault list entry with the given index. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        if id not in range(0, ht_heatpump.get_fault_list_size()):
            api.abort(404, "Fault list entry #{:d} not found".format(id))
        _logger.debug("*** {!s} -- id={}".format(request.url, id))
        return ht_heatpump.get_fault_list(id)[0]


@api.route("/last")
class LastFault(Resource):
    @api.marshal_with(fault_list_entry_model)
    def get(self):
        """ Returns the last fault list entry of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s}".format(request.url))
        idx, err, dt, msg = ht_heatpump.get_last_fault()
        # e.g.: idx, err, dt, msg = (28, 19, datetime.datetime.now(), "EQ_Spreizung")
        return {"index": idx, "error": err, "datetime": dt, "message": msg}
