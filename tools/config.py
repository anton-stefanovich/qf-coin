
class Config:
    from argparse import Namespace

    @staticmethod
    def read(filename: str) -> Namespace:
        with open(filename, 'r') as config:
            from json import load
            config = load(config)

        from argparse import ArgumentParser
        parser = ArgumentParser('Auto''trader by QF')

        def get_aliases(key: str) -> tuple:
            return '--%s' % key.replace('-', '_'), f'--{key}'

        for _type, _keys in {
            float: ('debug-exchange-fee', 'debug-amount',
                    'trade-limit', 'trade-rebound', 'trade-timeout'),
            str:   ('api-key', 'api-secret', 'api-version', 'auth-cookie',
                    'trade-currencies', 'trade-status-file', 'debug-scope',
                    'log-level', 'log-record-format', 'log-file-name',
                    'log-date-format')
                }.items():  # picking arguments and theirs types
            for _key in _keys:  # iterating the picked keys set
                parser.add_argument(*get_aliases(_key), type=_type,
                                    default=config.get(_key, None))

        for _key, _default in {
                'debug-mode': True}.items():
            from tools.converter import any_to_bool
            parser.add_argument(*get_aliases(_key), type=any_to_bool, nargs='?',
                                const=True, default=config.get(_key, _default))

        return parser.parse_args()
