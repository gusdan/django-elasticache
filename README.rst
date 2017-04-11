=======================
django-elastipymemcache
=======================

:Info: Simple Django cache backend for Amazon ElastiCache (memcached based).
:Author: UNCOVER TRUTH Inc. <develop@uncovertruth.co.jp>
:Copyright: © UNCOVER TRUTH Inc.
:Date: 2017-04-11
:Version: 0.0.1

.. index: README
.. image:: https://travis-ci.org/uncovertruth/django-elastipymemcache.svg?branch=master
    :target: https://travis-ci.org/uncovertruth/django-elastipymemcache
.. image:: https://codecov.io/gh/uncovertruth/django-elastipymemcache/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/uncovertruth/django-elastipymemcache

Purpose
-------

Simple Django cache backend for Amazon ElastiCache (memcached based). It uses
`pymemcache <https://github.com/pinterest/pymemcache>`_ and sets up a connection to each
node in the cluster using
`auto discovery <http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/AutoDiscovery.html>`_.
Originally forked from `django-elasticache <https://github.com/gusdan/django-elasticache>`_.

Requirements
------------

* pymemcache
* Django>=1.8

Installation
------------

Get it from `pypix <http://pypi.python.org/pypi/django-elastipymemcache>`_::

    pip install django-elastipymemcache

Usage
-----

Your cache backend should look something like this::

    CACHES = {
        'default': {
            'BACKEND': 'django_elastipymemcache.memcached.ElastiPyMemCache',
            'LOCATION': '[configuration endpoint].com:11211',
        }
    }

Testing
-------

Run the tests like this::

    nosetests
