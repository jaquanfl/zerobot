import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone

class MessageLogger(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.timestamp = datetime.now(timezone.utc).strftime('%m-%d-%Y @ %H:%M:%S UTC')

    # Deleted Message Logging
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == 853629533855809596 or message.author.id == 159985870458322944 or message.author.id == 432610292342587392:
            return
        elif message.guild.id == 330867026803556354:
            return
        if message.author == self.client.user:
            embeds = message.embeds
            if embeds:
                await self.client.get_channel(1204132381561458728).send(embed=embeds[0])
            else:
                await self.client.get_channel(1204132381561458728).send(embed=discord.Embed(
                    title=f"Deleted Message by {message.author} in {message.channel.mention}",
                    description=f"\"{message.content}\"",
                    color=0xff0000)
                    .set_footer(text=self.timestamp))
        elif message.attachments:
            attachments = "".join([attachment.url for attachment in message.attachments])
            await self.client.get_channel(1357870960027631747).send(embed=discord.Embed(
                title=f"Deleted Message by {message.author} in {message.channel.mention}",
                description=f"\"{message.content}\"",
                color=0xff0000)
                .set_footer(text=self.timestamp)
                .set_image(url=attachments))
        else:
            await self.client.get_channel(1357870960027631747).send(embed=discord.Embed(
                title=f"Deleted Message by {message.author} in {message.channel.mention}",
                description=f"\"{message.content}\"",
                color=0xff0000)
                .set_footer(text=self.timestamp))
    
    # Edited Message Logging
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author == self.client.user or before.author.id == 853629533855809596 or before.author.id == 159985870458322944 or before.author.id == 432610292342587392:
            return
        elif before.content == after.content:
            return
        elif before.guild.id == 330867026803556354:
            return
        
        await self.client.get_channel(1357870960027631747).send(embed=discord.Embed(
                title=f"Edited Message by {before.author} in {before.channel.mention}",
                description=f"\"{before.content}\" \n\n ➡️ \"{after.content}\"",
                color=0xff0000)
                .set_footer(text=self.timestamp))
        
async def setup(client):
    cog = MessageLogger(client)
    await client.add_cog(cog)
    