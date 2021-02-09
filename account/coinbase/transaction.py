class CoinbaseTransaction:

    from .session import CoinbaseSession
    from ..transaction import Transaction

    from ._constants import __CB_BASE_URL__
    __CB_TRADE_URL__ = f'{__CB_BASE_URL__}/trades'

    def __init__(self, session: CoinbaseSession,
                 transaction: Transaction,
                 assets_map: dict):
        self.__session = session

        from json import dumps, loads
        response = self.__session.post(self.__CB_TRADE_URL__, dumps(
            dict(source_asset=assets_map.get(transaction.source),
                 target_asset=assets_map.get(transaction.target),
                 amount=transaction.amount, amount_asset='USD',
                 amount_from='input')))

        from tools.picker import cherry_pick_first
        self.__transaction_id = cherry_pick_first(
            loads(response.text), 'id')

        assert self.__transaction_id

    def commit(self, attempts: int = 7, attempt_timeout: int = 1) -> bool:

        transaction_link = f'{self.__CB_TRADE_URL__}/{self.__transaction_id}'
        self.__session.post(f'{transaction_link}/commit')

        from json import loads
        from tools.picker import cherry_pick_first
        for attempt in range(attempts):  # checking the transaction status
            transaction_status = self.__session.get(transaction_link)
            if transaction_status and 'completed' in cherry_pick_first(
                    loads(transaction_status.text), 'status'):
                return print('Transaction succeed') or True

            else:
                from time import sleep
                print(f'Transaction verification failed #{attempt}')
                sleep(attempt_timeout if attempt < attempts - 1 else 0)

        return print('No transaction success status') or False
