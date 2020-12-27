
def read_config():
    with open('./config.json', 'r') as config:
        from json import load
        config = load(config)

    from argparse import ArgumentParser
    parser = ArgumentParser('Auto''trader by QF')
    for key in ('api-key', 'api-secret', 'api-version', 'trade-cookie'):
        parser.add_argument(f'--%s' % key.replace('-', '_'), f'--{key}',
                            type=str, default=config.get(key, None))

    return parser.parse_args()


if __name__ == '__main__':
    from trader import Trader
    Trader(read_config(), ('ETC', 'ETH')).trade()
