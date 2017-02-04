from django.conf import global_settings, settings
from nose.tools import eq_, raises
import sys
if sys.version < '3':
    from mock import patch, Mock
else:
    from unittest.mock import patch, Mock


# Initialize django 1.7
settings.configure()
global_settings.configured = True


@patch('django.conf.settings', global_settings)
def test_patch_params():
    from django_elasticache.memcached import ElastiCache
    params = {}
    ElastiCache('qew:12', params)
    eq_(params['BINARY'], True)
    eq_(params['OPTIONS']['tcp_nodelay'], True)
    eq_(params['OPTIONS']['ketama'], True)


@raises(Exception)
@patch('django.conf.settings', global_settings)
def test_wrong_params():
    from django_elasticache.memcached import ElastiCache
    ElastiCache('qew', {})


@raises(Warning)
@patch('django.conf.settings', global_settings)
def test_wrong_params_warning():
    from django_elasticache.memcached import ElastiCache
    ElastiCache('qew', {'BINARY': False})


@patch('django.conf.settings', global_settings)
@patch('django_elasticache.memcached.get_cluster_info')
def test_split_servers(get_cluster_info):
    from django_elasticache.memcached import ElastiCache
    backend = ElastiCache('h:0', {})
    servers = ['h1:p', 'h2:p']
    get_cluster_info.return_value = {
        'nodes': servers
    }
    backend._lib.Client = Mock()
    assert backend._cache
    get_cluster_info.assert_called_once_with('h', '0', False)
    backend._lib.Client.assert_called_once_with(servers)


@patch('django.conf.settings', global_settings)
@patch('django_elasticache.memcached.get_cluster_info')
def test_node_info_cache(get_cluster_info):
    from django_elasticache.memcached import ElastiCache
    servers = ['h1:p', 'h2:p']
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiCache('h:0', {})
    backend._lib.Client = Mock()
    backend.set('key1', 'val')
    backend.get('key1')
    backend.set('key2', 'val')
    backend.get('key2')
    backend._lib.Client.assert_called_once_with(servers)
    eq_(backend._cache.get.call_count, 2)
    eq_(backend._cache.set.call_count, 2)

    get_cluster_info.assert_called_once_with('h', '0', False)


@patch('django.conf.settings', global_settings)
@patch('django_elasticache.memcached.get_cluster_info')
def test_invalidate_cache(get_cluster_info):
    from django_elasticache.memcached import ElastiCache
    servers = ['h1:p', 'h2:p']
    get_cluster_info.return_value = {
        'nodes': servers
    }

    backend = ElastiCache('h:0', {})
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
    eq_(get_cluster_info.call_count, 2)
