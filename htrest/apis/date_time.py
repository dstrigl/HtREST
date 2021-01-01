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

""" REST API for operations related to the date and time of the heat pump. """

import logging
from datetime import datetime

from flask import request
from flask_restx import Namespace, Resource, fields

from .. import settings
from ..app import ht_heatpump
from .utils import HtContext

_LOGGER = logging.getLogger(__name__)

api = Namespace(
    "datetime", description="Operations related to the date and time of the heat pump."
)

date_time_model = api.model(
    "date_time_model",
    {
        "datetime": fields.DateTime(
            dt_format="iso8601",
            description="current date and time of the heat pump",
            required=True,
            example=datetime.now().replace(microsecond=0).isoformat(),
        ),
    },
)


@api.route("/")
class DateTime(Resource):
    @api.marshal_with(date_time_model)
    def get(self):
        """ Returns the current date and time of the heat pump. """
        _LOGGER.info("*** [GET] %s", request.url)
        with HtContext(ht_heatpump):
            dt, _ = ht_heatpump.get_date_time()
        res = {"datetime": dt}
        _LOGGER.debug("*** [GET] %s -> %s", request.url, res)
        return res

    @api.expect(date_time_model, validate=True)
    @api.marshal_with(date_time_model)
    def put(self):
        """Sets the current date and time of the heat pump.
        Note: If 'datetime' is empty current date and time of the host will be used.
        """
        _LOGGER.info(
            "*** [PUT%s] %s -- payload=%s",
            " (read-only)" if settings.READ_ONLY else "",
            request.url,
            api.payload,
        )
        dt = api.payload["datetime"]
        if not dt:  # if 'dt' is empty (or None), use the current system time!
            dt = datetime.now()
        else:
            dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        with HtContext(ht_heatpump):
            if not settings.READ_ONLY:
                dt, _ = ht_heatpump.set_date_time(dt)
        res = {"datetime": dt}
        _LOGGER.debug(
            "*** [PUT%s] %s -> %s",
            " (read-only)" if settings.READ_ONLY else "",
            request.url,
            res,
        )
        return res
