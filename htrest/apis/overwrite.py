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

""" REST API for operations related to the heat pump parameters. """

import logging

from flask import request
from flask_restx import Namespace, Resource
from htheatpump import HtParams

from .. import settings
from ..app import ht_heatpump
from .utils import HtContext, NullableParamValueField, bool_as_int, int_as_bool

_LOGGER = logging.getLogger(__name__)


api = Namespace("overwrite", description="Operations related to manual overwrite heat pump parameters.")

nullable_param_model = api.model("nullable_param_model", {"value": NullableParamValueField})


@api.route("/<string:name>")
@api.param("name", "The parameter name")
@api.response(404, "Parameter not found")
class Overwrite(Resource):
    @api.expect(nullable_param_model)
    @api.marshal_with(nullable_param_model)
    def put(self, name: str):
        """ Manual overwrite the current value of a specific heat pump parameter. """
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
        with HtContext(ht_heatpump):
            if value is not None:
                value = int_as_bool(name, value)
            if not settings.READ_ONLY:
                value = ht_heatpump.overwrite_param(name, value)
        res = {"value": bool_as_int(name, value) if value is not None else value}
        _LOGGER.debug(
            "*** [PUT%s] %s -> %s",
            " (read-only)" if settings.READ_ONLY else "",
            request.url,
            res,
        )
        return res
