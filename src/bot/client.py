# -*- coding utf-8 -*-

from typing import Optional, List

from nextcord.ext.commands import Bot
from numpy.typing import NDArray
from numpy import random

from nextcord import Intents
from pandas import read_csv
import numpy as np

import nextcord
import logging

class Client(Bot):

	def __init__(self, /, *, token: str, prefix: str, intents: Intents) -> None:
		super().__init__(command_prefix=prefix, intents=intents, help_command=None)

		logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s [%(levelname)s] %(message)s',
			datefmt='%Y-%m-%d %H:%M:%S'
		)

		logging.info(f'Using intents: {intents.__repr__()}')

		self._token: str = token

		self._load_furniture()

		logging.info('Applying command cog')
		self.load_extension('bot.commands')
		logging.info('Successfully applied commands.')

		logging.info(f'Client instance built.')

	def _load_furniture(self, /, *, csv_data_path: Optional[str] = './data/ikea-furniture.csv') -> None:
		logging.info(f'Loading Ikea furniture data from: {csv_data_path}')

		try:
			self._furniture: NDArray[np.str_] = read_csv(csv_data_path)['name'].to_numpy()
		except Exception as exc:
			logging.critical(f'Failed to load Ikea furniture data: {str(exc)}')
			raise SystemExit(1)
		
		logging.info('Successfully loaded Ikea furniture data')

	@property
	def token(self, /) -> str:
		return self._token
	
	@property
	def prefix(self, /) -> str:
		return self.command_prefix
	
	@property
	def furniture_list(self, /) -> List[str]:
		return self._furniture.tolist()
	
	def get_random_name(self, /) -> str:
		return random.choice(self._furniture)

	async def on_ready(self, /) -> None:
		logging.info('Successfully connected to the discord API')
		logging.info(f'Client logged in as bot user: {self.user}')
		logging.info('Client is ready.')

	def launch_client(self, /) -> None:
		try:
			self.run(self._token)
		except nextcord.LoginFailure:
			logging.critical(f'Client failed to log into {self.user}')
		except Exception as exc:
			logging.error(f'{str(exc)}')

	@classmethod
	def from_intents(cls, /, *, token: str, prefix: str) -> object:

		intents: Intents = Intents.default()
		intents.message_content = True
		intents.members = True
		intents.guilds = True

		return cls(token=token, prefix=prefix, intents=intents)
