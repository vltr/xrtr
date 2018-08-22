========
``xrtr``
========

.. start-badges

.. image:: https://img.shields.io/pypi/status/xrtr.svg
    :alt: PyPI - Status
    :target: https://pypi.org/project/xrtr/

.. image:: https://img.shields.io/pypi/v/xrtr.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/xrtr/

.. image:: https://img.shields.io/pypi/pyversions/xrtr.svg
    :alt: Supported versions
    :target: https://pypi.org/project/xrtr/

.. image:: https://travis-ci.org/vltr/xrtr.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/vltr/xrtr

.. image:: https://readthedocs.org/projects/xrtr/badge/?style=flat
    :target: https://readthedocs.org/projects/xrtr
    :alt: Documentation Status

.. image:: https://codecov.io/github/vltr/xrtr/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/vltr/xrtr

.. end-badges

A generic string router based on a Radix Tree structure, (partially) Cython optimized for speed.

Documentation
=============

https://xrtr.readthedocs.io/en/latest/

Inspiration
===========

``xrtr`` is highly inspired in `Router <https://github.com/shiyanhui/Router>`_, by `shiyanhui <https://github.com/shiyanhui>`_.

License
=======

``xrtr`` is a free software distributed under the `MIT <https://choosealicense.com/licenses/mit/>`_ license, the same license as `Router's license <https://github.com/shiyanhui/Router#license>`_.

To Do
=====

- There is a LOT of room for improvement (specially when migrating the code to C and Cython *and* the fact this is my first project with Cython);
- Fix test coverage (and why is it not covering method declarations, as an example);
- Add Windows builds `using AppVeyor <https://packaging.python.org/guides/supporting-windows-using-appveyor/>`_;
