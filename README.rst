=======================
django-elastipymemcache
=======================

:Info: Simple Django cache backend for Amazon ElastiCache (memcached based).
:Author: UNCOVER TRUTH Inc. <develop@uncovertruth.co.jp>
:Copyright: © UNCOVER TRUTH Inc.
:Date: 2018-06-19
:Version: 1.2.0

.. index: README
.. image:: https://travis-ci.org/uncovertruth/django-elastipymemcache.svg?branch=master
    :target: https://travis-ci.org/uncovertruth/django-elastipymemcache
.. image:: https://codecov.io/gh/uncovertruth/django-elastipymemcache/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/uncovertruth/django-elastipymemcache
.. image:: https://requires.io/github/uncovertruth/django-elastipymemcache/requirements.svg?branch=master
    :target: https://requires.io/github/uncovertruth/django-elastipymemcache/requirements/?branch=master
.. image:: https://badge.fury.io/py/django-elastipymemcache.svg
    :target: https://badge.fury.io/py/django-elastipymemcache

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
* Django>=1.11

Installation
------------

Get it from `pypi <http://pypi.python.org/pypi/django-elastipymemcache>`_::

    pip install django-elastipymemcache

Usage
-----

Your cache backend should look something like this::

    CACHES = {
        'default': {
            'BACKEND': 'django_elastipymemcache.memcached.ElastiPyMemCache',
            'LOCATION': '[configuration endpoint]:11211',
            'OPTIONS': {
              'cluster_timeout': 1, # its used when get cluster info
              'ignore_exc': True, # pymemcache Client params
              'ignore_cluster_errors': True, # ignore get cluster info error
            }
        }
    }

Testing
-------

Run the tests like this::

    nosetests
