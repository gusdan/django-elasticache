# django-elastipymemcache

This project is forked [django-elasticache](https://github.com/gusdan/django-elasticache)

Simple Django cache backend for Amazon ElastiCache (memcached based). It uses
[pymemcache](https://github.com/pinterest/pymemcache>) and sets up a connection to each
node in the cluster using
[auto discovery](http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/AutoDiscovery.html>)


## Requirements

* pymemcache
* Django 1.7+.

It was written and tested on Python 2.7 and 3.5.

## Installation

Get it from [pypi](http://pypi.python.org/pypi/django-elastipymemcache)

```bash
pip install django-elastipymemcache
```

## Usage

Your cache backend should look something like this

```python
CACHES = {
    'default': {
        'BACKEND': 'django_elastipymemcache.memcached.ElastiPyMemCache',
        'LOCATION': '[configuration endpoint].com:11211',
        'OPTIONS' {
            'IGNORE_CLUSTER_ERRORS': [True,False],
        },
    }
}
```

## Testing

Run the tests like this

```bash
nosetests
```
