import socket
import sys

from nose.tools import eq_

if sys.version < '3':
    from mock import patch, Mock
else:
    from unittest.mock import patch, Mock


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


@patch('django_elastipymemcache.memcached.get_cluster_info')
def test_client_get_many(get_cluster_info):
    from django_elastipymemcache.memcached import ElastiPyMemCache

    servers = [('h1', 0), ('h2', 0)]
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiPyMemCache('h:0', {})
    ret = backend.get_many(['key1'])
    eq_(ret, {})

    # When server does not found...
    with patch('pymemcache.client.hash.HashClient._get_client') as p:
        p.return_value = None
        ret = backend.get_many(['key2'])
        eq_(ret, {})

    with patch('django_elastipymemcache.client.Client.get_many'), \
            patch('pymemcache.client.hash.HashClient._safely_run_func') as p2:
        p2.return_value = {
            ':1:key3': 1509111630.048594
        }

        ret = backend.get_many(['key3'])
        eq_(ret, {'key3': 1509111630.048594})

    # If False value is included, ignore it.
    with patch('pymemcache.client.hash.HashClient.get_many') as p:
        p.return_value = {
            ':1:key1': 1509111630.048594,
            ':1:key2': False,
            ':1:key3': 1509111630.058594,
        }
        ret = backend.get_many(['key1', 'key2', 'key3'])
        eq_(
            ret,
            {
                'key1': 1509111630.048594,
                'key3': 1509111630.058594
            },
        )

    with patch('pymemcache.client.hash.HashClient.get_many') as p:
        p.return_value = {
            ':1:key1': None,
            ':1:key2': 1509111630.048594,
            ':1:key3': False,
        }
        ret = backend.get_many(['key1', 'key2', 'key3'])
        eq_(
            ret,
            {
                'key2': 1509111630.048594,
            },
        )
