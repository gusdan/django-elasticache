from django.conf import global_settings
from mock import patch, Mock
from nose.tools import eq_, raises


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
    get_cluster_info.assert_called_once_with('h', '0')
    backend._lib.Client.assert_called_once_with(servers)


@patch('django.conf.settings', global_settings)
@patch('django_elasticache.memcached.get_cluster_info')
def test_property_cache(get_cluster_info):
    from django_elasticache.memcached import ElastiCache
    backend = ElastiCache('h:0', {})
    servers = ['h1:p', 'h2:p']
    get_cluster_info.return_value = {
        'nodes': servers
    }
    backend._lib.Client = Mock()
    backend.set('key1', 'val')
    backend.set('key2', 'val')
    backend._lib.Client.assert_called_once_with(servers)
