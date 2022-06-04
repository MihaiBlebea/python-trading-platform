import logging
from pathlib import Path

CWD = Path(__file__).parent.resolve()

class Logger:
	
	def log(self, level: str, message: str)-> None:
		logging.basicConfig(
			filename=f"{CWD}/../../../app.log", 
			filemode="w", 
			format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
			datefmt="%d-%b-%y %H:%M:%S",
			level=logging.DEBUG
		)

		match level:
			case "info": logging.info(message)
			case "error": logging.error(message)
			case "debug": logging.debug(message)
			case _ : logging.info(message)
