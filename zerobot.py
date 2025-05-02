import discord
from discord.ext import commands
from datetime import datetime, timezone
import os

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="0", intents=intents)
GUILD_ID = discord.Object(id=870386780560568370)
TIMESTAMP = datetime.now(timezone.utc).strftime('%m-%d-%Y @ %H:%M:%S UTC')

@client.event
async def on_ready():
	print(f"Logged on as {client.user}")
	channel = client.get_channel(1357870960027631747)

	try:
		await load_cogs()
		guild = discord.Object(id=870386780560568370)
		synced = await client.tree.sync(guild=guild)
		print(f'Synced {len(synced)} commands to guild {guild.id}')
		await channel.send("https://tenor.com/view/vivy-vivy_ep10-gif-21749884")


	except Exception as e:
		print(f'Error syncing commands: {e}')



async def load_cogs():
	cog_paths = ["Commands", "Events", "Utils"]

	for folder in cog_paths:
		for filename in os.listdir(folder):
			if filename.endswith(".py") and filename != "__init__.py":
				cog_name = filename[:-3]
				try:
					await client.load_extension(f"{folder}.{cog_name}")
					print(f"Loaded cog: {cog_name}")
				except Exception as e:
					print(f"Failed to load cog {cog_name}: {e}")

with open("token.txt") as f:
	TOKEN = f.readline()
client.run(TOKEN)