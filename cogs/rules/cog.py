import config
import nextcord
from cogs.error.friendly_error import FriendlyError
from nextcord.ext import commands
from utils.embedder import embed_success


class Rules(commands.Cog, name="Rules"):
	"""Command for mods to update rules"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.command(name="update_rules", hidden=True)
	@commands.has_guild_permissions(manage_roles=True)
	async def update_rules(self, ctx: commands.Context, *, args=None):
		"""Checks for a response from the bot"""
		# get the message containing the rules
		channel = self.bot.get_channel(config.RULES_CHANNEL_ID)
		message = await channel.fetch_message(config.RULES_MESSAGE_ID)
		# remove the bot command from the message
		try:
			new_rules = ctx.message.content.split(None, 1)[1]
		except ValueError as error:
			raise FriendlyError("missing content", ctx.channel, ctx.author, error)
		# update the rules
		await message.edit(
			content="",
			embed=embed_success(
				title="🚨 __Greninja's Grotto Rules__🚨", description=new_rules
			),
		)
		# confirmation
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed_success("Rules have been successfully updated. 🎉"))
  
def setup(bot: commands.Bot):
	bot.add_cog(Rules(bot))
