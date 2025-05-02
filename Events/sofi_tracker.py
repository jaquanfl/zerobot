import re
import asyncio
import discord
from discord.ext import commands

class SofiTracker(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		self.client.process_commands(message)

		if message.channel.id != 1319243069480243341:
			return

		# Sofi bot ID
		if message.author.id == 853629533855809596:
			match = re.match(r"<@!?(\d+)> is \*\*dropping\*\* cards", message.content)
			if match:
				user_id = int(match.group(1))
				asyncio.create_task(self.start_sofi_timer(user_id, message.channel))
				print(f"Creating a timer for: {user_id}")

	async def start_sofi_timer(self, user_id, channel):
		await asyncio.sleep(8 * 60)
		user = await self.client.fetch_user(user_id)
		print(f"Timer expired for user: {user}")
		await channel.send(f"{user.mention} you can drop cards now")

async def setup(client):
	await client.add_cog(SofiTracker(client))
