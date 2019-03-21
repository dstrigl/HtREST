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
from flask_restplus import Namespace, Resource, fields, reqparse
from htheatpump.htparams import HtDataTypes, HtParams
from htrest import ht_heatpump

_logger = logging.getLogger(__name__)


def dt_to_field(p):
    if p.data_type == HtDataTypes.STRING:
        return fields.String(required=True)
    elif p.data_type == HtDataTypes.BOOL:
        return fields.Boolean(required=True)
    elif p.data_type == HtDataTypes.INT:
        return fields.Integer(required=True, min=p.min_val, max=p.max_val, example=p.min_val)
    elif p.data_type == HtDataTypes.FLOAT:
        return fields.Float(required=True, min=p.min_val, max=p.max_val, example=p.min_val)
    assert False


api = Namespace("param", description="Operations related to the heat pump parameters")

param_models = {name: dt_to_field(param) for name, param in HtParams.items()}
param_list_model = api.model("param_list_model", param_models)
param_model = api.model("param_model", {
    "value": fields.Raw(required=True, description="parameter value")
})

param_value_parser = reqparse.RequestParser()
param_value_parser.add_argument("value", location="json", help="parameter value")


@api.route("/")
class ParamList(Resource):
    @api.marshal_with(param_list_model)
    def get(self):
        """ Returns the list of heat pump parameters with their current value. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        #assert ht_heatpump.is_open, "serial connection to heat pump not established"  # TODO
        _logger.info("*** {!s}".format(request.url))
        return {name: param.min_val for name, param in HtParams.items()}  # TODO


@api.route("/<string:name>")
@api.param("name", "The parameter name")
@api.response(404, "Parameter not found")
class Param(Resource):
    @api.marshal_with(param_model)
    def get(self, name):
        """ Returns the current value of a specific heat pump parameter. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        #assert ht_heatpump.is_open, "serial connection to heat pump not established"
        if name not in HtParams:
            api.abort(404, "Parameter '{}' not found".format(name))
        _logger.info("*** {!s} -- name={}".format(request.url, name))
        return {"value": 0}  # TODO

    @api.expect(param_model, validate=True)  # BUG validate=...
    @api.marshal_with(param_model)
    def put(self, name):
        """ TODO """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        #assert ht_heatpump.is_open, "serial connection to heat pump not established"
        if name not in HtParams:
            api.abort(404, "Parameter '{}' not found".format(name))
        args = param_value_parser.parse_args(strict=True)
        value = args["value"]
        _logger.info("*** {!s} -- name={}, value={!s}".format(request.url, name, value))
        return {"value": value}  # TODO
