import socket
import sys

from django.conf import global_settings, settings
from nose.tools import eq_

if sys.version < '3':
    from mock import patch, Mock
else:
    from unittest.mock import patch, Mock


# Initialize django 1.7
settings.configure()
global_settings.configured = True


@patch('django.conf.settings', global_settings)
@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_split_servers(get_cluster_info):
    from django_elastipymemcache.memcached import (
        ElastiPyMemCache,
        deserialize_pickle,
        serialize_pickle,
    )
    backend = ElastiPyMemCache('h:0', {})
    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }
    backend._lib.Client = Mock()
    assert backend._cache
    get_cluster_info.assert_called_once_with(
            'h', '0', False, socket._GLOBAL_DEFAULT_TIMEOUT)
    backend._lib.Client.assert_called_once_with(
        servers,
        deserializer=deserialize_pickle,
        ignore_exc=True,
        serializer=serialize_pickle
    )


@patch('django.conf.settings', global_settings)
@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_node_info_cache(get_cluster_info):
    from django_elastipymemcache.memcached import (
        ElastiPyMemCache,
        deserialize_pickle,
        serialize_pickle,
    )
    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    backend._lib.Client = Mock()
    backend.set('key1', 'val')
    backend.get('key1')
    backend.set('key2', 'val')
    backend.get('key2')
    backend._lib.Client.assert_called_once_with(
        servers,
        deserializer=deserialize_pickle,
        ignore_exc=True,
        serializer=serialize_pickle
    )
    eq_(backend._cache.get.call_count, 2)
    eq_(backend._cache.set.call_count, 2)

    get_cluster_info.assert_called_once_with(
            'h', '0', False, socket._GLOBAL_DEFAULT_TIMEOUT)


@patch('django.conf.settings', global_settings)
@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_invalidate_cache(get_cluster_info):
    from django_elastipymemcache.memcached import ElastiPyMemCache
    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    backend._lib.Client = Mock()
    assert backend._cache
    backend._cache.get = Mock()
    backend._cache.get.side_effect = Exception()
    try:
        backend.get('key1', 'val')
    except Exception:
        pass
    #  invalidate cached client
    container = getattr(backend, '_local', backend)
    container._client = None
    try:
        backend.get('key1', 'val')
    except Exception:
        pass
    eq_(backend._cache.get.call_count, 2)
    eq_(get_cluster_info.call_count, 3)
