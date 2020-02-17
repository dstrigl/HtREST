[![PyPI version](https://img.shields.io/pypi/v/HtREST.svg)](https://pypi.python.org/pypi/HtREST)
[![Build status](https://img.shields.io/travis/dstrigl/HtREST.svg)](https://travis-ci.org/dstrigl/HtREST)
[![Updates](https://pyup.io/repos/github/dstrigl/HtREST/shield.svg)](https://pyup.io/repos/github/dstrigl/HtREST)


HtREST
======

[Heliotherm](http://www.heliotherm.com/) heat pump HTTP/REST API server for Python 3.5, 3.6 and 3.7.

* GitHub repo: https://github.com/dstrigl/HtREST
* Free software: [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

> **Warning:**
>
> Please note that any incorrect or careless usage of this application as well as
> errors in the implementation can damage your heat pump!
>
> Therefore, the author does not provide any guarantee or warranty concerning
> to correctness, functionality or performance and does not accept any liability
> for damage caused by this application, examples or mentioned information.
>
> **Thus, use it on your own risk!**


API
---

The following table describes the HTTP/REST API exposed by this server application for the Heliotherm heat pump.

| URI                                             | GET   | POST  | description                                                                                 |
| :---------------------------------------------- | :---: | :---: | :------------------------------------------------------------------------------------------ |
| `/api/v1/device`                                |   X   |       | Delivers information about the connected heat pump.                                         |
| `/api/v1/datetime`                              |   X   |   X   | Returns or sets the current date and time of the heat pump.                                 |
| `/api/v1/faultlist`                             |   X   |       | Returns the fault list of the heat pump.                                                    |
| `/api/v1/faultlist/size`                        |   X   |       | Returns the fault list size of the heat pump.                                               |
| `/api/v1/faultlist/<int:id>`                    |   X   |       | Returns the fault list entry with the given index.                                          |
| `/api/v1/faultlist/last`                        |   X   |       | Returns the last fault list entry of the heat pump.                                         |
| `/api/v1/timeprog`                              |   X   |       | Returns a list of all available time programs of the heat pump.                             |
| `/api/v1/timeprog/<int:id>`                     |   X   |   X   | Returns or sets the time program with the given index of the heat pump.                     |
| `/api/v1/timeprog/<int:id>/<int:day>/<int:num>` |   X   |   X   | Returns or sets a specific time program entry of the heat pump.                             |
| `/api/v1/param`                                 |   X   |   X   | Returns or sets the current value of several heat pump parameters.                          |
| `/api/v1/param/<string:name>`                   |   X   |   X   | Returns or sets the current value of a specific heat pump parameter.                        |
| `/api/v1/fastquery`                             |   X   |       | Performs a fast query of all heat pump parameters representing a 'MP' data point.           |
| `/api/v1/fastquery/<string:name>`               |   X   |       | Performs a fast query of a specific heat pump parameter which represents a 'MP' data point. |














Wanna support me?
-----------------

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/default-orange.png)](https://www.buymeacoffee.com/N362PLZ)
