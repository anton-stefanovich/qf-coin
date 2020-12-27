
from data.picker import cherry_pick_first
from time import sleep


class Trader:

    __CB_BASE_URL__ = 'https://www.coinbase.com/api/v2'

    def __init__(self, config, currencies: (list, tuple)):
        from pycoinbaseapi.wallet.client import Client
        self.__client = Client(config.api_key, config.api_secret,
                               api_version=config.api_version)

        known_accounts = self.__client \
            .get_accounts().response.json()

        self.__currencies = currencies
        account_details = tuple(cherry_pick_first(
                known_accounts, name=f'{currency} Wallet')
            for currency in self.__currencies)

        self.__account_asset_map = dict((
                cherry_pick_first(account, 'id'),
                cherry_pick_first(account, 'asset_id'))
            for account in account_details)

        # creating the new session
        from requests import session
        self.__session = session()  # no parameters
        self.__session.cookies.update(dict(jwt=config.trade_cookie))

    def trade(self):
        from trigger import Trigger
        trigger = Trigger(sensitivity=0.05)
        # rates_master = self.__client.get_exchange_rates()
        # assert not rates_master.warnings  # means we re ok

        def pick_rate_values():
            rates_link = f'{self.__CB_BASE_URL__}/assets/prices?base=USD' \
                          '&filter=listed&resolution=latest'
            from requests import get
            rates_response = get(rates_link)
            return None if not rates_response else tuple(float(cherry_pick_first(
                    cherry_pick_first(rates_response.json(), base=currency), 'latest'))
                for currency in self.__currencies)

        self._do_sync_exchange(pick_rate_values())

        while True:
            rates = pick_rate_values()
            if trigger.feed(*rates):
                trigger.reset() \
                    if self._do_sync_exchange(rates) \
                    else trigger.mute()

            sleep(7)  # sleep between updates

    def _do_sync_exchange(self, current_rates) -> bool:
        coinbase_trades_url = f'{self.__CB_BASE_URL__}/trades'
        print('Trade started due the trigger flagged')

        known_accounts = self.__account_asset_map.keys()
        account_masters = tuple(
            self.__client.get_account(account)
            for account in known_accounts)

        account_details = tuple(account_master.refresh().response.json()
                                for account_master in account_masters)

        account_balances = tuple(float(
            cherry_pick_first(details, 'balance > amount'))
            for details in account_details)

        actual_balance = tuple(balance * rate for balance, rate in zip(account_balances, current_rates))
        trade_value = round((actual_balance[0] - actual_balance[1]) * 100 / 2) / 100
        if abs(trade_value) < 0.5:  # means too less value for trading
            return print(f'Trading aborted due too less trade value: {trade_value}') or False

        source_target = list(
            self.__account_asset_map[key]
            for key in known_accounts)

        if trade_value < 0:
            source_target.reverse()
        source, target = source_target

        from json import dumps, loads
        response = self.__session.post(
            coinbase_trades_url, dumps(dict(
                amount_asset='USD', amount_from='input',
                source_asset=source, target_asset=target,
                amount=abs(trade_value))))

        transaction_id = cherry_pick_first(loads(response.text), 'id')
        if transaction_id:

            transaction_link = f'{coinbase_trades_url}/{transaction_id}?'
            self.__session.post(f'{transaction_link}/commit')

            for _ in range(7):
                transaction_status = self.__session.get(transaction_link)
                if transaction_status and 'completed' in cherry_pick_first(
                        loads(transaction_status.text), 'status'):
                    break

                else:
                    sleep(1)  # sleep between status check attempts

            else:  # no transaction success status
                return print('No transaction success status') or False

            # transaction succeed
            return print('Transaction succeed') or True

        else:  # no transaction_id
            return print('Cant get transaction ID') or False
