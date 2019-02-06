import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from sparksd import SparksDaemon
from sparks_config import SparksConfig


def test_sparksd():
    config_text = SparksConfig.slurp_config_file(config.sparks_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000a5c6ddfaac5097218560d5b92d416931cfeba1abf10c81d1d6a232fc8ea'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000005f15ec2b9e4495efb539fb5b113338df946291cccd8dfd192bb68cd6dcf'

    creds = SparksConfig.get_rpc_creds(config_text, network)
    sparksd = SparksDaemon(**creds)
    assert sparksd.rpc_command is not None

    assert hasattr(sparksd, 'rpc_connection')

    # Sparks testnet block 0 hash == 000005f15ec2b9e4495efb539fb5b113338df946291cccd8dfd192bb68cd6dcf
    # test commands without arguments
    info = sparksd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert sparksd.rpc_command('getblockhash', 0) == genesis_hash
