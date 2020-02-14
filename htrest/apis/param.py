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

""" REST API for operations related to the heat pump parameters. """

import logging
from flask import request
from flask_restx import Namespace, Resource, fields
from htheatpump.htparams import HtParams
from .utils import ParamValueField, DotKeyField
from htrest.app import ht_heatpump  # type: ignore
from htrest.settings import READ_ONLY as HTREST_READ_ONLY


_logger = logging.getLogger(__name__)


api = Namespace("param", description="Operations related to the heat pump parameters.")

wildcard = fields.Wildcard(DotKeyField)
param_list_model = api.model("param_list_model", {
    "*": wildcard
})
param_model = api.model("param_model", {
    "value": ParamValueField
})


@api.route("/")
class ParamList(Resource):
    @api.marshal_with(param_list_model)
    def get(self):
        """ Returns the list of heat pump parameters with their current value. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s}".format(request.url))
        result = {}
        for name in HtParams.keys():
            value = ht_heatpump.get_param(name)
            result.update({name: value})
        return result

    @api.expect(param_list_model)
    @api.marshal_with(param_list_model)
    @api.response(404, "Parameter(s) not found")
    def put(self):
        """ Sets the current value of several heat pump parameters. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s} -- payload={!s}".format(request.url, api.payload))
        unknown = [name for name in api.payload.keys() if name not in HtParams]
        if unknown:
            api.abort(404, "Parameter(s) {} not found".format(
                ", ".join(map(lambda name: "{!r}".format(name), unknown))
            ))
        result = {}
        for name, value in api.payload.items():
            if not HTREST_READ_ONLY:
                value = ht_heatpump.set_param(name, value)
            result.update({name: value})
        return result


@api.route("/<string:name>")
@api.param("name", "The parameter name")
@api.response(404, "Parameter not found")
class Param(Resource):
    @api.marshal_with(param_model)
    def get(self, name: str):
        """ Returns the current value of a specific heat pump parameter. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        if name not in HtParams:
            api.abort(404, "Parameter '{}' not found".format(name))
        _logger.debug("*** {!s} -- name={!r}".format(request.url, name))
        value = ht_heatpump.get_param(name)
        return {"value": value}

    @api.expect(param_model)
    @api.marshal_with(param_model)
    def put(self, name: str):
        """ Sets the current value of a specific heat pump parameter. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        if name not in HtParams:
            api.abort(404, "Parameter '{}' not found".format(name))
        value = api.payload["value"]
        _logger.debug("*** {!s} -- name={!r}, value={}, type={}".format(request.url, name, value, type(value)))
        if not HTREST_READ_ONLY:
            value = ht_heatpump.set_param(name, value)
        return {"value": value}
