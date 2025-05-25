from discord import app_commands
from discord.ext import commands
from Utils.casino_manager import CasinoManager
import random

casino = CasinoManager()
class Casino(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(name="new", aliases=["create", "start"])
	async def create_account(self, ctx):
		if casino.make_account(ctx.author.id) is None:
			await ctx.send(f"❌ {ctx.author.mention}, you already have an account.")
		else:
			await ctx.send(f"✅ {ctx.author.mention}, your account has been created.")

	@commands.command()
	async def balance(self, ctx):
		bal = casino.get_balance(ctx.author.id)
		if bal is None:
			await ctx.send(f"❌ {ctx.author.mention}, you don't have an account. Use `0new` to create one.")
			return
		else:
			await ctx.send(f"{ctx.author.mention}, you have 🪙 {bal} coins")

	@commands.command()
	async def coinflip(self, ctx, guess: str, bet: int):
		guess = guess.lower()
		if guess not in ["heads", "tails"]:
			await ctx.send("❌ Guess must be 'heads' or 'tails'.")
			return

		current = casino.get_balance(ctx.author.id)
		if bet > current or bet <= 0:
			await ctx.send("❌ Invalid bet amount.")
			return

		import random
		result = random.choice(["heads", "tails"])
		if result == guess:
			winnings = bet
			new_bal = casino.update_balance(ctx.author.id, winnings)
			await ctx.send(f"🎉 It's {result}! You won {winnings} coins! New balance: {new_bal}")
		else:
			new_bal = casino.update_balance(ctx.author.id, -bet)
			await ctx.send(f"💀 It's {result}. You lost {bet} coins. New balance: {new_bal}")
	
	@commands.command(name="work", help="Work a small job and earn coins every 5 minutes.")
	@commands.cooldown(rate=1, per=300.0, type=commands.BucketType.user)  # 5 minutes per user
	async def work(self, ctx):
		earnings = random.randint(5, 15)
		new_bal = casino.update_balance(ctx.author.id, earnings)
		await ctx.send(f"💼 You put fries in a bag and earned {earnings} coins. Your new balance is {new_bal} 💰")

	@work.error
	async def work_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			remaining = error.retry_after
			minutes, seconds = divmod(int(remaining), 60)
			await ctx.send(f"⏳ You can work again in {minutes}m {seconds}s.")
		else:
			raise error
# async def setup(client):
# 	cog = Casino(client)
# 	await client.add_cog(cog)

