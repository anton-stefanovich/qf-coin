
def start(once: bool):
    from .trader import Trader
    from tools.config import Config
    Trader(Config.read('config.json')) \
        .go(1 if once else None)
