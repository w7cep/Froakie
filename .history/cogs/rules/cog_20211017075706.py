import nextcord
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
		
	@commands.command(name="test_rules", hidden=True)
	@commands.has_permissions(administrator=True)
	@commands.guild_only()
	async def test_rules(self, ctx):
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

	@commands.command(name="sysbot_rules")
	@commands.has_permissions(administrator=True)
	@commands.guild_only()
	async def sysbot_rules(self, ctx):

		"""SysBot Rules"""

		version = "v1.0.0"

		embed = nextcord.Embed(
			title="__**Greninja SysBot Rules**__",
			description="Anyone who break the rules or is just straight up a pain in the ass about it, gets access revoked, to either the bot or the server. \n\n__**The 10 Bot Commandments**__\n\n1. Don't try anything illegal, it won't work. \n2. You've tried everything and it still isn't legal, DM or ping <@&858153204146634782> \n2. Help can be asked, we won't shy away from it just make sure you've read<#858130122221420554> first. \n3. Anyone who uses it, does so at their own discretion. Don't be that person to call others out for using it. \n4. First try? Checkout <#858130122221420554> \n5. Made anything with the bot and you go sell it, insta-ban, no excuses.\n6. Refrain from deleting messages, even if it's a spelling mistake.  \n8. Have fun and Be respectful\n9. Using the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n10. No code sharing. The bot is for this server only\n\nBot access will be revoked for multiple offenders.\n\nRequests for special mons can be made in <#865074053759893525> , The PK8 Master will get to it as soon as he can.\n\nTo get access to the bots click below!\n🤖: Greninja SysBot Access",
			colour=nextcord.Colour.blue()
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_author(name="Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/866572422438060052/cb32b40409c7df4d147c400582f939ac.webp?size=4096")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"Bot is running {version}")
		await ctx.send(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(Rules(bot))