"""
utils for discovery cluster
"""
from distutils.version import StrictVersion
import re
from telnetlib import Telnet


class WrongProtocolData(ValueError):
    """
    Exception for raising when we get something unexpected
    in telnet protocol
    """
    def __init__(self, cmd, response):
        super(WrongProtocolData, self).__init__(
            'Unexpected response {} for command {}'.format(response, cmd))


def get_cluster_info(host, port):
    """
    return dict with info about nodes in cluster and current version
    {
        'nodes': [
            'IP:port',
            'IP:port',
        ],
        'version': '1.4.4'
    }
    """
    client = Telnet(host, int(port))
    client.write('version\n')
    res = client.read_until('\r\n').strip()
    version_list = res.split(' ')
    if len(version_list) != 2 or version_list[0] != 'VERSION':
        raise WrongProtocolData('version', res)
    version = version_list[1]
    if StrictVersion(version) >= StrictVersion('1.4.14'):
        cmd = 'config get cluster\n'
    else:
        cmd = 'get AmazonElastiCache:cluster\n'
    client.write(cmd)
    res = client.read_until('\n\r\nEND\r\n')
    client.close()
    ls = filter(None, re.compile(r'\r?\n').split(res))
    if len(ls) != 4:
        raise WrongProtocolData(cmd, res)

    try:
        version = int(ls[1])
    except ValueError:
        raise WrongProtocolData(cmd, res)
    nodes = []
    try:
        for node in ls[2].split(' '):
            host, ip, port = node.split('|')
            nodes.append('{}:{}'.format(ip or host, port))
    except ValueError:
        raise WrongProtocolData(cmd, res)
    return {
        'version': version,
        'nodes': nodes
    }
