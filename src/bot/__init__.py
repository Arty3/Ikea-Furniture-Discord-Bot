# -*- coding utf-8 -*-

from typing import Optional, List, Tuple, Literal, Dict, Final
from sys import version_info, version
from datetime import datetime
from os import system, name

import logging

__all__: List[str] = ['Client']

MIN_PYTHON_VERSION: Final[Tuple[Literal[3], Literal[8], Literal[1]]] = (3, 8, 1)

if version_info < MIN_PYTHON_VERSION:
	print(
		f'Python {".".join(map(str, MIN_PYTHON_VERSION))} is required'
		f'to run this module, but you have {version}. Please update Python.'
	)
	raise SystemExit(78)

def install() -> None:
	try:
		if name == 'nt':
			system('python -m pip install -r requirements.txt')
		else:
			system('python3 -m pip install -r requirements.txt')
	except OSError:
		logging.critical('Failed to install dependencies, manual intervention required.')
		raise SystemExit(1)

def verify(*, should_install: Optional[bool] = False) -> None:
	logging.info('Verifying dependencies...')
	try:
		import dotenv, nextcord, numpy, pandas
		logging.info('Verified all dependencies.')
	except ImportError:
		if not should_install:
			print('Missing critical dependencies, please run `pip install -r requirements.txt`')
			raise SystemExit(1)
		
		logging.info('Missing required dependencies, attempting install...')
		install()

class ColorFormatter(logging.Formatter):
	COLORS: Final[Dict[str, str]] = {
		'DEBUG':	'\033[94m',	# Blue
		'INFO':		'\033[92m',	# Green
		'WARNING':	'\033[93m',	# Yellow
		'ERROR':	'\033[91m',	# Red
		'CRITICAL':	'\033[41m',	# Red background
	}

	RESET: Final[Literal['\033[0m']] = '\033[0m'

	TIMESTAMP_COLOR: Final[Literal['\033[90m']] = '\033[90m'

	def format(self, record: logging.LogRecord, /) -> str:
		log_level_color: Final[str] = self.COLORS.get(record.levelname, self.RESET)
		record.levelname = f'{log_level_color}{record.levelname}{self.RESET}'
		return super().format(record)
	
	def formatTime(self, record: logging.LogRecord, /, datefmt: Optional[str] = None) -> str:
		return f'{self.TIMESTAMP_COLOR}{datetime.fromtimestamp(record.created).strftime(datefmt)}{self.RESET}'

logger: logging.Logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('./logs/client.log', mode='w')
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_formatter = logging.Formatter(
	'%(asctime)s [%(levelname)s] %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

stream_formatter = ColorFormatter(
	'%(asctime)s %(levelname)s\t%(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(file_formatter)
console_handler.setFormatter(stream_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

verify(should_install=True)
