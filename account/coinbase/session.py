from requests import Session


class CoinbaseSession (Session):
    from argparse import Namespace

    def __init__(self, config: Namespace):
        super().__init__()
        self.cookies.update(
            dict(jwt=config.trade_cookie))
