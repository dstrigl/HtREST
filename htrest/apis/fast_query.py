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

""" REST API for fast query of heat pump parameters representing a 'MP' data point. """

import logging
from typing import Final

from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from htheatpump import HtParams

from .utils import DotKeyField, HtContext, ParamValueField, bool_as_int

_LOGGER: Final = logging.getLogger(__name__)

api: Final = Namespace(
    "fastquery",
    description="Fast query of heat pump parameters representing a 'MP' data point.",
)

wildcard: Final = fields.Wildcard(DotKeyField)
param_list_model: Final = api.model("param_list_model", {"*": wildcard})
param_model: Final = api.model("param_model", {"value": ParamValueField})


@api.route("/")
@api.response(404, "Parameter(s) not found")
@api.response(400, "Invalid parameter(s), doesn't represent a 'MP' data point")
class FastQueryList(Resource):
    @api.marshal_with(param_list_model)
    def get(self):
        """Performs a fast query of a subset or all heat pump parameters representing a 'MP' data point."""
        _LOGGER.info("*** [GET] %s", request.url)
        params = list(request.args.keys())
        unknown = [name for name in params if name not in HtParams]
        if unknown:
            api.abort(
                404,
                "Parameter(s) {} not found".format(", ".join(repr(name) for name in unknown)),
            )
        invalid = [name for name in params if HtParams[name].dp_type != "MP"]
        if invalid:
            api.abort(
                400,
                "Parameter(s) {} doesn't represent a 'MP' data point".format(
                    ", ".join(repr(name) for name in invalid)
                ),
            )
        if not params:
            params = [name for name, param in HtParams.items() if param.dp_type == "MP"]
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            res = current_app.ht_heatpump.fast_query(*params)  # type: ignore[attr-defined]
        for name, value in res.items():
            res[name] = bool_as_int(name, value)
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res


@api.route("/<string:name>")
@api.param("name", "The parameter name (which represents a 'MP' data point)")
@api.response(404, "Parameter not found")
class FastQuery(Resource):
    @api.marshal_with(param_model)
    def get(self, name: str):
        """Performs a fast query of a specific heat pump parameter which represents a 'MP' data point."""
        _LOGGER.info("*** [GET] %s -- name='%s'", request.url, name)
        if name not in HtParams:
            api.abort(404, "Parameter {!r} not found".format(name))
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            value = current_app.ht_heatpump.fast_query(name)  # type: ignore[attr-defined]
        res = {"value": bool_as_int(name, value[name])}
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res
