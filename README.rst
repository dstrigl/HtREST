HtREST
======


.. image:: https://img.shields.io/pypi/v/htrest.svg
        :target: https://pypi.python.org/pypi/htrest

.. image:: https://img.shields.io/travis/dstrigl/htrest.svg
        :target: https://travis-ci.org/dstrigl/htrest

.. image:: https://pyup.io/repos/github/dstrigl/htrest/shield.svg
     :target: https://pyup.io/repos/github/dstrigl/htrest/
     :alt: Updates


`Heliotherm <http://www.heliotherm.com/>`_ heat pump REST API server


* GitHub repo: https://github.com/dstrigl/HtREST
* Free software: `GNU General Public License v3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_


API
---

+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| URI                                           | GET | POST | description                                                     |
+===============================================+=====+======+=================================================================+
| /api/v1/device                                | X   |      | Delivers information about the connected heat pump.             |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/datetime                              | X   | X    |                                                                 |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/faultlist                             | X   |      | Returns the fault list of the heat pump.                        |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/faultlist/size                        | X   |      | Returns the fault list size of the heat pump.                   |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/faultlist/<int:id>                    | X   |      | Returns the fault list entry with the given index.              |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/faultlist/last                        | X   |      | Returns the last fault list entry of the heat pump.             |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/timeprog                              | X   |      | Returns a list of all available time programs of the heat pump. |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/timeprog/<int:id>                     | X   | X    |                                                                 |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/timeprog/<int:id>/<int:day>/<int:num> | X   | X    |                                                                 |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/param                                 | X   | X    |                                                                 |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
| /api/v1/param/<string:name>                   | X   | X    |                                                                 |
+-----------------------------------------------+-----+------+-----------------------------------------------------------------+
