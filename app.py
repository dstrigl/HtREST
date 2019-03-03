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

import os
import logging.config
from htrest import create_app

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "logging.conf"))
logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)

def main():
    app = create_app()
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
