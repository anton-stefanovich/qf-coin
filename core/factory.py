from argparse import Namespace


def target_account(config: Namespace,
                   last_amounts: dict):
    from account import DebugAccount
    from account import CoinbaseAccount
    return DebugAccount(config) \
        if config.debug_mode else \
        CoinbaseAccount(config, last_amounts)
