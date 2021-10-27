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
	
	@commands.command(name="sysbot_instructions", aliases=["sbi","bot_instructions", "bi"]) 
	async def sysbot_instructions(self, ctx):
		"""A useful command that displays sysbot instructions."""
		version = "v1.1.0"

		embed = nextcord.Embed(
			title=f"__Greninja SysBot Commands__",
			description="__🤖 New bot, Extra commands!🤖__",
      # \n\n`$trade, $t`\n\nE.G.:\n```$trade Scorbunny (M) @ Life Orb\nAbility: Libero\nLevel: 5\nShiny: Square\nBall: Poke Ball\nOT: FreshBot\nOTGender: Male\nTID: 035481\nSID: 0231\nEVs: 116 HP / 188 Atk / 204 Spe\nIVs: 30 SpA\nJolly Nature\n- Blaze Kick\n- Sucker Punch\n- Gunk Shot\n- High Jump Kick```\n\nWe all know the random mon command\n``` $ga random\n\nAnd when the pool has been released, the actual number of the one you want.\n\n$ga ###\n\n```\n**But it can do more! **\n\nGot a pesky admon and you want it fixed? \nThis will change the OT to yours. (You can trick the bot by renaming it to a website for any OT change)\n```\n$fixot, $fix\n```\nWant an egg? \n```\n$trade egg <showdown format>\n\nE.G.\n$trade egg (Scorbunny) (F)\nShiny: Square\nJolly Nature\n- Tackle\n- Growl\n- Sucker Punch\n- High Jump Kick\n\nAlways ask for eggmoves, others will be illegal (or leave em blank when you just don't care) \nPut brackets around the mon's name. \n```\nNeed an extra Master Ball or 20 or any other item? \nThe bot will send a Delibird with your item! \n```\n\n$itemtrade <item name>\n$item <item name>\n$it <item name>\n\nE.G.\n$item Beast Ball\n```\nLooking to breed for a shiny, but need a specific Ditto? \n```\n$dittotrade, $ditto, $dt <Stats> <Language> <Nature>\n\nStats: \nChoosing one of these or all 3 will make that IV 0 or No Good. 6IV will always yield 31 or Best  \nATK\nSPA\nSPE\n6IV\nCombinations can be made, no spaces between them. \n\nE.G.\nATKSPE will give you a ditto with 0 ATK & SPE\n\nLanguage:\nThese Locales in the games can be chosen:\nJapanese\nEnglish\nFrench\nItalian\nGerman\n\nNature: \nHardy / Docile / Serious / Bashful\nQuirky / Lonely / Brave / Adamant\nNaughty / Bold / Relaxed / Impish\nLax / Modest / Mild / Quiet / Naive \nRash / Calm / Gentle / Sassy\nCareful / Timid / Hasty / Jolly\n\nE.G. of the full command: \n\n$ditto SPE Japanese Brave\nWill give you a 0 Speed Japanese Ditto with a Brave nature\n\n$ditto 6IV German Timid\nWill give you a 6IV German Ditto with a Timid nature. \n```",
   			# "Anyone who break the rules or is just straight up a pain in the ass about it, gets access revoked, to either the bot or the server. \n\n1. Don't try anything illegal, it won't work. \n2. You've tried everything and it still isn't legal, DM or ping <@&858153204146634782> \n2. Help can be asked, we won't shy away from it just make sure you've read<#858130122221420554> first. \n3. Anyone who uses it, does so at their own discretion. Don't be that person to call others out for using it. \n4. First try? Checkout <#858130122221420554> \n5. Made anything with the bot and you go sell it, insta-ban, no excuses.\n6. Refrain from deleting messages, even if it's a spelling mistake.  \n8. Have fun and Be respectful\n9. Using the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n10. No code sharing. The bot is for this server only\n\nBot access will be revoked for multiple offenders.\n\nRequests for special mons can be made in <#865074053759893525> , The PK8 Master will get to it as soon as he can.\n\nTo get access to the bots click below!\n🤖: Greninja SysBot Access",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		embed.add_field(name="`$trade, $t`", value="```E.G.:\n$trade Scorbunny (M) @ Life Orb\nAbility: Libero\nLevel: 5\nShiny: Square\nBall: Poke Ball\nOT: FreshBot\nOTGender: Male\nTID: 035481\nSID: 0231\nEVs: 116 HP / 188 Atk/ 204 Spe\nIVs: 30 SpA\nJolly Nature\n- Blaze Kick\n- Sucker Punch\n- Gunk Shot\n- High Jump Kick\n```", inline=False)
		embed.add_field(name="__We all know the random mon command__", value="`$ga random`\nAnd when the pool has been released, the actual number of the one you want.\n`$ga ###`", inline=False)
		await ctx.send(embed=embed)
     
def setup(bot: commands.Bot):
	bot.add_cog(CustomCommands(bot))
