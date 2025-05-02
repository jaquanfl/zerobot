import discord
from discord import app_commands
from discord.ext import commands
from Utils.jikan_api import JikanHandler
import aiohttp
import random

class AnimeCommands(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.jikan = JikanHandler()

	async def anime(self, interaction: discord.Interaction, min_score: float = None, max_score: float = None, aired_from: int = None, aired_to: int = None):
		await interaction.response.defer()

		params = {}
		if min_score:
			params["min_score"] = min_score
		if max_score:
			params["max_score"] = max_score
		if aired_from:
			params["start_date"] = f"{aired_from}-01-01"
		if aired_to:
			params["end_date"] = f"{aired_to}-12-31"

		async with aiohttp.ClientSession() as session:
			data = await self.jikan.fetch_random_anime(session, params if params else None)
			if not data:
				await interaction.followup.send("⚠️ Failed to fetch anime. Please try again later.")
				return

		# Get anime from either random or filtered results
		anime_info = None
		if "data" in data and isinstance(data["data"], list):
			if not data["data"]:
				await interaction.followup.send("⚠️ No anime found with the given filters.")
				return
			anime_info = random.choice(data["data"])
		else:
			anime_info = data["data"]

		# Build and send embed
		title = anime_info["title"]
		synopsis = anime_info["synopsis"] or "No synopsis available."
		image_url = anime_info["images"]["jpg"]["image_url"]
		mal_url = anime_info["url"]
		score = anime_info["score"] or "N/A"
		episodes = anime_info["episodes"] or "Unknown"
		aired_start = anime_info["aired"]["from"][:10] if anime_info["aired"]["from"] else "Unknown"
		aired_end = anime_info["aired"]["to"][:10] if anime_info["aired"]["to"] else None
		aired_display = f"{aired_start} to {aired_end}" if aired_end else aired_start
		studios = ", ".join(studio["name"] for studio in anime_info["studios"]) or "Unknown"
		source = anime_info["source"] or "Unknown"
		genres = ", ".join(genre["name"] for genre in anime_info["genres"]) or "None"

		embed = discord.Embed(
			title=title,
			description=synopsis[:400] + ("..." if len(synopsis) > 400 else ""),
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

	async def manga(self, interaction: discord.Interaction, min_score: float = None, max_score: float = None, published_from: int = None, published_to: int = None):
		await interaction.response.defer()

		params = {}
		if min_score:
			params["min_score"] = min_score
		if max_score:
			params["max_score"] = max_score
		if published_from:
			params["start_date"] = f"{published_from}-01-01"
		if published_to:
			params["end_date"] = f"{published_to}-12-31"

		async with aiohttp.ClientSession() as session:
			data = await self.jikan.fetch_random_manga(session, params if params else None)
			if not data:
				await interaction.followup.send("⚠️ Failed to fetch manga. Please try again later.")
				return

		# Get manga from either random or filtered results
		manga_info = None
		if "data" in data and isinstance(data["data"], list):
			if not data["data"]:
				await interaction.followup.send("⚠️ No manga found with the given filters.")
				return
			manga_info = random.choice(data["data"])
		else:
			manga_info = data["data"]

		# Build and send embed
		title = manga_info["title"]
		synopsis = manga_info["synopsis"] or "No synopsis available."
		image_url = manga_info["images"]["jpg"]["image_url"]
		mal_url = manga_info["url"]
		score = manga_info["score"] or "N/A"
		chapters = manga_info["chapters"] or "Unknown"
		published_start = manga_info["published"]["from"][:10] if manga_info["published"]["from"] else "Unknown"
		published_end = manga_info["published"]["to"][:10] if manga_info["published"]["to"] else None
		published_display = f"{published_start} to {published_end}" if published_end else published_start
		authors = ", ".join(authors["name"] for authors in manga_info["authors"]) or "Unknown"
		mal_type = manga_info["type"] or "Unknown"
		genres = ", ".join(genre["name"] for genre in manga_info["genres"]) or "None"

		embed = discord.Embed(
			title=title,
			description=synopsis[:400] + ("..." if len(synopsis) > 400 else ""),
			color=0x2f52a2,
			url=mal_url
		)
		embed.set_thumbnail(url=image_url)
		embed.add_field(name="📊 Score", value=str(score), inline=True)
		embed.add_field(name="🎬 Chapters", value=str(chapters), inline=True)
		embed.add_field(name="📅 Published", value=published_display, inline=False)
		embed.add_field(name="✍️ Author", value=authors, inline=True)
		embed.add_field(name="📖 Type", value=mal_type, inline=True)
		embed.add_field(name="🎭 Genres", value=genres, inline=False)
		embed.set_footer(text="Source: MyAnimeList")

		await interaction.followup.send(embed=embed)

async def setup(client):
	cog = AnimeCommands(client)
	await client.add_cog(cog)	
	
	@app_commands.command(name="anime", description="Get a random anime from MyAnimeList")
	@app_commands.describe(
		min_score="Minimum score (1-10)",
		max_score="Maximum score (1-10)",
		aired_from="Earliest year (e.g., 2020)",
		aired_to="Latest year (e.g., 2023)"
	)
	async def anime_command(interaction, min_score: float = None, max_score: float = None, aired_from: int = None, aired_to: int = None):
		await cog.anime(interaction, min_score, max_score, aired_from, aired_to)
	client.tree.add_command(anime_command, guild=discord.Object(id=870386780560568370))

	@app_commands.command(name="manga", description="Get a random manga from MyAnimeList")
	@app_commands.describe(
		min_score="Minimum score (1-10)",
		max_score="Maximum score (1-10)",
		published_from="Earliest year (e.g., 2020)",
		published_to="Latest year (e.g., 2023)"
	)
	async def manga_command(interaction, min_score: float = None, max_score: float = None, published_from: int = None, published_to: int = None):
		await cog.manga(interaction, min_score, max_score, published_from, published_to)
	client.tree.add_command(manga_command, guild=discord.Object(id=870386780560568370))