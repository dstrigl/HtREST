# History

## 0.1.7 (2020-04-01)

* Fixed wrong uploaded package on PyPi.

## 0.1.6 (2020-03-31)

* Updated to `htheatpump v1.2.3`, which now includes several helper scripts (e.g. `htcomplparams`).
* Added possibility to disable all parameter verification actions (arg `--no-param-verification`).
* Changed behaviour: No reconnect of the serial connection will be performed for each request,
  because each `login()` call during a request will automatically try a reconnect on failure.
* Clean-up of `setup.py` and `MANIFEST.in`.

## 0.1.5 (2020-03-29)

* Adapted logging statements and default log levels.
* Python code reformatting using *Black*.
* Added possibility so that boolean values can be treated as integers (arg `--bool-as-int`).
* Fixed unsynchronized access to `HtHeatpump`, which results in a serial communication error.
* Changed package requirements structure; some changes in `setup.py`, `setup.cfg`, `tox.ini`, etc.

## 0.1.4 (2020-03-17)

* Fixed wrong uploaded package on PyPi.

## 0.1.3 (2020-03-17)

* Fixed missing file `logging.conf`.
* Corrected usage of host and port for the web server.

## 0.1.2 (2020-02-18)

* Fixed wrong version definition.

## 0.1.1 (2020-02-18)

* Fixed some errors in the project packaging.

## 0.1.0 (2020-02-18)

* First release on PyPI.
