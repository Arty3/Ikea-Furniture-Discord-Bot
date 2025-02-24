# -*- coding utf-8 -*-

from dotenv import dotenv_values
from typing import Dict, Union

from os import system, name

from bot.client import Client

def clear_screen() -> None:
	try:
		if name == 'nt':
			system('cls')
		else:
			system('clear')
	except:
		pass

def main() -> None:

	env: Dict[str, Union[str, None]]
	env = dotenv_values(dotenv_path='.env')

	client: Client = Client.from_intents(
		token=env['BOT_TOKEN'],
		prefix=env['BOT_PREFIX']
	)

	client.launch_client()

if __name__ == '__main__':
	clear_screen(); main()
