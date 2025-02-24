# -*- coding utf-8 -*-

from nextcord.ext.commands import Bot, Cog, has_permissions

from nextcord import Interaction
from nextcord import Member

from typing import Final

import asyncio
import logging
import nextcord

class Commands(Cog):

	def __init__(self, bot: Bot, /) -> None:
		self.bot: Bot = bot

	@Cog.listener()
	async def on_ready(self, /) -> None:
		logging.info('Commands are ready.')

	@has_permissions(administrator=True)
	@nextcord.slash_command(name='ikea', description='Renames a specific server memember to ikea furniture.')
	async def rename_command(self, interaction: Interaction, member: Member) -> None:
		logging.info('Called rename command.')
	
		if not interaction.guild:
			await interaction.response.send_message('This command can only be used in a server.', ephemeral=True)
			return

		if not interaction.guild.me.guild_permissions.manage_nicknames:
			await interaction.response.send_message("I don't have permission to change nicknames :(", ephemeral=True)
			return
			
		if member.top_role.position >= interaction.guild.me.top_role.position:
			await interaction.response.send_message(f"I can't rename {member.display_name} due to role hierarchy :(", ephemeral=True)
			return
		
		if member.id == self.bot.user.id:
			await interaction.response.send_message(f"I can't rename myself dummy, I'm already furniture!", ephemeral=True)
			return
		
		if not hasattr(self.bot, 'get_random_name'):
			raise AttributeError('Failed to find `get_random_name` method from parent client class, possible object mismatch')
			
		name: str = self.bot.get_random_name()

		try:
			await member.edit(nick=name)
			await interaction.response.send_message(f'Renamed {member.name} to {name}', ephemeral=True)
			logging.info(f'Renamed {member.name} to {name} in {interaction.guild.name}')

		except nextcord.Forbidden:
			await interaction.response.send_message(f'I don\'t have permission to rename {member.display_name} :(', ephemeral=True)
			logging.error(f'Failed to rename {member.display_name} in {interaction.guild.name} due to missing permissions')
		except Exception as exc:
			await interaction.response.send_message(f'Unknown exception occurred while trying to rename {member.display_name}, check logs for more info.', ephemeral=True)
			logging.error(f'Error renaming user {member.display_name}: {str(exc)}')

	@has_permissions(administrator=True)
	@nextcord.slash_command(name='unkea', description='Restores a specific server memember\'s name.')
	async def rename_command(self, interaction: Interaction, member: Member) -> None:
		logging.info('Called restore name command.')
	
		if not interaction.guild:
			await interaction.response.send_message('This command can only be used in a server.', ephemeral=True)
			return

		if not interaction.guild.me.guild_permissions.manage_nicknames:
			await interaction.response.send_message("I don't have permission to change nicknames :(", ephemeral=True)
			return
			
		if member.top_role.position >= interaction.guild.me.top_role.position:
			await interaction.response.send_message(f"I can't rename {member.display_name} due to role hierarchy :(", ephemeral=True)
			return
		
		if member.id == self.bot.user.id:
			await interaction.response.send_message(f"I can't rename myself dummy, I'm already furniture!", ephemeral=True)
			return
		
		name: Final[str] = member.global_name

		try:
			await member.edit(nick=name)
			await interaction.response.send_message(f'Renamed {member.display_name} to {member.global_name}', ephemeral=True)
			logging.info(f'Renamed {member.name} to {name} in {interaction.guild.name}')

		except nextcord.Forbidden:
			await interaction.response.send_message(f'I don\'t have permission to rename {member.display_name} :(', ephemeral=True)
			logging.error(f'Failed to rename {member.display_name} in {interaction.guild.name} due to missing permissions')
		except Exception as exc:
			await interaction.response.send_message(f'Unknown exception occurred while trying to rename {member.display_name}, check logs for more info.', ephemeral=True)
			logging.error(f'Error renaming user {member.display_name}: {str(exc)}')

	@nextcord.slash_command(name='ikea_all', description='Renames all server members to ikea furniture.')
	async def rename_all_command(self, interaction: Interaction) -> None:
		logging.info('Called rename all command.')

		if not interaction.guild:
			await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
			return
		
		if not interaction.guild.me.guild_permissions.manage_nicknames:
			await interaction.response.send_message('I don\'t have permission to change nicknames :(')
			return
		
		renamed_count: int = 0
		skipped_count: int = 0

		if not hasattr(self.bot, 'get_random_name'):
			raise AttributeError('Failed to find `get_random_name` method from parent client class, possible object mismatch')

		await interaction.response.send_message('Starting to rename all members... This might take a while.', ephemeral=True)

		members = interaction.guild.members
		total = len(members)

		for i, member in enumerate(members):

			if member.top_role.position >= interaction.guild.me.top_role.position or member.id == interaction.guild.owner_id:
				logging.info(f'Skipped renaming member {member.display_name}, skipped {skipped_count + 1} member(s)')
				skipped_count += 1
				continue

			try:

				name: str = self.bot.get_random_name()
				await member.edit(nick=name)
				renamed_count += 1
				await asyncio.sleep(0.5)
				logging.info(f'Renamed member {member.display_name}, renamed {renamed_count} member(s)')

				if member.id == self.bot.user.id:
					logging.info(f'Skipped renaming member {member.display_name}, skipped {skipped_count + 1} member(s)')
					skipped_count += 1

			except Exception:
				logging.info(f'Skipped renaming member {member.display_name}, skipped {skipped_count + 1} member(s)')
				skipped_count += 1

			if i % 5 == 0 or i == total-1:
				progress = min(100, round((i + 1) / total * 100))
				await interaction.edit_original_message(
					content=f'Renaming members... {progress}% complete ({i+1}/{total})'
				)

		await interaction.edit_original_message(
			content=f'Renamed {renamed_count} member(s), skipped {skipped_count} member(s).'
		)

		logging.info(f'Renamed {renamed_count} member(s) in {interaction.guild.name}')

	@nextcord.slash_command(name='unkea_all', description='Restores original usernames.')
	async def restore_names_command(self, interaction: Interaction) -> None:
		logging.info('Called restore names command.')

		if not interaction.guild:
			await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
			return
		
		if not interaction.guild.me.guild_permissions.manage_nicknames:
			await interaction.response.send_message('I don\'t have permission to change nicknames :(')
			return
		
		renamed_count: int = 0
		skipped_count: int = 0

		if not hasattr(self.bot, 'furniture_list'):
			await interaction.response.send_message('Internal Error Occurred.')
			raise AttributeError('Failed to find `get_random_name` method from parent client class, possible object mismatch')

		await interaction.response.send_message('Starting to rename all members... This might take a while.', ephemeral=True)

		members = interaction.guild.members
		total = len(members)

		for i, member in enumerate(members):

			if member.top_role.position >= interaction.guild.me.top_role.position or member.id == interaction.guild.owner_id:
				logging.info(f'Skipped renaming member {member.display_name}, skipped {skipped_count + 1} member(s)')
				skipped_count += 1
				continue

			if not (member.display_name in self.bot.furniture_list):
				continue

			try:
				await member.edit(nick=member.global_name)
				renamed_count += 1
				await asyncio.sleep(0.5)
				logging.info(f'Renamed member {member.display_name}, renamed {renamed_count} member(s)')

				if member.id == self.bot.user.id:
					logging.info(f'Skipped renaming member {member.display_name}, skipped {skipped_count + 1} member(s)')
					skipped_count += 1

			except Exception:
				logging.info(f'Skipped renaming member {member.display_name}, skipped {skipped_count + 1} member(s)')
				skipped_count += 1

			if i % 5 == 0 or i == total-1:
				progress = min(100, round((i + 1) / total * 100))
				await interaction.edit_original_message(
					content=f'Renaming members... {progress}% complete ({i+1}/{total})'
				)

		await interaction.edit_original_message(
			content=f'Renamed {renamed_count} member(s), skipped {skipped_count} member(s).'
		)

		logging.info(f'Renamed {renamed_count} member(s) in {interaction.guild.name}')

def setup(bot: Bot) -> None:
	bot.add_cog(Commands(bot))
