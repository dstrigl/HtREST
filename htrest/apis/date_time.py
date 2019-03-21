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
from datetime import datetime
from htrest import ht_heatpump


_logger = logging.getLogger(__name__)

api = Namespace("datetime", description="Operations related to the date and time of the heat pump")

date_time_model = api.model("date_time_model", {
    "datetime": fields.DateTime(dt_format="iso8601", description="current date and time of the heat pump",
                                required=True, example=datetime.now().isoformat()),
})

date_time_parser = reqparse.RequestParser()
date_time_parser.add_argument("datetime", type=str, location="json", help="current date and time of the heat pump")


@api.route("/")
class DateTime(Resource):
    @api.marshal_with(date_time_model)
    def get(self):
        """ Returns the current date and time of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.info("*** {!s}".format(request.url))
        dt, _ = ht_heatpump.get_date_time()
        return {"datetime": dt}

    @api.expect(date_time_model)
    @api.marshal_with(date_time_model)
    def put(self):
        """ Sets the current date and time of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.info("*** {!s}".format(request.url))
        args = date_time_parser.parse_args(strict=True)
        dt = args["datetime"]
        if not dt:  # if 'dt' is empty, use the current system time!
            dt = datetime.now()
        else:
            dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%f")
        dt, _ = ht_heatpump.set_date_time(dt)
        return {"datetime": dt}
