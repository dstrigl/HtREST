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

""" REST API which delivers information about the connected heat pump. """

import logging
from flask import request
from flask_restx import Namespace, Resource, fields
from htheatpump.htparams import HtParams
from htrest.app import ht_heatpump  # type: ignore


_logger = logging.getLogger(__name__)

api = Namespace("device", description="Delivers information about the connected heat pump.")

device_model = api.model("device_model", {
    "property_id":      fields.Integer(min=0, description="property number of the heat pump",
                                       required=False, readonly=True, example=123456),
    "serial_number":    fields.Integer(min=0, description="serial number of the heat pump",
                                       required=True, readonly=True, example=123456),
    "software_version": fields.String(description="software version of the heat pump",
                                      required=True, readonly=True, example="3.0.20"),
})


@api.route("/")
class Device(Resource):
    @api.marshal_with(device_model)
    def get(self):
        """ Returns the properties of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s}".format(request.url))
        serial_number = ht_heatpump.get_serial_number()
        software_version, _ = ht_heatpump.get_version()
        res = {"serial_number": serial_number, "software_version": software_version}
        if "Liegenschaft" in HtParams:
            property_id = ht_heatpump.get_param("Liegenschaft")
            res.update({"property_id": property_id})
        return res
