from nextcord.ext import commands
import config
from utils.utils import embed_success
from cogs.error.friendly_error import FriendlyError

class Rules(commands.Cog, name="Rules"):
	"""Command for mods to update rules"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="update_rules")
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
				title="🚨 Dev Pro Tips Server Rules", description=new_rules
			),
		)
		# confirmation
		await ctx.send(embed=embed_success("Rules have been successfully updated. 🎉"))
		
	@commands.command(name="rules")
	@commands.has_permissions(administrator=True)
	@commands.guild_only()
	async def rules(self, ctx):
		await ctx.send(	f"\n<:Switch:865465921040678932> __**The Rules**__ <:Switch:865465921040678932>\n\n"
						f"1. Full compliance to Discord's ToS.\n"
						f"2. Absolutely no drama.\n"
						f"3. Got issues with someone, talk to <@&829942684947841024>  or <@&867254914563178527> or resolve it in DM's.\n"
						f"4. Keep your -isms IRL and not in here.\n"
						f"5. You've got 3 strikes, so don't be that person.\n"
						f"6. Invite your friends, yet keep the Drama Queens out.\n"
						f"7. Please keep Politics and Religion out, we don't mind a healthy discussion, but DMs are best suited for that.\n"
						f"8. We allow pinging each other, demanding not to get pinged will get you a warning.\n"
						f"9. We don't mind cussing, sarcasm or sexually tinted jokes, but keep porn out.\n"
						f"10. Don't ask or distribute illegal Pokémon, talk is permitted (Use `!illegal` for a list).\n"
						f"11. No selling of any kind. (unless approved by an admin).\n"
						f"12. Don't DM other members unless you have their permission to do so.\n\n"
						f"This can be updated for future reference.\n\n"
						f"Click :thumbsup:Confirm to gain access to the rest of the server!\n\n"
						f"Then visit <#861616591199141908> to give yourself some roles and <#868914000572846120> for Sys-Bot access!\n\n"
						f"https://discord.gg/dm7gSAT68d\n\n"
						f"Server and Bot rules subject to change.\n\n"
						f"<a:rainbowmeltandab:866027057691230229>\n\n")

def setup(bot: commands.Bot):
	bot.add_cog(Rules(bot))