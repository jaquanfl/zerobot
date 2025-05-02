import discord
from discord.ext import commands
from discord import app_commands

class Logger(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # Command Listener
    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command):
        print(f"COMMAND: \"{command.name}\" FROM: {interaction.user}")

async def setup(client):
	await client.add_cog(Logger(client))