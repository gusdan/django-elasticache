"""
Backend for django cache
"""
import socket
from django.core.cache import InvalidCacheBackendError
from django.core.cache.backends.memcached import PyLibMCCache
from django.utils.functional import cached_property
from .cluster_utils import get_cluster_info


class ElastiCache(PyLibMCCache):
    """
    backend for Amazon ElastiCache (memcached) with auto discovery mode
    it used pylibmc in binary mode
    """
    def __init__(self, server, params):
        self.update_params(params)
        super(ElastiCache, self).__init__(server, params)
        if len(self._servers) > 1:
            raise InvalidCacheBackendError(
                'ElastiCache should be configured with only one server '
                '(Configuration Endpoint)')
        if len(self._servers[0].split(':')) != 2:
            raise InvalidCacheBackendError(
                'Server configuration should be in format IP:port')

    def update_params(self, params):
        """
        update connection params to maximize performance
        """
        if not params.get('BINARY', True):
            raise Warning('To increase performance please use ElastiCache'
                          ' in binary mode')
        else:
            params['BINARY'] = True  # patch params, set binary mode
        if not 'OPTIONS' in params:
            # set special 'behaviors' pylibmc attributes
            params['OPTIONS'] = {
                'tcp_nodelay': True,
                'ketama': True
            }

    @cached_property
    def get_cluster_nodes(self):
        """
        return list with all nodes in cluster
        """
        server, port = self._servers[0].split(':')
        try:
            return get_cluster_info(server, port)['nodes']
        except (socket.gaierror, socket.timeout) as err:
            raise Exception('Cannot connect to cluster {} ({})'.format(
                self._servers[0], err
            ))

    @property
    def _cache(self):
        # PylibMC uses cache options as the 'behaviors' attribute.
        # It also needs to use threadlocals, because some versions of
        # PylibMC don't play well with the GIL.

        # instance to store cached version of client
        # in Django 1.7 use self
        # in Django < 1.7 use thread local
        container = getattr(self, '_local', self)
        client = getattr(container, '_client', None)
        if client:
            return client

        client = self._lib.Client(self.get_cluster_nodes)
        if self._options:
            client.behaviors = self._options

        container._client = client

        return client
