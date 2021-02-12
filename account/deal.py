from .offer import Offer


class Deal (Offer):

    def __init__(self, offer: Offer, amount: float, currency: str = 'USD'):
        self.__amount, self.__currency = abs(amount), currency
        super().__init__(*((offer.source, offer.target)
                           if amount > 0 else
                           (offer.target, offer.source)))

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def currency(self) -> str:
        return self.__currency
