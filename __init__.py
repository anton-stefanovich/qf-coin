
if __name__ == '__main__':
    from _engine.config import Config
    config = Config.read('config.json')

    from account import AccountFake
    account = AccountFake(config)

    from _engine.trader import Trader
    Trader(account, config).go()
