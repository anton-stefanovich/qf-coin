
if __name__ == '__main__':
    from tools.config import Config
    config = Config.read('config.json')

    from account import DebugAccount
    account = DebugAccount(config)

    from core.trader import Trader
    Trader(account, config).go()
