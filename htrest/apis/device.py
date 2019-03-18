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
from flask_restplus import Namespace, Resource, fields
from htrest import ht_heatpump
from htheatpump.htparams import HtParams


_logger = logging.getLogger(__name__)

api = Namespace("device", description="Delivers information about the connected heat pump")

device_model = api.model("device_model", {
    "property_id":      fields.Integer(min=0, description="property number of the heat pump",
                                       required=True, readonly=True, example=123456),  # TODO
    "serial_number":    fields.Integer(min=0, description="serial number of the heat pump",
                                       required=True, readonly=True, example=123456),  # TODO
    "software_version": fields.String(description="software version of the heat pump",
                                      required=True, readonly=True, example="3.0.20"),
    # ... TODO add some more properties?
})


@api.route("/")
class Device(Resource):
    @api.marshal_with(device_model)
    def get(self):
        """ Returns the properties of the heat pump. """
        assert ht_heatpump is not None
        _logger.info("*** {!s}".format(request.url))
        property_id = ht_heatpump.get_param("Liegenschaft") if "Liegenschaft" in HtParams else 0  # TODO
        serial_number = ht_heatpump.get_serial_number()
        software_version, _ = ht_heatpump.get_version()
        return {"property_id": property_id, "serial_number": serial_number, "software_version": software_version}
