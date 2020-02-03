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
from flask_restplus import Namespace, Resource, fields
from htheatpump.htparams import HtDataTypes, HtParams
from htrest import ht_heatpump  # type: ignore
from contextlib import contextmanager

_logger = logging.getLogger(__name__)


# Support 'dot' notation in model/field keys:
# -------------------------------------------
# Workaround by SteadBytes (https://github.com/SteadBytes):
#   https://github.com/noirbizarre/flask-restplus/issues/598#issuecomment-477650244
# Pull request:
#   https://github.com/noirbizarre/flask-restplus/pull/604
#
class DotKeyField(fields.Raw):
    """ Allows use of flask_restplus fields with '.' in key names. By default, '.'
    is used as a separator for accessing nested properties. Mixin prevents this,
    allowing fields to use '.' in the key names.

    Example of issue:

    .. code-block:: python

       >>> data = {"my.dot.field": 1234}
       >>> model = {"my.dot.field": fields.String}
       >>> marshal(data, model)
       {"my.dot.field": None}

    flask_restplus tries to fetch values for ``data['my']['dot']['field']`` instead
    of ``data['my.dot.field']`` which is the desired behaviour in this case.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def output(self, key, obj, **kwargs):
        key_map = {}
        transformed_obj = {}
        for k, v in obj.items():
            transformed_key = k.replace(".", "___")
            key_map[k] = transformed_key
            transformed_obj[transformed_key] = v
        # if self.attribute is set and contains '.' super().output() will
        # use '.' as a separator for nested access.
        # -> temporarily set to None to overcome this
        with self.toggle_attribute() as attribute:
            data = super().output(
                key_map[key if attribute is None else attribute], transformed_obj
            )
        return data

    @contextmanager
    def toggle_attribute(self):
        """ Context manager to temporarily set ``self.attribute`` to :const:`None`.

        Yields ``self.attribute`` before setting to :const:`None`.
        """
        attribute = self.attribute
        self.attribute = None
        yield attribute
        self.attribute = attribute


api = Namespace("param", description="Operations related to the heat pump parameters.")

wildcard = fields.Wildcard(DotKeyField(required=True, description="parameter value"))
param_list_model = api.model("param_list_model", {
    "*": wildcard
})
param_model = api.model("param_model", {
    "value": fields.Raw(required=True, description="parameter value")
})


@api.route("/")
class ParamList(Resource):
    @api.marshal_with(param_list_model)
    def get(self):
        """ Returns the list of heat pump parameters with their current value. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        #_logger.info("*** {!s}".format(request.url))
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
        _logger.info("*** {!s} -- payload={!s}".format(request.url, api.payload))  # TODO
        unknown = [name for name in api.payload.keys() if name not in HtParams]
        if unknown:
            api.abort(404, "Parameter(s) {} not found".format(
                ", ".join(map(lambda n: "{!r}".format(n), unknown))
            ))
        result = {}
        for name, value in api.payload.items():
            #value = ht_heatpump.set_param(name, value)  # TODO
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
        #_logger.info("*** {!s} -- name='{}'".format(request.url, name))
        value = ht_heatpump.get_param(name)
        return {"value": value}

    @api.expect(param_model, validate=False)  # TODO
    @api.marshal_with(param_model)
    def put(self, name: str):
        """ Sets the current value of a specific heat pump parameter. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        if name not in HtParams:
            api.abort(404, "Parameter '{}' not found".format(name))
        value = api.payload["value"]
        _logger.info("*** {!s} -- name='{}', value='{!s}', type='{!s}'".format(request.url, name, value, type(value)))
        #value = ht_heatpump.set_param(name, value)  # TODO
        return {"value": value}
