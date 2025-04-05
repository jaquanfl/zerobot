import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone
import aiohttp
import random

class Client(commands.Bot):
	async def on_ready(self):
		print(f"Logged on as {self.user}")    

		try:
			guild = discord.Object(id=870386780560568370)
			synced = await self.tree.sync(guild=guild)
			print(f'Synced {len(synced)} commands to guild {guild.id}')

		except Exception as e:
			print(f'Error syncing commands: {e}')
	
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="0", intents=intents)
GUILD_ID = discord.Object(id=870386780560568370)
TIMESTAMP = datetime.now(timezone.utc).strftime('%m-%d-%Y @ %H:%M:%S UTC')

# Ping Command
@client.tree.command(name="ping",description="Latency Test",guild=GUILD_ID)
async def getPing(interaction):
	print(f"COMMAND: \"ping\" FROM: {interaction.user}")
	await interaction.response.send_message(f"Pong: {round(client.latency*1000)}ms")

# Say command
@client.tree.command(name="say",description="Make Z.RO speak",guild=GUILD_ID)
async def sayMsg(interaction, message: str):
	print(f"COMMAND: \"say\" FROM: {interaction.user} PARAM: \"{message}\"")
	await interaction.response.send_message(message)

# Clean Command
@client.tree.command(name="clean",description="Remove a specified number of messages",guild=GUILD_ID)
@app_commands.describe(amount="Number of messages to delete")
async def cleanMsg(interaction, amount: int):
	clean_limit=50
	print(f"COMMAND: \"clean\" FROM: {interaction.user} PARAM: \"{amount}\"")
	await interaction.response.defer(ephemeral=True)
	if interaction.user.id != 185171693566689280:
		await interaction.channel.send(f"You do not have permission to use this command.")
		return
	elif amount < 1 or amount > clean_limit:
		await interaction.followup.send(f"You can only delete between 1 and {clean_limit} messages.", ephemeral=True)
		return
	else:
		deleted = await interaction.channel.purge(limit=amount)
		await interaction.followup.send(f"Deleted {len(deleted)} messages.")  
		# await interaction.channel.send(f"{interaction.user.mention} has cleaned {len(deleted)} messages.")

# Embed Message Test
@client.tree.command(name="embed",description="Embed messsage test",guild=GUILD_ID)
@app_commands.describe(text="Message to embed")
async def embedMsg(interaction, text: str):
	print(f"COMMAND: \"embed\" FROM: {interaction.user} PARAM: \"{text}\"")
	embed = discord.Embed(title=text,color=0x0000ff)
	await interaction.response.send_message(embed=embed)

# Deleted Message Logging
@client.event
async def on_message_delete(message):
	if message.author == client.user or message.author.id == 853629533855809596 or message.author.id == 159985870458322944 or message.author.id == 432610292342587392:
		return
	if message.attachments:
		attachments = "".join([attachment.url for attachment in message.attachments])
		await client.get_channel(1357870960027631747).send(embed=discord.Embed(
			title=f"Deleted Message by {message.author} in {message.channel.mention}",
			description=f"\"{message.content}\"",
			color=0xff0000)
			.set_footer(text=TIMESTAMP)
			.set_image(url=attachments))
	else:
		await client.get_channel(1357870960027631747).send(embed=discord.Embed(
			title=f"Deleted Message by {message.author} in {message.channel.mention}",
			description=f"\"{message.content}\"",
			color=0xff0000)
			.set_footer(text=TIMESTAMP))

# Edited Message Logging
@client.event
async def on_message_edit(before,after):
	if before.author == client.user or before.author.id == 853629533855809596 or before.author.id == 159985870458322944 or before.author.id == 432610292342587392:
		return
	elif before.content == after.content:
		return
	
	await client.get_channel(1357870960027631747).send(embed=discord.Embed(
			title=f"Edited Message by {before.author} in {before.channel.mention}",
			description=f"**Before: **\"{before.content}\"\n**After: **\"{after.content}\"",
			color=0xffff00)
			.set_footer(text=TIMESTAMP))


