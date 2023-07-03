#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  HtREST - Heliotherm heat pump REST API
#  Copyright (C) 2023  Daniel Strigl

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
from typing import Final

from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from htheatpump import HtParams

from .. import settings
from .utils import DotKeyField, HtContext, ParamValueField, bool_as_int, int_as_bool

_LOGGER: Final = logging.getLogger(__name__)

api: Final = Namespace("param", description="Operations related to the heat pump parameters.")

wildcard: Final = fields.Wildcard(DotKeyField)
param_list_model: Final = api.model("param_list_model", {"*": wildcard})
param_model: Final = api.model("param_model", {"value": ParamValueField})


@api.route("/")
class ParamList(Resource):
    @api.marshal_with(param_list_model)
    @api.response(404, "Parameter(s) not found")
    def get(self):
        """Returns a subset or complete list of the known heat pump parameters with their current value."""
        _LOGGER.info("*** [GET] %s", request.url)
        params = list(request.args.keys())
        unknown = [name for name in params if name not in HtParams]
        if unknown:
            api.abort(
                404,
                "Parameter(s) {} not found".format(", ".join(repr(name) for name in unknown)),
            )
        if not params:
            params = list(HtParams.keys())
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            res = {}
            for name in params:
                value = current_app.ht_heatpump.get_param(name)  # type: ignore[attr-defined]
                res.update({name: bool_as_int(name, value)})
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res

    @api.expect(param_list_model)
    @api.marshal_with(param_list_model)
    @api.response(404, "Parameter(s) not found")
    def put(self):
        """Sets the current value of several heat pump parameters."""
        _LOGGER.info(
            "*** [PUT%s] %s -- payload=%s",
            " (read-only)" if settings.READ_ONLY else "",
            request.url,
            api.payload,
        )
        unknown = [name for name in api.payload.keys() if name not in HtParams]
        if unknown:
            api.abort(
                404,
                "Parameter(s) {} not found".format(", ".join(repr(name) for name in unknown)),
            )
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            res = {}
            for name, value in api.payload.items():
                value = int_as_bool(name, value)
                if not settings.READ_ONLY:
                    value = current_app.ht_heatpump.set_param(name, value)  # type: ignore[attr-defined]
                res.update({name: bool_as_int(name, value)})
        _LOGGER.debug(
            "*** [PUT%s] %s -> %s",
            " (read-only)" if settings.READ_ONLY else "",
            request.url,
            res,
        )
        return res


@api.route("/<string:name>")
@api.param("name", "The parameter name")
@api.response(404, "Parameter not found")
class Param(Resource):
    @api.marshal_with(param_model)
    def get(self, name: str):
        """Returns the current value of a specific heat pump parameter."""
        _LOGGER.info("*** [GET] %s -- name='%s'", request.url, name)
        if name not in HtParams:
            api.abort(404, "Parameter {!r} not found".format(name))
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            value = current_app.ht_heatpump.get_param(name)  # type: ignore[attr-defined]
        res = {"value": bool_as_int(name, value)}
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res

    @api.expect(param_model)
    @api.marshal_with(param_model)
    def put(self, name: str):
        """Sets the current value of a specific heat pump parameter."""
        _LOGGER.info(
            "*** [PUT%s] %s -- name='%s', payload=%s",
            " (read-only)" if settings.READ_ONLY else "",
            request.url,
            name,
            api.payload,
        )
        if name not in HtParams:
            api.abort(404, "Parameter {!r} not found".format(name))
        value = api.payload["value"]
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            value = int_as_bool(name, value)
            if not settings.READ_ONLY:
                value = current_app.ht_heatpump.set_param(name, value)  # type: ignore[attr-defined]
        res = {"value": bool_as_int(name, value)}
        _LOGGER.debug(
            "*** [PUT%s] %s -> %s",
            " (read-only)" if settings.READ_ONLY else "",
            request.url,
            res,
        )
        return res
