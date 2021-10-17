import nextcord
import random
from typing import Optional
from aiohttp import request
from nextcord.ext import commands
from nextcord import Member, Embed
from nextcord.ext.commands import BadArgument

class Testing(commands.Cog, name="Testing"):
	"""Test commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(name="add", descripton="Adds two numbers together.")
	async def add(ctx, left: int, right: int):
			await ctx.send(left + right)

	@commands.command(
		 name="repeat",
		description="Repeat a message a number of times."
	)
	async def repeat(ctx, times: int, content='repeating...'):
			for i in range(times):
				await ctx.send(content)

	@commands.command(name="cmd")
	@commands.has_permissions(administrator=True)
	@commands.guild_only()
	async def cmd(self, ctx):

		"""Test Embed."""
		
		version = "v1.0.0"
		
		embed = nextcord.Embed(
			title="__**Server Rules**__",
			description="<:Switch:865465921040678932> __**The Rules**__ <:Switch:865465921040678932>\n\n1. Full compliance to Discord's ToS. \n2. Absolutely no drama. \n3. Got issues with someone, talk to <@&829942684947841024>  or @Moderator or resolve it in DM's. \n4. Keep your -isms IRL and not in here. \n5. You've got 3 strikes, so don't be that person.\n6. Invite your friends, yet keep the Drama Queens out.\n7. Please keep Politics and Religion out, we don't mind a healthy discussion, but DMs are best suited for that. \n8. We allow pinging each other, demanding not to get pinged will get you a warning.\n9. We don't mind cussing, sarcasm or sexually tinted jokes, but keep porn out.\n10. Don't ask or distribute illegal Pokémon, talk is permitted (Use `!illegal` for a list) \n11.No selling of any kind. (unless approved by an admin)\n12. Don't DM other members unless you have their permission to do so.\n\nThis can be updated for future reference. \n\nReact to the message with 👍 to gain access to the rest of the server!\n\nThen visit <#861616591199141908> to give yourself some roles and <#868914000572846120> for Sys-Bot access!\n\n[Permanent Invite Link:](https://discord.gg/dm7gSAT68d) \n\nServer and Bot rules subject to change.\n\n<a:rainbowmeltandab:866027057691230229>",
			colour=nextcord.Colour.blue()
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_author(name="Greninja Mod", icon_url="https://cdn.discordapp.com/avatars/866572422438060052/cb32b40409c7df4d147c400582f939ac.webp?size=4096")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")                                               
		embed.set_footer(text=f"Bot is running {version}")
		await ctx.send(embed=embed)
		

def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))