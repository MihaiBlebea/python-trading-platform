from typing import Protocol, Tuple


class PriceGetter(Protocol):

	def get_symbol_price(self, symbol: str)-> Tuple[float, float]:
		pass