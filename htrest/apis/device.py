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

""" REST API which delivers information about the connected heat pump. """

import logging
from typing import Final

from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from htheatpump import HtParams

from .utils import HtContext

_LOGGER: Final = logging.getLogger(__name__)

api: Final = Namespace("device", description="Delivers information about the connected heat pump.")

device_model: Final = api.model(
    "device_model",
    {
        "property_id": fields.Integer(
            min=0,
            description="property number of the heat pump",
            required=False,
            readonly=True,
            example=123456,
        ),
        "serial_number": fields.Integer(
            min=0,
            description="serial number of the heat pump",
            required=True,
            readonly=True,
            example=123456,
        ),
        "software_version": fields.String(
            description="software version of the heat pump",
            required=True,
            readonly=True,
            example="3.0.20",
        ),
    },
)


@api.route("/")
class Device(Resource):
    @api.marshal_with(device_model)
    def get(self):
        """Returns the properties of the heat pump."""
        _LOGGER.info("*** [GET] %s", request.url)
        with HtContext(current_app.ht_heatpump):  # type: ignore[attr-defined]
            serial_number = current_app.ht_heatpump.get_serial_number()  # type: ignore[attr-defined]
            software_version, _ = current_app.ht_heatpump.get_version()  # type: ignore[attr-defined]
            res = {"serial_number": serial_number, "software_version": software_version}
            if "Liegenschaft" in HtParams:
                property_id = current_app.ht_heatpump.get_param("Liegenschaft")  # type: ignore[attr-defined]
                res.update({"property_id": property_id})
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res
