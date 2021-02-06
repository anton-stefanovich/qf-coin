
class Config:
    from argparse import Namespace

    @staticmethod
    def read(filename: str) -> Namespace:
        with open(filename, 'r') as config:
            from json import load
            config = load(config)

        from argparse import ArgumentParser
        parser = ArgumentParser('Auto''trader by QF')

        for _type, _keys in {
            float: ('trade-percentage', 'trade-amount',
                    'debug-exchange-fee', 'debug-amount'),
            str:   ('trade-currencies', 'trade-cookie', 'debug-scope',
                    'api-key', 'api-secret', 'api-version')}.items():
            for _key in _keys:  # iterating the keys set
                parser.add_argument(
                    f'--%s' % _key.replace('-', '_'), f'--{_key}',
                    type=_type, default=config.get(_key, None))

        return parser.parse_args()
