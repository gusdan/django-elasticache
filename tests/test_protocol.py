import sys

from django_elastipymemcache.cluster_utils import (
    WrongProtocolData,
    get_cluster_info,
)
from nose.tools import eq_, raises

if sys.version < '3':
    from mock import patch, call, MagicMock
else:
    from unittest.mock import patch, call, MagicMock


TEST_PROTOCOL_1_READ_UNTIL = [
    b'VERSION 1.4.14',
]

TEST_PROTOCOL_1_EXPECT = [
    (0, None, b'CONFIG cluster 0 138\r\n1\nhost|ip|11211 host||11211\n\r\nEND\r\n'),  # NOQA
]

TEST_PROTOCOL_2_READ_UNTIL = [
    b'VERSION 1.4.13',
]

TEST_PROTOCOL_2_EXPECT = [
    (0, None, b'CONFIG cluster 0 138\r\n1\nhost|ip|11211 host||11211\n\r\nEND\r\n'),  # NOQA
]

TEST_PROTOCOL_3_READ_UNTIL = [
    b'VERSION 1.4.14 (Ubuntu)',
]

TEST_PROTOCOL_3_EXPECT = [
    (0, None, b'CONFIG cluster 0 138\r\n1\nhost|ip|11211 host||11211\n\r\nEND\r\n'),  # NOQA
]

TEST_PROTOCOL_4_READ_UNTIL = [
    b'VERSION 1.4.34',
]

TEST_PROTOCOL_4_EXPECT = [
    (0, None, b'ERROR\r\n'),
]


@patch('django_elastipymemcache.cluster_utils.Telnet')
def test_happy_path(Telnet):
    client = Telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_1_READ_UNTIL
    client.expect.side_effect = TEST_PROTOCOL_1_EXPECT
    info = get_cluster_info('', 0)
    eq_(info['version'], 1)
    eq_(info['nodes'], [('ip', 11211), ('host', 11211)])


@raises(WrongProtocolData)
@patch('django_elastipymemcache.cluster_utils.Telnet', MagicMock())
def test_bad_protocol():
    get_cluster_info('', 0)


@patch('django_elastipymemcache.cluster_utils.Telnet')
def test_last_versions(Telnet):
    client = Telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_1_READ_UNTIL
    client.expect.side_effect = TEST_PROTOCOL_1_EXPECT
    get_cluster_info('', 0)
    client.write.assert_has_calls([
        call(b'version\n'),
        call(b'config get cluster\n'),
    ])


@patch('django_elastipymemcache.cluster_utils.Telnet')
def test_prev_versions(Telnet):
    client = Telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_2_READ_UNTIL
    client.expect.side_effect = TEST_PROTOCOL_2_EXPECT
    get_cluster_info('', 0)
    client.write.assert_has_calls([
        call(b'version\n'),
        call(b'get AmazonElastiCache:cluster\n'),
    ])


@patch('django_elastipymemcache.cluster_utils.Telnet')
def test_ubuntu_protocol(Telnet):
    client = Telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_3_READ_UNTIL
    client.expect.side_effect = TEST_PROTOCOL_3_EXPECT

    # try:
    #     get_cluster_info('', 0)
    # except WrongProtocolData:
    #     raise AssertionError('Raised WrongProtocolData with Ubuntu version.')
    get_cluster_info('', 0)

    client.write.assert_has_calls([
        call(b'version\n'),
        call(b'config get cluster\n'),
    ])


@raises(WrongProtocolData)
@patch('django_elastipymemcache.cluster_utils.Telnet')
def test_no_configuration_protocol_support_with_errors(Telnet):
    client = Telnet.return_value
    client.read_until.side_effect = TEST_PROTOCOL_4_READ_UNTIL
    client.expect.side_effect = TEST_PROTOCOL_4_EXPECT
    get_cluster_info('test', 0)
    client.write.assert_has_calls([
        call(b'version\n'),
        call(b'config get cluster\n'),
    ])
