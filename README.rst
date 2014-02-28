Amazon ElastiCache backend for Django
=====================================

Simple Django cache backend for Amazon ElastiCache (memcached based). It uses
`pylibmc <http://github.com/lericson/pylibmc>`_ and setup connection to each
node in cluster using
`Auto Discovery <http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/AutoDiscovery.html>`_
function.


Requirements
------------

* pylibmc
* Django 1.3+.

It was written and tested on Python 2.7.

Installation
------------

Get it from `pypi <http://pypi.python.org/pypi/django-elasticache>`_::

    pip install django-pylibmc

or `github <http://github.com/gusdan/django-elasticache>`_::

    pip install -e git://github.com/gusdan/django-elasticache.git#egg=django-elasticache


Usage
-----

Your cache backend should look something like this::

    CACHES = {
        'default': {
            'BACKEND': 'django_elasticache.memcached.ElasctiCache',
            'LOCATION': 'cache-c.drtgf.cfg.use1.cache.amazonaws.com:11211',
        }
    }

By the first call to cache it connect to cluster (using LOCATION),
get list of all nodes and setup pylibmc client using full
list of nodes. As result your cache will work with all nodes and
automatically detect new nodes in cluster. List of nodes are stored in class-level
cached, so any changes in cluster take affect only after restart working process.
But if you're using gunicorn or mod_wsgi you usually have max_request settings which
restart process after some count of processed requests.

Django-elascticache changes default pylibmc params to increase performance.


Testing
-------

Run the tests like this::

    nosetest