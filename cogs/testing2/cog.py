import nextcord
from nextcord.ext import commands
import asyncio
import random

class Testing2(commands.Cog, name="Testing2"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.command
	@commands.guild_only()
	async def lockdown(self, ctx, channel : nextcord.TextChannel=None, setting = None):
		if setting == '--server':
			for channel in ctx.guild.channels:
				await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name} with --server", send_messages=False)
			await ctx.send('locked down server')
		if channel is None:
			channel = ctx.message.channel
		await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name}", send_messages=False)
		await ctx.send('locked channel down')

	@commands.command
	@commands.guild_only()
	async def unlockdown(self, ctx, channel : nextcord.TextChannel=None, setting = None):
		if setting == '--server':
			for channel in ctx.guild.channels:
				await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name} with --server", send_messages=True)
			await ctx.send('unlocked server')
		if channel is None:
			channel = ctx.message.channel
		await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name}", send_messages=True)
		await ctx.send('unlocked channel')

def setup(bot: commands.Bot):
	bot.add_cog(Testing2(bot))
