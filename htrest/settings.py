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

""" Settings for the Heliotherm heat pump REST API server. """


# Flask-RESTX settings
RESTX_SWAGGER_UI_DOC_EXPANSION = "list"
RESTX_VALIDATE = True
RESTX_MASK_SWAGGER = False
RESTX_ERROR_404_HELP = False
RESTX_BUNDLE_ERRORS = True

BOOL_AS_INT = False  # boolean values are treated as integers (with false equivalent to 0 and true equivalent to 1)
READ_ONLY = False  # no write accesses to the heat pump; if you want to be sure, that nothing will be manipulated
