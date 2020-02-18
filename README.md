# HtREST

[![PyPI version](https://img.shields.io/pypi/v/HtREST.svg)](https://pypi.org/project/HtREST)
[![Python versions](https://img.shields.io/pypi/pyversions/HtREST.svg)](https://pypi.org/project/HtREST)
[![Build status](https://img.shields.io/travis/dstrigl/HtREST?logo=travis)](https://travis-ci.org/dstrigl/HtREST)
[![Updates](https://pyup.io/repos/github/dstrigl/HtREST/shield.svg)](https://pyup.io/repos/github/dstrigl/HtREST)


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


## API

The following table describes the HTTP/REST API exposed by this server application for the
[Heliotherm](http://www.heliotherm.com/) heat pump.

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


### GET /api/v1/device

Delivers information about the connected heat pump.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/device/" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/device/
```

**Sample Response:**

```
{
  "property_id": 123456,
  "serial_number": 123456,
  "software_version": "3.0.20"
}
```


### GET /api/v1/datetime

Returns the current date and time of the heat pump.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/datetime/" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/datetime/
```

**Sample Response:**

```
{
  "datetime": "2020-01-29T13:11:35"
}
```


### PUT /api/v1/datetime

Sets the current date and time of the heat pump.

**Sample Payload:**

```
{
  "datetime": "2020-01-29T13:12:07"
}
```

*Remark: If "datetime" is empty current date and time of the host will be used.*

**Sample Curl:**

```
curl -X PUT "http://localhost:8888/api/v1/datetime/" -H "accept: application/json" -H "Content-Type: application/json" -d "{  \"datetime\": \"2020-01-29T13:12:07\"}"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/datetime/
```

**Sample Response:**

```
{
  "datetime": "2020-01-29T13:12:07"
}
```


### GET /api/v1/faultlist

Returns the fault list of the heat pump.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/faultlist/" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/faultlist/
```

**Sample Response:**

```
[
  {
    "index": 0,
    "error": 65534,
    "datetime": "2000-01-01T00:00:00",
    "message": "Keine Stoerung"
  },
  {
    "index": 1,
    "error": 65286,
    "datetime": "2000-01-01T00:00:00",
    "message": "Info: Programmupdate 1"
  },
  {
    "index": 2,
    "error": 65285,
    "datetime": "2000-01-01T00:00:00",
    "message": "Info: Initialisiert"
  },
  {
    "index": 3,
    "error": 19,
    "datetime": "2014-09-14T02:08:56",
    "message": "EQ_Spreizung"
  }
]
```


### GET /api/v1/faultlist/size

Returns the fault list size of the heat pump.

```
curl -X GET "http://localhost:8888/api/v1/faultlist/size" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/faultlist/size
```

**Sample Response:**

```
{
  "size": 4
}
```


### GET /api/v1/faultlist/\<int:id\>

Returns the fault list entry with the given index.

**Parameter:**

* **\<int:id\>**: The fault list index.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/faultlist/3" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/faultlist/3
```

**Sample Response:**

```
{
  "index": 3,
  "error": 19,
  "datetime": "2014-09-14T02:08:56",
  "message": "EQ_Spreizung"
}
```


### GET /api/v1/faultlist/last

Returns the last fault list entry of the heat pump.

```
curl -X GET "http://localhost:8888/api/v1/faultlist/last" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/faultlist/last
```

**Sample Response:**

```
{
  "index": 3,
  "error": 19,
  "datetime": "2014-09-14T02:08:56",
  "message": "EQ_Spreizung"
}
```


### GET /api/v1/timeprog

Returns a list of all available time programs of the heat pump.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/timeprog/" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/timeprog/
```

**Sample Response:**

```
[
  {
    "index": 0,
    "name": "Warmwasser",
    "ead": 7,
    "nos": 2,
    "ste": 15,
    "nod": 7
  },
  {
    "index": 1,
    "name": "Zirkulationspumpe",
    "ead": 7,
    "nos": 2,
    "ste": 15,
    "nod": 7
  },
  {
    "index": 2,
    "name": "Heizung",
    "ead": 7,
    "nos": 3,
    "ste": 15,
    "nod": 7
  },
  {...},
  {...}
]
```


### GET /api/v1/timeprog/\<int:id\>

Returns the time program with the given index of the heat pump.

**Parameter:**

* **\<int:id\>**: The time program index.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/timeprog/1" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/timeprog/1
```

**Sample Response:**

```
{
  "index": 1,
  "name": "Zirkulationspumpe",
  "ead": 7,
  "nos": 2,
  "ste": 15,
  "nod": 7,
  "entries": [
    [
      {
        "state": 0,
        "start": "00:00",
        "end": "05:15"
      },
      {
        "state": 1,
        "start": "05:15",
        "end": "08:00"
      },
      {...},
      {...},
      {...},
      {...},
      {...}
    ],
    [...],
    [...],
    [...],
    [...],
    [...],
    [...]
  ]
}
```


### PUT /api/v1/timeprog/\<int:id\>

Sets all time program entries of a specific time program of the heat pump.

**Parameter:**

* **\<int:id\>**: The time program index.

**Sample Payload:**

```
{
  "index": 1,
  "name": "Zirkulationspumpe",
  "ead": 7,
  "nos": 2,
  "ste": 15,
  "nod": 7,
  "entries": [
    [
      {
        "state": 0,
        "start": "00:00",
        "end": "06:00"
      },
      {
        "state": 1,
        "start": "06:00",
        "end": "09:00"
      },
      {...},
      {...},
      {...},
      {...},
      {...}
    ],
    [...],
    [...],
    [...],
    [...],
    [...],
    [...]
  ]
}
```

**Sample Curl:**

```
curl -X PUT "http://localhost:8888/api/v1/timeprog/1" -H "accept: application/json" -H "Content-Type: application/json" -d "{  \"index\": 1,  \"name\": \"Zirkulationspumpe\",  ... }"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/timeprog/1
```

**Sample Response:**

```
{
  "index": 1,
  "name": "Zirkulationspumpe",
  "ead": 7,
  "nos": 2,
  "ste": 15,
  "nod": 7,
  "entries": [
    [
      {
        "state": 0,
        "start": "00:00",
        "end": "06:00"
      },
      {
        "state": 1,
        "start": "06:00",
        "end": "09:00"
      },
      {...},
      {...},
      {...},
      {...},
      {...}
    ],
    [...],
    [...],
    [...],
    [...],
    [...],
    [...]
  ]
}
```


#### GET /api/v1/timeprog/\<int:id\>/\<int:day\>/\<int:num\>

Returns a specific time program entry of the heat pump.

**Parameter:**

* **\<int:num\>**: The number of the time program entry (of the specified day).
* **\<int:day\>**: The day of the time program entry (inside the specified time program).
* **\<int:id\>**:  The time program index.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/timeprog/1/1/1" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/timeprog/1/1/1
```

**Sample Response:**

```
{
  "state": 1,
  "start": "06:00",
  "end": "08:00"
}
```


### PUT /api/v1/timeprog/\<int:id\>/\<int:day\>/\<int:num\>

Sets a specific time program entry of the heat pump.

**Parameter:**

* **\<int:num\>**: The number of the time program entry (of the specified day).
* **\<int:day\>**: The day of the time program entry (inside the specified time program).
* **\<int:id\>**:  The time program index.

**Sample Payload:**

```
{
  "state": 1,
  "start": "06:00",
  "end": "08:00"
}
```

**Sample Curl:**

```
curl -X PUT "http://localhost:8888/api/v1/timeprog/1/1/1" -H "accept: application/json" -H "Content-Type: application/json" -d "{  \"state\": 1,  \"start\": \"06:00\",  \"end\": \"08:00\"}"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/timeprog/1/1/1
```

**Sample Response:**

```
{
  "state": 1,
  "start": "06:00",
  "end": "08:00"
}
```


### GET /api/v1/param

Returns the current value of all known heat pump parameters.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/param/" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/param/
```

**Sample Response:**

```
{
  "HKR Soll_Raum": 23,
  "Stoerung": false,
  "Temp. EQ_Austritt": 4.7,
  "Temp. EQ_Eintritt": 6.1,
  "Temp. Ruecklauf": 27.7,
  "Temp. Vorlauf": 27.8,
  "Temp. Brauchwasser": 50.1,
  "Temp. Aussen verzoegert": 4.9,
  "Temp. Aussen": 4.9,
  ...
}
```

*Remark: A list of available Heliotherm heat pump parameters can be found
[here](https://htheatpump.readthedocs.io/en/latest/htparams.html).*


### PUT /api/v1/param

Sets the current value of several heat pump parameters.

**Sample Payload:**

```
{
  "Betriebsart": 1,
  "HKR Soll_Raum": 21.5,
  "HKR Aufheiztemp. (K)": 3,
  "HKR Absenktemp. (K)": -3,
  "WW Minimaltemp.": 15,
  "WW Normaltemp.": 50
}
```

**Sample Curl:**

```
curl -X PUT "http://localhost:8888/api/v1/param/" -H "accept: application/json" -H "Content-Type: application/json" -d "{  \"Betriebsart\": 1,  \"HKR Soll_Raum\": 21.5,  ... }"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/param/
```

**Sample Response:**

```
{
  "Betriebsart": 1,
  "HKR Soll_Raum": 21.5,
  "HKR Aufheiztemp. (K)": 3,
  "HKR Absenktemp. (K)": -3,
  "WW Minimaltemp.": 15,
  "WW Normaltemp.": 50
}
```

*Remark: A list of available Heliotherm heat pump parameters can be found
[here](https://htheatpump.readthedocs.io/en/latest/htparams.html).*


### GET /api/v1/param/\<string:name\>

Returns the current value of a specific heat pump parameter.

**Parameter:**

* **\<string:name\>**: The parameter name.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/param/Temp.%20Aussen" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/param/Temp.%20Aussen
```

**Sample Response:**

```
{
  "value": 4.9
}
```

*Remark: A list of available Heliotherm heat pump parameters can be found
[here](https://htheatpump.readthedocs.io/en/latest/htparams.html).*


### PUT /api/v1/param/\<string:name\>

Sets the current value of a specific heat pump parameter.

**Parameter:**

* **\<string:name\>**: The parameter name.

**Sample Payload:**

```
{
  "value": 22.5
}
```

**Sample Curl:**

```
curl -X PUT "http://localhost:8888/api/v1/param/HKR%20Soll_Raum" -H "accept: application/json" -H "Content-Type: application/json" -d "{  \"value\": 22.5}"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/param/HKR%20Soll_Raum
```

**Sample Response:**

```
{
  "value": 22.5
}
```

*Remark: A list of available Heliotherm heat pump parameters can be found
[here](https://htheatpump.readthedocs.io/en/latest/htparams.html).*


### GET /api/v1/fastquery

Performs a fast query of all heat pump parameters representing a "MP" data point.

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/fastquery/" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/fastquery/
```

**Sample Response:**

```
{
  "HKR_Sollwert": 32.2,
  "Verdichteranforderung": 3,
  "Frischwasserpumpe": 0,
  "FWS Stroemungsschalter": false,
  "Stoerung": false,
  "Verdichter": true,
  "Zirkulationspumpe WW": false,
  ...
}
```

*Remark: A list of available Heliotherm heat pump parameters can be found
[here](https://htheatpump.readthedocs.io/en/latest/htparams.html).*


### GET /api/v1/fastquery/\<string:name\>

Performs a fast query of a specific heat pump parameter which represents a "MP" data point.

**Parameter:**

* **\<string:name\>**: The parameter name (representing a "MP" data point).

**Sample Curl:**

```
curl -X GET "http://localhost:8888/api/v1/fastquery/Verdichter" -H "accept: application/json"
```

**Sample Request URL:**

```
http://localhost:8888/api/v1/fastquery/Verdichter
```

**Sample Response:**

```
{
  "value": true
}
```

*Remark: A list of available Heliotherm heat pump parameters can be found
[here](https://htheatpump.readthedocs.io/en/latest/htparams.html).*


## Installation

You can install or upgrade `HtREST` with:

```
$ pip install HtREST --upgrade
```

Or you can install from source with:

```
$ git clone https://github.com/dstrigl/HtREST.git
$ cd HtREST
$ python setup.py install
```


## Usage

```
usage: htrest [-h] [-d DEVICE] [-b {9600,19200,38400,57600,115200}]
              [-s SERVER] [-u USER] [-l LOGGING_CONFIG] [--debug]

Heliotherm heat pump REST API server

optional arguments:
  -h, --help            show this help message and exit
  -d DEVICE, --device DEVICE
                        the serial device on which the heat pump is connected,
                        default: /dev/ttyUSB0
  -b {9600,19200,38400,57600,115200}, --baudrate {9600,19200,38400,57600,115200}
                        baudrate of the serial connection (same as configured
                        on the heat pump), default: 115200
  -s SERVER, --server SERVER
                        the name and port number of the server in the form
                        <hostname>:<port>, default: localhost:8888
  -u USER, --user USER  the username and password for the basic access
                        authentication in the form "<username>:<password>",
                        default:
  -l LOGGING_CONFIG, --logging-config LOGGING_CONFIG
                        the filename under which the logging configuration can
                        be found, default:
                        /home/pi/HtREST/htrest/logging.conf
  --debug               enable Flask debug mode, default: False
```


## Wanna support me?

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/default-orange.png)](https://www.buymeacoffee.com/N362PLZ)


## License

Distributed under the terms of the [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).
