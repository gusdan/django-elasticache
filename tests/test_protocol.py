from django_elasticache.cluster_utils import (
    get_cluster_info, WrongProtocolData)
from nose.tools import eq_, raises
import sys
if sys.version < '3':
    from mock import patch, call, MagicMock
else:
    from unittest.mock import patch, call, MagicMock


TEST_PROTOCOL_1 = [
    b'VERSION 1.4.14',
    b'CONFIG cluster 0 138\r\n1\nhost|ip|port host||port\n\r\nEND\r\n',
]

TEST_PROTOCOL_2 = [
    b'VERSION 1.4.13',
    b'CONFIG cluster 0 138\r\n1\nhost|ip|port host||port\n\r\nEND\r\n',
]


@patch('django_elasticache.cluster_utils.Telnet')
def test_happy_path(Telnet):
    client = Telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_1
    info = get_cluster_info('', 0)
    eq_(info['version'], 1)
    eq_(info['nodes'], ['ip:port', 'host:port'])


@raises(WrongProtocolData)
@patch('django_elasticache.cluster_utils.Telnet', MagicMock())
def test_bad_protocol():
    get_cluster_info('', 0)


@patch('django_elasticache.cluster_utils.Telnet')
def test_last_versions(Telnet):
    client = Telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_1
    get_cluster_info('', 0)
    client.write.assert_has_calls([
        call(b'version\n'),
        call(b'config get cluster\n'),
    ])


@patch('django_elasticache.cluster_utils.Telnet')
def test_prev_versions(Telnet):
    client = Telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_2
    get_cluster_info('', 0)
    client.write.assert_has_calls([
        call(b'version\n'),
        call(b'get AmazonElastiCache:cluster\n'),
    ])