# Anime Command
@client.tree.command(name="anime", description="Get a random anime from MyAnimeList with optional filters", guild=GUILD_ID)
@app_commands.describe(
	min_score="Minimum score (1-10)",
	max_score="Maximum score (1-10)",
	aired_from="Earliest year (e.g., 2020)",
	aired_to="Latest year (e.g., 2023)"
)
async def anime(
	interaction: discord.Interaction,
	min_score: float = None,
	max_score: float = None,
	aired_from: int = None,
	aired_to: int = None
):
	print(f"COMMAND: \"anime\" FROM: {interaction.user} PARAM: \"min_score: {min_score}, max_score: {max_score}, aired_from: {aired_from}, aired_to: {aired_to}\"")
	await interaction.response.defer()

	# If no filters are provided, use the true random anime endpoint
	if not min_score and not max_score and not aired_from and not aired_to:
		full_url = "https://api.jikan.moe/v4/random/anime"
	else:
		# Use /anime endpoint with filters
		api_url = "https://api.jikan.moe/v4/anime"
		params = {}
		if min_score:
			params["min_score"] = min_score
		if max_score:
			params["max_score"] = max_score
		if aired_from:
			params["start_date"] = f"{aired_from}-01-01"
		if aired_to:
			params["end_date"] = f"{aired_to}-12-31"
		
		# Convert params to query string
		query_string = "&".join(f"{key}={value}" for key, value in params.items())
		full_url = f"{api_url}?{query_string}&limit=25"  # Fetch up to 25 results

	async with aiohttp.ClientSession() as session:
		async with session.get(full_url) as response:
			if response.status != 200:
				await interaction.followup.send("⚠️ Failed to fetch anime. Please try again later.")
				return
			data = await response.json()

	# If using /anime endpoint, pick a random anime from results
	if "data" in data and isinstance(data["data"], list):
		if not data["data"]:
			await interaction.followup.send("⚠️ No anime found with the given filters.")
			return
		anime_info = random.choice(data["data"])  # Randomly pick from filtered list
	else:
		anime_info = data["data"]  # Use directly if from /random/anime
	
	# Extracting relevant information
	title = anime_info["title"]
	synopsis = anime_info["synopsis"] if anime_info["synopsis"] else "No synopsis available."
	image_url = anime_info["images"]["jpg"]["image_url"]
	mal_url = anime_info["url"]
	score = anime_info["score"] if anime_info["score"] else "N/A"
	episodes = anime_info["episodes"] if anime_info["episodes"] else "Unknown"
	aired_from = anime_info["aired"]["from"][:10] if anime_info["aired"]["from"] else "Unknown"
	aired_to = anime_info["aired"]["to"][:10] if anime_info["aired"]["to"] else None
	if aired_to:
		aired_display = f"{aired_from} to {aired_to}"
	else:
		aired_display = aired_from  # Show only the start date
	studios = ", ".join(studio["name"] for studio in anime_info["studios"]) if anime_info["studios"] else "Unknown"
	source = anime_info["source"] if anime_info["source"] else "Unknown"
	genres = ", ".join(genre["name"] for genre in anime_info["genres"]) if anime_info["genres"] else "None"

	embed = discord.Embed(
		title=title,
		description=synopsis[:400] + ("..." if len(synopsis) > 400 else ""),  # Shorten long descriptions
		color=0x2f52a2,
		url=mal_url
	)
	embed.set_thumbnail(url=image_url)
	embed.add_field(name="📊 Score", value=str(score), inline=True)
	embed.add_field(name="🎬 Episodes", value=str(episodes), inline=True)
	embed.add_field(name="📅 Aired", value=aired_display, inline=False)
	embed.add_field(name="🏢 Studio", value=studios, inline=True)
	embed.add_field(name="📖 Source", value=source, inline=True)
	embed.add_field(name="🎭 Genres", value=genres, inline=False)
	embed.set_footer(text="Source: MyAnimeList")

	await interaction.followup.send(embed=embed)

# Manga Command
@client.tree.command(name="manga", description="Get a random manga from MyAnimeList", guild=GUILD_ID)
async def manga(interaction: discord.Interaction):
	await interaction.response.defer()

	async with aiohttp.ClientSession() as session:
		async with session.get("https://api.jikan.moe/v4/random/manga") as response:
			if response.status != 200:
				await interaction.followup.send("⚠️ Failed to fetch manga. Please try again later.")
				return
			data = await response.json()
	
	manga_info = data["data"]
	
	# Extracting relevant information
	title = manga_info["title"]
	synopsis = manga_info["synopsis"] if manga_info["synopsis"] else "No synopsis available."
	image_url = manga_info["images"]["jpg"]["image_url"]
	mal_url = manga_info["url"]
	score = manga_info["score"] if manga_info["score"] else "N/A"
	chapters = manga_info["chapters"] if manga_info["chapters"] else "Unknown"
	published_from = manga_info["published"]["from"][:10] if manga_info["published"]["from"] else "Unknown"
	published_to = manga_info["published"]["to"][:10] if manga_info["published"]["to"] else None
	type = manga_info["type"] if manga_info["type"] else "Unknown"
	if published_to:
		published_display = f"{published_from} to {published_to}"
	else:
		published_display = published_from  # Show only the start date
	authors = ", ".join(studio["name"] for studio in manga_info["authors"]) if manga_info["authors"] else "Unknown"
	genres = ", ".join(genre["name"] for genre in manga_info["genres"]) if manga_info["genres"] else "None"

	embed = discord.Embed(
		title=title,
		description=synopsis[:400] + ("..." if len(synopsis) > 400 else ""),  # Shorten long descriptions
		color=0x2f52a2,
		url=mal_url
	)
	embed.set_thumbnail(url=image_url)
	embed.add_field(name="📊 Score", value=str(score), inline=True)
	embed.add_field(name="🔖 Chapters", value=str(chapters), inline=True)
	embed.add_field(name="📖 Type", value=type, inline=False)
	embed.add_field(name="📅 Published", value=published_display, inline=False)
	embed.add_field(name="🏢 Authors", value=authors, inline=True)
	embed.add_field(name="🎭 Genres", value=genres, inline=False)
	embed.set_footer(text="Source: MyAnimeList")

	await interaction.followup.send(embed=embed)


with open("token.txt") as f:
	TOKEN = f.readline()
client.run(TOKEN)