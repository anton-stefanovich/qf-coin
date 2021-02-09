
if __name__ == '__main__':
    from tools.config import Config
    config = Config.read('config.json')

    from core.trader import Trader
    Trader(config).go()
