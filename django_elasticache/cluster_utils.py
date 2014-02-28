"""
utils for discovery cluster
"""
from distutils.version import StrictVersion
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
    client = Telnet(host, port)
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
    client.read_until('\r\n')
    res = client.read_until('\r\n').strip()
    try:
        version = int(res)
    except ValueError:
        raise WrongProtocolData(cmd, res)
    res = client.read_until('\r\n').strip()
    client.close()
    nodes = []
    try:
        for node in res.split(' '):
            host, ip, port = node.split('|')
            nodes.append('{}:{}'.format(ip or host, port))
    except ValueError:
        raise WrongProtocolData(cmd, res)
    return {
        'version': version,
        'nodes': nodes
    }
