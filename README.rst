🤙 Calls
========

**Archived:** this project is no longer maintained, and no further
releases or fixes are planned. The code stays available as-is.
The documentation from before archiving is in the
`docs folder <https://github.com/ariebovenberg/calls/tree/cf8362d93d33e0db3de022de49beb241f6a8dd1d/docs>`_.

.. image:: https://img.shields.io/pypi/v/calls.svg?style=flat-square
   :target: https://pypi.python.org/pypi/calls

.. image:: https://img.shields.io/pypi/l/calls.svg?style=flat-square
   :target: https://pypi.python.org/pypi/calls

.. image:: https://img.shields.io/pypi/pyversions/calls.svg?style=flat-square
   :target: https://pypi.python.org/pypi/calls

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square
   :target: https://github.com/psf/black

Simple, typed, composable tools for callables. 
They're also good Python citizens with nice ``repr``, mypy support, and picklability.

Quickstart
----------

All utilities are directly importable.
See `the docs <https://github.com/ariebovenberg/calls/tree/cf8362d93d33e0db3de022de49beb241f6a8dd1d/docs>`_ for a complete overview.

.. code-block:: python

  >>> from calls import raises, always, identity, flip, pipe

Installation
------------

It's available on PyPI.

.. code-block:: bash

  pip install calls
