Amazon ElastiCache backend for Django
=====================================

Simple Django cache backend for Amazon ElastiCache (memcached based). It uses
`pylibmc <http://github.com/lericson/pylibmc>`_ and sets up a connection to each
node in the cluster using
`auto discovery <http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/AutoDiscovery.html>`_.


Requirements
------------

* pylibmc
* Django 1.5+.

It was written and tested on Python 2.7 and 3.4.

Installation
------------

Get it from `pypi <http://pypi.python.org/pypi/django-elasticache>`_::

    pip install django-elasticache

or `github <http://github.com/gusdan/django-elasticache>`_::

    pip install -e git://github.com/gusdan/django-elasticache.git#egg=django-elasticache


Usage
-----

Your cache backend should look something like this::

    CACHES = {
        'default': {
            'BACKEND': 'django_elasticache.memcached.ElastiCache',
            'LOCATION': 'cache-c.draaaf.cfg.use1.cache.amazonaws.com:11211',
            'OPTIONS': {
                'IGNORE_CLUSTER_ERRORS': [True,False],
            },
        }
    }

By the first call to cache it connects to cluster (using ``LOCATION`` param),
gets list of all nodes and setup pylibmc client using full
list of nodes. As result your cache will work with all nodes in cluster and
automatically detect new nodes in cluster. List of nodes are stored in class-level
cached, so any changes in cluster take affect only after restart of working process.
But if you're using gunicorn or mod_wsgi you usually have max_request settings which
restart process after some count of processed requests, so auto discovery will work
fine.

The ``IGNORE_CLUSTER_ERRORS`` option is useful when ``LOCATION`` doesn't have support
for ``config get cluster``. When set to ``True``, and ``config get cluster`` fails,
it returns a list of a single node with the same endpoint supplied to ``LOCATION``.

Django-elasticache changes default pylibmc params to increase performance.

Another solutions
-----------------

ElastiCache provides memcached interface so there are three solution of using it:

1. Memcached configured with location = Configuration Endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this case your application
will randomly connect to nodes in cluster and cache will be used with not optimal
way. At some moment you will be connected to first node and set item. Minute later
you will be connected to another node and will not able to get this item.

 ::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': 'cache.gasdbp.cfg.use1.cache.amazonaws.com:11211',
        }
    }


2. Memcached configured with all nodes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It will work fine, memcache client will
separate items between all nodes and will balance loading on client side. You will
have problems only after adding new nodes or delete old nodes. In this case you should
add new nodes manually and don't forget update your app after all changes on AWS.

 ::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'LOCATION': [
                'cache.gqasdbp.0001.use1.cache.amazonaws.com:11211',
                'cache.gqasdbp.0002.use1.cache.amazonaws.com:11211',
            ]
        }
    }


3. Use django-elasticache
~~~~~~~~~~~~~~~~~~~~~~~~~

It will connect to cluster and retrieve ip addresses
of all nodes and configure memcached to use all nodes.

 ::

    CACHES = {
        'default': {
            'BACKEND': 'django_elasticache.memcached.ElastiCache',
            'LOCATION': 'cache-c.draaaf.cfg.use1.cache.amazonaws.com:11211',
        }
    }


Difference between setup with nodes list (django-elasticache) and
connection to only one configuration Endpoint (using dns routing) you can see on
this graph:

.. image:: https://raw.github.com/gusdan/django-elasticache/master/docs/images/get%20operation%20in%20cluster.png

Testing
-------

Run the tests like this::

    nosetests
