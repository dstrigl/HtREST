# History

## 0.1.11 (2022-02-27)

* Bumped `htheatpump` from `1.3.1` to `1.3.2`.
* Bumped `Flask` from `1.1.2` to `2.0.3`.
* Bumped `flask-restx` from `0.2.0` to `0.5.1`.
* Bumped `flake8` from `3.8.4` to `4.0.1`.
* Bumped `tox` from `3.21.3` to `3.24.5`.
* Bumped `mypy` from `0.800` to `0.931`.
* Bumped `coverage` from `5.4` to `6.3.2`.
* Bumped `pytest` from `6.2.2` to `7.0.1`.
* Bumped `pytest-mypy` from `0.8.0` to `0.9.1`.
* Bumped `pytest-cov` from `2.11.1` to `3.0.0`.

## 0.1.10 (2021-01-30)

* Updated README.
* Replaced Travis CI by GitHub Actions.
* Updated copyright statements.
* Python code reformatting using *Black* and *isort*.
* Bumped `htheatpump` from `1.2.4` to `1.3.1`.
* Dropped support for Python 3.5 and 3.6.

## 0.1.9 (2020-04-20)

* Fixed *flake8* errors.

## 0.1.8 (2020-04-20)

* Added support for Python 3.8.
* Bumped `htheatpump` from `1.2.3` to `1.2.4`.
* Some minor cleanup and improvements.
* Changed default port of the HtREST application to `8777`.
* Resource `/api/v1/param` and `/api/v1/fastquery` are now supports the possibility to request
  for a specific subset of parameters.
* Resource `/api/v1/fastquery` now also supports the possibility to treat boolean values as
  integers (arg `--bool-as-int`).
* Changed log statements to the form with the preferred and well-known `%s` (and `%d`, `%f`, etc.)
  string formatting indicators (due to performance reasons).

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
