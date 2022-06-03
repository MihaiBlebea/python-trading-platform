from typing import Tuple
import yfinance as yf

class PriceGetter:

	def get_symbol_price(self, symbol: str)-> Tuple[float, float]:
		"""
		Get current price of the symbol.

		Accepts symbol string as param.

		Returns tupple with (bid, ask) as the two params.
		"""
		ticker = yf.Ticker(symbol)
		info = ticker.get_info()
		bid = info["bid"]
		ask = info["ask"]

		return (bid, ask,)