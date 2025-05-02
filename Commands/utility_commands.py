import discord
from discord import app_commands
from discord.ext import commands

class UtilityCommands(commands.Cog):
	def __init__(self, client):
		self.client = client

	# Ping Command
	async def getPing(self, interaction: discord.Interaction):
		await interaction.response.send_message(f"{round(self.client.latency * 1000)}ms")
	
	# Say Command
	async def sayMsg(self, interaction: discord.Interaction, message: str):
		await interaction.response.send_message(message)

	# Clean Command
	async def cleanMsg(self, interaction: discord.Interaction, amount: int):
		clean_limit = 50
		await interaction.response.defer(ephemeral=True)
		if interaction.user.id != 185171693566689280:
			await interaction.followup.send("You do not have permission to use this command.")
			return
		elif amount < 1 or amount > clean_limit:
			await interaction.followup.send(f"You can only delete between 1 and {clean_limit} messages.", ephemeral=True)
			return
		else:
			deleted = await interaction.channel.purge(limit=amount)
			await interaction.followup.send(f"Deleted {len(deleted)} messages.")

	# Echo Command
	@commands.command(name="echo")
	async def echo(self, ctx, channel: str, *, message: str):
		channels = {"general": 870386780984209482, "zero": 1357870960027631747, "sofi": 1319243069480243341}
		try:
			if ctx.author.id != 185171693566689280:
				await ctx.send("🤨")
				return
			if channel.lower() not in channels:
				await ctx.send("❌ Unknown channel name. Use one of: " + ", ".join(channels.keys()))
				return
			channel_obj = self.client.get_channel(channels[channel.lower()])
			if channel_obj is None:
				await ctx.send("⚠️ Could not resolve the channel ID.")
				return

			await channel_obj.send(message)
			await ctx.send(f"✅ Message sent to {channel_obj.mention}")
		except Exception as e:
			await ctx.send(f"⚠️ Error: {e}")

async def setup(client):
	cog = UtilityCommands(client)
	await client.add_cog(cog)
	
	@app_commands.command(name="ping", description="Latency Test")
	async def ping_command(interaction):
		await cog.getPing(interaction)
	client.tree.add_command(ping_command, guild=discord.Object(id=870386780560568370))

	@app_commands.command(name="say", description="Make Z.RO speak")
	async def say_command(interaction, message: str):
		await cog.sayMsg(interaction, message)
	client.tree.add_command(say_command, guild=discord.Object(id=870386780560568370))

	@app_commands.command(name="clean", description="Remove a specified number of messages")
	@app_commands.describe(amount="Number of messages to delete")
	async def clean_command(interaction, amount: int):
		await cog.cleanMsg(interaction, amount)
	client.tree.add_command(clean_command, guild=discord.Object(id=870386780560568370))