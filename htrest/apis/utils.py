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

""" Miscellaneous helper functions and classes for the REST API. """

from contextlib import contextmanager

from flask_restx import fields
from htheatpump import HtDataTypes, HtParams

from .. import settings


class HtContext:
    """Context manager for auto login/logout on the heat pump.

    Example:

    >>> with HtContext(ht_heatpump):
    ...     print(ht_heatpump.get_version())
    ...
    >>>
    """

    def __init__(self, heatpump):
        assert heatpump is not None, "'ht_heatpump' must not be None"
        assert heatpump.is_open, "serial connection to heat pump not established"
        self._heatpump = heatpump

    @property
    def heatpump(self):
        """Return the passed :class:`HtHeatpump` instance of the context manager.

        :returns: The passed :class:`HtHeatpump` instance.
        :rtype: ``HtHeatpump``
        """
        return self._heatpump

    def __enter__(self):
        self._heatpump.login()  # Hint: login() will also try a reconnect on failure
        return self

    def __exit__(self, *args):
        self._heatpump.logout()


class ParamValueField(fields.Raw):
    __schema_type__ = ["number", "boolean"]
    __schema_example__ = "number or boolean"

    def __init__(self):
        super().__init__(required=True, description="parameter value")


# Support 'dot' notation in model/field keys:
# -------------------------------------------
# Workaround by SteadBytes (https://github.com/SteadBytes):
#   https://github.com/noirbizarre/flask-restplus/issues/598#issuecomment-477650244
# Pull request:
#   https://github.com/noirbizarre/flask-restplus/pull/604
#
class DotKeyField(ParamValueField):
    """Allows use of flask_restx fields with '.' in key names. By default, '.'
    is used as a separator for accessing nested properties. Mixin prevents this,
    allowing fields to use '.' in the key names.

    Example of issue:

    .. code-block:: python

       >>> data = {"my.dot.field": 1234}
       >>> model = {"my.dot.field": fields.String}
       >>> marshal(data, model)
       {"my.dot.field": None}

    flask_restx tries to fetch values for ``data['my']['dot']['field']`` instead
    of ``data['my.dot.field']`` which is the desired behaviour in this case.
    """

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
        """Context manager to temporarily set ``self.attribute`` to :const:`None`.

        Yields ``self.attribute`` before setting to :const:`None`.
        """
        attribute = self.attribute
        self.attribute = None
        yield attribute
        self.attribute = attribute


def bool_as_int(name, value):
    """ Convert a boolean value to an integer, if desired (:const:`False` = 0, :const:`True` = 1). """
    if settings.BOOL_AS_INT and HtParams[name].data_type == HtDataTypes.BOOL:
        value = 1 if value else 0
    return value


def int_as_bool(name, value):
    """ Convert an integer value to a boolean, if desired (``0`` = :const:`False`, anything else :const:`True`). """
    if settings.BOOL_AS_INT and HtParams[name].data_type == HtDataTypes.BOOL:
        value = True if value else False
    return value
