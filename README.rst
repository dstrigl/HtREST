HtREST
======


.. image:: https://img.shields.io/pypi/v/htrest.svg
        :target: https://pypi.python.org/pypi/htrest

.. image:: https://img.shields.io/travis/dstrigl/htrest.svg
        :target: https://travis-ci.org/dstrigl/htrest

.. image:: https://pyup.io/repos/github/dstrigl/htrest/shield.svg
     :target: https://pyup.io/repos/github/dstrigl/htrest/
     :alt: Updates


`Heliotherm <http://www.heliotherm.com/>`_ heat pump REST API server.


* GitHub repo: https://github.com/dstrigl/HtREST
* Free software: `GNU General Public License v3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_


API
---

+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| URI                                           | GET | POST | description                                                                |
+===============================================+=====+======+============================================================================+
| /api/v1/device                                | X   |      | Delivers information about the connected heat pump.                        |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/datetime                              | X   |      | Returns the current date and time of the heat pump.                        |
|                                               +-----+------+----------------------------------------------------------------------------+
|                                               |     | X    | Sets the current date and time of the heat pump.                           |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/faultlist                             | X   |      | Returns the fault list of the heat pump.                                   |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/faultlist/size                        | X   |      | Returns the fault list size of the heat pump.                              |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/faultlist/<int:id>                    | X   |      | Returns the fault list entry with the given index.                         |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/faultlist/last                        | X   |      | Returns the last fault list entry of the heat pump.                        |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/timeprog                              | X   |      | Returns a list of all available time programs of the heat pump.            |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/timeprog/<int:id>                     | X   |      | Returns the time program with the given index of the heat pump.            |
|                                               +-----+------+----------------------------------------------------------------------------+
|                                               |     | X    | Sets all time program entries of a specific time program of the heat pump. |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/timeprog/<int:id>/<int:day>/<int:num> | X   |      | Returns a specific time program entry of the heat pump.                    |
|                                               +-----+------+----------------------------------------------------------------------------+
|                                               |     | X    | Sets a specific time program entry of the heat pump.                       |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/param                                 | X   |      | Returns the list of heat pump parameters with their current value.         |
|                                               +-----+------+----------------------------------------------------------------------------+
|                                               |     | X    | Sets the current value of several heat pump parameters.                    |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+
| /api/v1/param/<string:name>                   | X   |      | Returns the current value of a specific heat pump parameter.               |
|                                               +-----+------+----------------------------------------------------------------------------+
|                                               |     | X    | Sets the current value of a specific heat pump parameter.                  |
+-----------------------------------------------+-----+------+----------------------------------------------------------------------------+


GET /api/v1/device
~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/datetime
~~~~~~~~~~~~~~~~~~~~

  TODO


PUT /api/v1/datetime
~~~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/faultlist
~~~~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/faultlist/size
~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/faultlist/<int:id>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/faultlist/last
~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/timeprog
~~~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/timeprog/<int:id>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO


PUT /api/v1/timeprog/<int:id>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/timeprog/<int:id>/<int:day>/<int:num>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO


PUT /api/v1/timeprog/<int:id>/<int:day>/<int:num>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/param
~~~~~~~~~~~~~~~~~

  TODO


PUT /api/v1/param
~~~~~~~~~~~~~~~~~

  TODO


GET /api/v1/param/<string:name>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO


PUT /api/v1/param/<string:name>
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  TODO

