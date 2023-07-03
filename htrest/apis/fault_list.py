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

""" REST API for operations related to the heat pump fault list. """

import logging
from typing import Final

from flask import current_app, request
from flask_restx import Namespace, Resource, fields

from .utils import HtContext

_LOGGER: Final = logging.getLogger(__name__)

api: Final = Namespace("faultlist", description="Operations related to the heat pump fault list.")

# Single fault list entry of the heat pump, e.g.:
#
#   { "index"   : 28,                      # fault list index
#     "error"   : 19,                      # error code
#     "datetime": datetime.datetime(...),  # date and time of the entry
#     "message" : "EQ_Spreizung",          # error message
#     }
#
fault_list_entry_model: Final = api.model(
    "fault_list_entry_model",
    {
        "index": fields.Integer(
            min=0,
            description="fault list index",
            required=True,
            readonly=True,
            example=28,
        ),
        "error": fields.Integer(min=0, description="error code", required=True, readonly=True, example=19),
        "datetime": fields.DateTime(
            dt_format="iso8601",
            description="date and time of the error",
            required=True,
            readonly=True,
            example="2014-09-14T02:08:56",
        ),
        "message": fields.String(
            description="error message",
            required=True,
            readonly=True,
            example="EQ_Spreizung",
        ),
    },
)

fault_list_size_model: Final = api.model(
    "fault_list_size_model",
    {
        "size": fields.Integer(
            min=0,
            description="fault list size",
            required=True,
            readonly=True,
            example=62,
        ),
    },
)


@api.route("/")
class FaultList(Resource):
    @api.marshal_list_with(fault_list_entry_model)
    def get(self):
        """Returns the fault list of the heat pump."""
        _LOGGER.info("*** [GET] %s", request.url)
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            res = current_app.ht_heatpump.get_fault_list()  # type: ignore[attr-defined]
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res


@api.route("/size")
class FaultListSize(Resource):
    @api.marshal_with(fault_list_size_model)
    def get(self):
        """Returns the fault list size of the heat pump."""
        _LOGGER.info("*** [GET] %s", request.url)
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            size = current_app.ht_heatpump.get_fault_list_size()  # type: ignore[attr-defined]
        res = {"size": size}
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res


@api.route("/<int:id>")
@api.param("id", "The fault list index")
@api.response(404, "Fault list entry not found")
class FaultEntry(Resource):
    @api.marshal_with(fault_list_entry_model)
    def get(self, identifier: int):
        """Returns the fault list entry with the given index."""
        _LOGGER.info("*** [GET] %s -- id=%d", request.url, identifier)
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            if identifier not in range(0, current_app.ht_heatpump.get_fault_list_size()):  # type: ignore[attr-defined]
                api.abort(404, "Fault list entry #{:d} not found".format(identifier))
            res = current_app.ht_heatpump.get_fault_list(identifier)[0]  # type: ignore[attr-defined]
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res


@api.route("/last")
class LastFault(Resource):
    @api.marshal_with(fault_list_entry_model)
    def get(self):
        """Returns the last fault list entry of the heat pump."""
        _LOGGER.info("*** [GET] %s", request.url)
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            idx, err, dt, msg = current_app.ht_heatpump.get_last_fault()  # type: ignore[attr-defined]
            # e.g.: idx, err, dt, msg = (28, 19, datetime.datetime.now(), "EQ_Spreizung")
            res = {"index": idx, "error": err, "datetime": dt, "message": msg}
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res
