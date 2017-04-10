"""
Backend for django cache
"""
import socket
from functools import wraps

from django.core.cache import InvalidCacheBackendError
from django.core.cache.backends.memcached import BaseMemcachedCache

from . import client as pymemcache_client
from .cluster_utils import get_cluster_info


def invalidate_cache_after_error(f):
    """
    catch any exception and invalidate internal cache with list of nodes
    """
    @wraps(f)
    def wrapper(self, *args, **kwds):
        try:
            return f(self, *args, **kwds)
        except Exception:
            self.clear_cluster_nodes_cache()
            raise
    return wrapper


class PyMemcacheElastiCache(BaseMemcachedCache):
    """
    backend for Amazon ElastiCache (memcached) with auto discovery mode
    it used pymemcache
    """
    def __init__(self, server, params):
        super(PyMemcacheElastiCache, self).__init__(
            server,
            params,
            library=pymemcache_client,
            value_not_found_exception=ValueError)
        if len(self._servers) > 1:
            raise InvalidCacheBackendError(
                'ElastiCache should be configured with only one server '
                '(Configuration Endpoint)')
        if len(self._servers[0].split(':')) != 2:
            raise InvalidCacheBackendError(
                'Server configuration should be in format IP:port')

        self._ignore_cluster_errors = self._options.get(
            'IGNORE_CLUSTER_ERRORS', False)

    def clear_cluster_nodes_cache(self):
        """clear internal cache with list of nodes in cluster"""
        if hasattr(self, '_cluster_nodes_cache'):
            del self._cluster_nodes_cache

    def get_cluster_nodes(self):
        """
        return list with all nodes in cluster
        """
        if not hasattr(self, '_cluster_nodes_cache'):
            server, port = self._servers[0].split(':')
            try:
                nodes = get_cluster_info(
                    server,
                    port,
                    self._ignore_cluster_errors
                )['nodes']
                self._cluster_nodes_cache = [ 
                    (i.split(':')[0], int(i.split(':')[1]))
                    for i in nodes
                ]
                print(self._cluster_nodes_cache)
            except (socket.gaierror, socket.timeout) as err:
                raise Exception('Cannot connect to cluster {} ({})'.format(
                    self._servers[0], err
                ))
        return self._cluster_nodes_cache

    @property
    def _cache(self):
        return self._lib.Client(self.get_cluster_nodes())

    @invalidate_cache_after_error
    def get(self, *args, **kwargs):
        return super(PyMemcacheElastiCache, self).get(*args, **kwargs)

    @invalidate_cache_after_error
    def get_many(self, *args, **kwargs):
        return super(PyMemcacheElastiCache, self).get_many(*args, **kwargs)

    @invalidate_cache_after_error
    def set(self, *args, **kwargs):
        return super(PyMemcacheElastiCache, self).set(*args, **kwargs)

    @invalidate_cache_after_error
    def set_many(self, *args, **kwargs):
        return super(PyMemcacheElastiCache, self).set_many(*args, **kwargs)

    @invalidate_cache_after_error
    def delete(self, *args, **kwargs):
        return super(PyMemcacheElastiCache, self).delete(*args, **kwargs)
