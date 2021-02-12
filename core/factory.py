from argparse import Namespace


def target_account(config: Namespace):
    from account import DebugAccount
    from account import CoinbaseAccount
    return DebugAccount(config) \
        if config.debug_mode else \
        CoinbaseAccount(config)
