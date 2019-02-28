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
from flask import Flask
from htrest import settings
from apiv1 import blueprint as apiv1


logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../logging.conf"))
logging.config.fileConfig(logging_conf_path)
#log = logging.getLogger(__name__)


def configure_app(app):
    app.config["SERVER_NAME"] = settings.FLASK_SERVER_NAME
    app.config["SWAGGER_UI_DOC_EXPANSION"] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config["RESTPLUS_VALIDATE"] = settings.RESTPLUS_VALIDATE
    app.config["RESTPLUS_MASK_SWAGGER"] = settings.RESTPLUS_MASK_SWAGGER
    app.config["ERROR_404_HELP"] = settings.RESTPLUS_ERROR_404_HELP


#@app.before_first_request
#def before_first_request():
#    log.info("*** @app.before_first_request")


def main():
    app = Flask(__name__)
    configure_app(app)
    app.register_blueprint(apiv1)
    #log.info(">>>>> Starting server @ http://{}/ <<<<<".format(app.config["SERVER_NAME"]))
    app.run(debug=settings.FLASK_DEBUG, use_reloader=False)
    #app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
