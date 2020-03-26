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
from htheatpump.htparams import HtDataTypes, HtParams
from .utils import ParamValueField, DotKeyField, HtContext
from htrest.app import ht_heatpump
from htrest import settings


_logger = logging.getLogger(__name__)


api = Namespace("param", description="Operations related to the heat pump parameters.")

wildcard = fields.Wildcard(DotKeyField)
param_list_model = api.model("param_list_model", {"*": wildcard})
param_model = api.model("param_model", {"value": ParamValueField})


def bool_as_int(name, value):
    if settings.BOOL_AS_INT and HtParams[name].data_type == HtDataTypes.BOOL:
        value = 1 if value else 0
    return value


def int_as_bool(name, value):
    if settings.BOOL_AS_INT and HtParams[name].data_type == HtDataTypes.BOOL:
        value = True if value else False
    return value


@api.route("/")
class ParamList(Resource):
    @api.marshal_with(param_list_model)
    def get(self):
        """ Returns the list of heat pump parameters with their current value. """
        _logger.info("*** [GET] {!s}".format(request.url))
        with HtContext(ht_heatpump):
            res = {}
            for name in HtParams.keys():
                value = ht_heatpump.get_param(name)
                value = bool_as_int(name, value)
                res.update({name: value})
        return res

    @api.expect(param_list_model)
    @api.marshal_with(param_list_model)
    @api.response(404, "Parameter(s) not found")
    def put(self):
        """ Sets the current value of several heat pump parameters. """
        _logger.info(
            "*** [PUT{}] {!s} -- payload={!s}".format(
                " (read-only)" if settings.READ_ONLY else "", request.url, api.payload
            )
        )
        unknown = [name for name in api.payload.keys() if name not in HtParams]
        if unknown:
            api.abort(
                404,
                "Parameter(s) {} not found".format(
                    ", ".join(map(lambda name: "{!r}".format(name), unknown))
                ),
            )
        with HtContext(ht_heatpump):
            res = {}
            for name, value in api.payload.items():
                value = int_as_bool(name, value)
                if not settings.READ_ONLY:
                    value = ht_heatpump.set_param(name, value)
                value = bool_as_int(name, value)
                res.update({name: value})
        return res


@api.route("/<string:name>")
@api.param("name", "The parameter name")
@api.response(404, "Parameter not found")
class Param(Resource):
    @api.marshal_with(param_model)
    def get(self, name: str):
        """ Returns the current value of a specific heat pump parameter. """
        _logger.info("*** [GET] {!s} -- name={!r}".format(request.url, name))
        if name not in HtParams:
            api.abort(404, "Parameter '{}' not found".format(name))
        with HtContext(ht_heatpump):
            value = ht_heatpump.get_param(name)
            value = bool_as_int(name, value)
        return {"value": value}

    @api.expect(param_model)
    @api.marshal_with(param_model)
    def put(self, name: str):
        """ Sets the current value of a specific heat pump parameter. """
        _logger.info(
            "*** [PUT{}] {!s} -- name={!r}, payload={!s}".format(
                " (read-only)" if settings.READ_ONLY else "",
                request.url,
                name,
                api.payload,
            )
        )
        value = api.payload["value"]
        if name not in HtParams:
            api.abort(404, "Parameter '{}' not found".format(name))
        with HtContext(ht_heatpump):
            value = int_as_bool(name, value)
            if not settings.READ_ONLY:
                value = ht_heatpump.set_param(name, value)
            value = bool_as_int(name, value)
        return {"value": value}
