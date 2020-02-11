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

""" REST API for fast query of heat pump parameters representing a 'MP' data point. """

import logging
from flask import request
from flask_restx import Namespace, Resource, fields
from htheatpump.htparams import HtParams
from .utils import ParamValueField, DotKeyField
from htrest.app import ht_heatpump  # type: ignore


_logger = logging.getLogger(__name__)


api = Namespace("fastquery", description="Fast query of heat pump parameters representing a 'MP' data point.")

wildcard = fields.Wildcard(DotKeyField)
param_list_model = api.model("param_list_model", {
    "*": wildcard
})
param_model = api.model("param_model", {
    "value": ParamValueField
})


@api.route("/")
class FastQueryList(Resource):
    @api.marshal_with(param_list_model)
    def get(self):
        """ Performs a fast query of all heat pump parameters representing a 'MP' data point. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s}".format(request.url))
        return ht_heatpump.fast_query()


@api.route("/<string:name>")
@api.param("name", "The parameter name (which represents a 'MP' data point)")
@api.response(404, "Parameter not found")
class FastQuery(Resource):
    @api.marshal_with(param_model)
    def get(self, name: str):
        """ Performs a fast query of a specific heat pump parameter which represents a 'MP' data point. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        if name not in HtParams:
            api.abort(404, "Parameter '{}' not found".format(name))
        _logger.debug("*** {!s} -- name={!r}".format(request.url, name))
        value = ht_heatpump.fast_query(name)
        return {"value": value[name]}
