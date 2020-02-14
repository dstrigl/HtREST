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

""" REST API for operations related to the time programs of the heat pump. """

import logging
from flask import request
from flask_restx import Namespace, Resource, fields
from htheatpump.httimeprog import TimeProgram as HtTimeProg
from htheatpump.httimeprog import TimeProgEntry as HtTimeProgEntry
from htrest.app import ht_heatpump  # type: ignore
from htrest.settings import READ_ONLY as HTREST_READ_ONLY


_logger = logging.getLogger(__name__)

api = Namespace("timeprog", description="Operations related to the time programs of the heat pump.")

time_prog_model = api.model("time_prog_model", {
    "index": fields.Integer(min=0, description="index of the time program",
                            required=False, readonly=True, example=0),
    "name" : fields.String(description="name of the time program",
                           required=False, readonly=True, example="Warmwasser"),
    "ead"  : fields.Integer(min=0, description="number of entries a day of the time program",
                            required=False, readonly=True, example=7),
    "nos"  : fields.Integer(min=0, description="number of states of the time program",
                            required=False, readonly=True, example=3),
    "ste"  : fields.Integer(min=0, description="step-size in minutes of the time program",
                            required=False, readonly=True, example=15),
    "nod"  : fields.Integer(min=0, description="number of days of the time program",
                            required=False, readonly=True, example=7),
})

time_prog_entry_model = api.model("time_prog_entry_model", {
    "state": fields.Integer(min=0, description="state of the time program entry",
                            required=True, example=1),
    "start": fields.String(description="start-time of the time program entry",
                           required=True, example="09:45"),
    "end"  : fields.String(description="end-time of the time program entry",
                           required=True, example="11:15"),
})

time_prog_with_entries_model = api.clone("time_prog_with_entries_model", time_prog_model, {
    "entries": fields.List(
        fields.List(
            fields.Nested(time_prog_entry_model, required=True),
            required=True),
        required=True),
})


@api.route("/")
class TimeProgs(Resource):
    @api.marshal_list_with(time_prog_model, skip_none=True)
    def get(self):
        """ Returns a list of all available time programs of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s}".format(request.url))
        time_progs = ht_heatpump.get_time_progs()
        return [time_prog.as_json(with_entries=False) for time_prog in time_progs]


@api.route("/<int:id>")
@api.param("id", "The time program index")
class TimeProg(Resource):
    @api.marshal_with(time_prog_with_entries_model, skip_none=True)
    def get(self, id: int):
        """ Returns the time program with the given index of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s} -- id={}".format(request.url, id))
        time_prog = ht_heatpump.get_time_prog(id)
        return time_prog.as_json(with_entries=True)

    @api.expect(time_prog_with_entries_model, validate=True)
    @api.marshal_with(time_prog_with_entries_model)
    def put(self, id: int):
        """ Sets all time program entries of a specific time program of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s} -- id={}, payload={!s}".format(request.url, id, api.payload))
        time_prog = ht_heatpump.get_time_prog(id, with_entries=False).as_json(with_entries=False)
        time_prog.update({"entries": api.payload["entries"]})
        time_prog = HtTimeProg.from_json(time_prog)
        if not HTREST_READ_ONLY:
            time_prog = ht_heatpump.set_time_prog(time_prog)
        return time_prog.as_json(with_entries=True)


@api.route("/<int:id>/<int:day>/<int:num>")
@api.param("id", "The time program index")
@api.param("day", "The day of the time program entry (inside the specified time program)")
@api.param("num", "The number of the time program entry (of the specified day)")
class TimeProgEntry(Resource):
    @api.marshal_with(time_prog_entry_model)
    def get(self, id: int, day: int, num: int):
        """ Returns a specific time program entry of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s} -- id={}, day={}, num={}".format(request.url, id, day, num))
        entry = ht_heatpump.get_time_prog_entry(id, day, num)
        return entry.as_json()

    @api.expect(time_prog_entry_model, validate=True)
    @api.marshal_with(time_prog_entry_model)
    def put(self, id: int, day: int, num: int):
        """ Sets a specific time program entry of the heat pump. """
        assert ht_heatpump is not None, "'ht_heatpump' must not be None"
        assert ht_heatpump.is_open, "serial connection to heat pump not established"
        _logger.debug("*** {!s} -- id={}, day={}, num={}, payload={!s}".format(request.url, id, day, num, api.payload))
        entry = HtTimeProgEntry.from_json(api.payload)
        if not HTREST_READ_ONLY:
            entry = ht_heatpump.set_time_prog_entry(id, day, num, entry)
        return entry.as_json()
