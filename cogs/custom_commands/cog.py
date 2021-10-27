import random
from typing import Optional

import nextcord
from aiohttp import request
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import BadArgument


class CustomCommands(commands.Cog, name="Custom_Commands"):
	"""Test commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	"""//TODO:gbi-Greninja SysBot Instructions command--Add in how to use a sysbot"""	
	@commands.command(name="sysbot_instructions", aliases=["sbi","bot_instructions", "bi"]) 
	async def sysbot_instructions(self, ctx):
		"""A useful command that displays sysbot instructions."""
		version = "v1.1.0"

		embed = nextcord.Embed(
			title=f"__Greninja SysBot Commands__",
			description="__🤖 New bot, Extra commands!🤖__",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		embed.add_field(name="__Trade any legal mon to your game__", value="`$trade, $t`\nE.G.:\n```$trade Scorbunny (M) @ Life Orb\nAbility: Libero\nLevel: 5\nShiny: Square\nBall: Poke Ball\nOT: FreshBot\nOTGender: Male\nTID: 035481\nSID: 0231\nEVs: 116 HP / 188 Atk/ 204 Spe\nIVs: 30 SpA\nJolly Nature\n- Blaze Kick\n- Sucker Punch\n- Gunk Shot\n- High Jump Kick\n```", inline=False)
		embed.add_field(name="__We all know the random mon command__", value="`$ga random`\nAnd when the pool has been released, the actual number of the one you want.\n`$ga ###`", inline=False)
		embed.add_field(name="__But it can do more!__", value="Got a pesky admon and you want it fixed?\nThis will change the OT to yours. (You can trick the bot by renaming it to a website for any OT change)\n`$fixot, $fix`", inline=False)
		embed.add_field(name="__Want an egg?__", value="`$trade egg <showdown format>`\nE.G.\n```$trade egg (Scorbunny) (F)\nShiny: Square\nJolly Nature\n- Tackle\n- Growl\n- Sucker Punch\n- High Jump Kick```", inline=False)
		embed.add_field(name="_Reminder_", value="Always ask for eggmoves, others will be illegal (or leave em blank when you just don't care)\nPut brackets around the mon's name. ", inline=False)
		embed.add_field(name="__Unlimited items__", value="Need an extra Master Ball or 20 or any other item?\nThe bot will send a Delibird with your item!\n```$itemtrade <item name>\n$item <item name>\n$it <item name>```\n\nE.G.\n`$item Beast Ball`", inline=False)
		embed.add_field(name="__Breeding Dittos__", value="```$dittotrade, $ditto,\n$dt <Stats> <Languages> <Nature>```\n\n`Stats:`\nChoosing one of these or all 3 will make that IV 0 or No Good. 6IV will always yield 31 or Best\nATK\nSPA\nSPE\n6IV\nCombinations can be made, no spaces between them.\n\n`E.G.`\nATKSPE will give you a ditto with 0 ATK & SPE\n`Language:`\nThese Locales in the games can be chosen:\nJapanese\nEnglish\nFrench\nItalian\nGerman\n\n`Nature:`\nHardy / Docile / Serious / Bashful\nQuirky / Lonely / Brave / Adamant\nNaughty / Bold / Relaxed / Impish\nLax / Modest / Mild / Quiet / Naive \nRash / Calm / Gentle / Sassy\nCareful / Timid / Hasty / Jolly\n_E.G. of the full command:_\n\n`$ditto SPE Japanese Brave`\nWill give you a 0 Speed Japanese Ditto with a Brave nature\n\n`$ditto 6IV German Timid`\nWill give you a 6IV German Ditto with a Timid nature.", inline=False)
		await ctx.send(embed=embed)
		"""//TODO:gbr-Greninja SysBot Rules command"""
		"""//TODO:illegal-Illegal Pokemon"""
		"""//TODO:rules-Rules!"""
		"""//TODO:tci-TradeCord Instructions"""
		"""//TODO:raid-How to request a den for Greninja Raid Bot to host."""
		"""//TODO:invite-Permanent Invite Link"""
def setup(bot: commands.Bot):
	bot.add_cog(CustomCommands(bot))
