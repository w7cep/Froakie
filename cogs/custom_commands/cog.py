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

	@commands.command(name="sysbot_instructions", aliases=["sbi","bot_instructions", "bi"], hidden=True) 
	async def sysbot_instructions(self, ctx):
		"""A useful command that displays sysbot instructions."""
		version = "v1.1.0"
		embed = nextcord.Embed(
			title=f"__Greninja SysBot Instructions__",
			description="Greninja Bot Prefix: `$`",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		embed.add_field(name="🤖How To Use A Sysbot**Part 1 - Showdown format**🤖", value="-Go to https://play.pokemonshowdown.com/teambuilder\n-In Format Tab Select 'Ubers' under 'SWSH'\n-Now Go To New Team'\n-You Should now see 'Add Pokémon'\n-Either select or type the Pokémon you want to create\n-You have control over stuff like the nickname, items, abilities, moveset\n-Now that you have finished the Pokémon click validate to check that the import is legal\n-If you want to make sure the Pokémon are usable in ranked/VGC and other online competitions for Format select VGC 2020\n-When everything is finished click Import/Export and copy the text\n-Type command of the sysbot then space and Paste the text in the bot channel\n\n-The sysbot will send a personal message aka DM to you with a Link Trade Code for an online trade in Sword or Shield.\n-Type the code the bot sent you and start searching, once found, trade the bot a junkmon (no trade evolutions or illegals).\n-Once the trade is complete cancel trade and you're all set.\n-The bot will then proceed to send you a PK8 file of the Pokémon you sent.\n", inline=False)
		embed.add_field(name="🤖How To Use A Sysbot Part 2 - PK8 Files🤖", value="-Make, request or check #cloning-requests for PK8 files.\n-Type $trade and add the PK8 file as an attachment to the message in the bot channel.\n-The sysbot will send a personal message aka DM to you with a Link Trade Code for an online trade in Sword or Shield.\n-Type the code the bot sent you and start searching, once found, trade the bot a junkmon (no trade evolutions or illegals).\n-Once the trade is complete cancel trade and you're all set.\n-The bot will then proceed to send you a PK8 file of the Pokémon you sent.\n\n-If you can't add a file to the message or you don't want to download a file, go back to Part 1.", inline=False)
		embed.add_field(name="🤖How To Use A Sysbot Part 3 - Clone🤖", value="-Type $clone in the bot channel.\n-The sysbot will send a personal message aka DM to you with a Link Trade Code for an online trade in Sword or Shield.\n-Type the code the bot sent you and start searching, once found, trade the bot the Pokémon you want to clone.\n-The bot will message you to cancel the trade by pressing B. When done correctly, the bot will send you a PK8 file of the Pokémon you want to clone.\n-Then trade the bot a junkmon (no trade evolutions or illegals).\n-Once the trade is complete cancel trade and you're all set.\n-The bot will then proceed to send you a PK8 file of the Pokémon you sent.", inline=False)
		embed.add_field(name="__🤖 New bot, Extra commands!🤖__", value="`$trade, $t`\n__E.G.__\n```$trade Scorbunny (M) @ Life Orb\nAbility: Libero\nLevel: 5\nShiny: Square\nBall: Poke Ball\nOT: FreshBot\nOTGender: Male\nTID: 035481\nSID: 0231\nEVs: 116 HP / 188 Atk/ 204 Spe\nIVs: 30 SpA\nJolly Nature\n- Blaze Kick\n- Sucker Punch\n- Gunk Shot\n- High Jump Kick\n```", inline=False)
		embed.add_field(name="__We all know the random mon command__", value="`$ga random`\n-And when the pool has been released, the actual number of the one you want.\n`$ga ###`", inline=False)
		embed.add_field(name="__But it can do more!__", value="-Got a pesky admon and you want it fixed?\n-This will change the OT to yours. (You can trick the bot by renaming it to a website for any OT change)\n`$fixot, $fix`", inline=False)
		embed.add_field(name="__Want an egg?__", value="`$trade egg <showdown format>`\n__E.G.__\n```$trade egg (Scorbunny) (F)\nShiny: Square\nJolly Nature\n- Tackle\n- Growl\n- Sucker Punch\n- High Jump Kick```", inline=False)
		embed.add_field(name="_Reminder_", value="-Always ask for eggmoves, others will be illegal (or leave em blank when you just don't care)\n-Put brackets around the mon's name. ", inline=False)
		embed.add_field(name="__Unlimited items__", value="-Need an extra Master Ball or 20 or any other item?\n-The bot will send a Delibird with your item!\n`$itemtrade <item name>`\n`$item <item name>`\n`$it <item name>`\n__E.G.__\n`$item Beast Ball`", inline=False)
		embed.add_field(name="__Breeding Dittos__", value="`$dittotrade, $ditto, $dt <Stats> <Languages> <Nature>`\n\n`Stats:`\nChoosing one of these or all 3 will make that IV 0 or No Good. 6IV will always yield 31 or Best\n-ATK\n-SPA\n-SPE\n-6IV\n\nCombinations can be made, no spaces between them.\n__E.G.__\n'ATKSPE' will give you a ditto with 0 ATK & SPE\n`Language:`\nThese Locales in the games can be chosen:\n-Japanese\n-English\n-French\n-Italian\n-German\n`Nature:`\nHardy / Docile / Serious / Bashful\nQuirky / Lonely / Brave / Adamant\nNaughty / Bold / Relaxed / Impish\nLax / Modest / Mild / Quiet / Naive \nRash / Calm / Gentle / Sassy\nCareful / Timid / Hasty / Jolly\n\n__**E.G. of the full command:**__\n`$ditto ATKSPE Japanese Brave`\n-Will give you a 0 Speed Japanese Ditto with a Brave nature\n`$ditto 6IV German Timid`\n-Will give you a 6IV German Ditto with a Timid nature.", inline=False)
		await ctx.send(embed=embed)

	@commands.command(name="sysbot_rules", aliases=["sbr","bot_rules", "br"], hidden=True) 
	async def sysbot_rules(self, ctx):
		"""A useful command that displays sysbot rules."""
		version = "v1.1.0"

		embed = nextcord.Embed(
		title="__**Greninja SysBot Rules**__",
		description="Anyone who break the rules or is just straight up a pain in the ass about it, gets access revoked, to either the bot or the server. \n\n1. Don't try anything illegal, it won't work. \n2. You've tried everything and it still isn't legal, DM or ping <@&858153204146634782> \n2. Help can be asked, we won't shy away from it just make sure you've read<#858130122221420554> first. \n3. Anyone who uses it, does so at their own discretion. Don't be that person to call others out for using it. \n4. First try? Checkout <#858130122221420554> \n5. Made anything with the bot and you go sell it, insta-ban, no excuses.\n6. Refrain from deleting messages, even if it's a spelling mistake.  \n8. Have fun and Be respectful\n9. Using the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n10. No code sharing. The bot is for this server only\n\nBot access will be revoked for multiple offenders.\n\nRequests for special mons can be made in <#865074053759893525> , The PK8 Master will get to it as soon as he can.\n\nTo get access to the bots click below!\n🤖: Greninja SysBot Access",
		colour=ctx.author.colour,
		timestamp=ctx.message.created_at,
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.send(embed=embed)

	@commands.command(name="rules", aliases=["server_rules", "Rules", "sr"], hidden=True) 
	async def rules(self, ctx):
		"""A useful command that displays server rules."""
		version = "v1.1.0"

		embed = nextcord.Embed(
			title=f"__Greninja SysBot Commands__",
			description=f"\n<:Switch:865465921040678932> __**The Rules**__ <:Switch:865465921040678932>\n\n"
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
						f"<a:rainbowmeltandab:866027057691230229>\n\n",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.send(embed=embed)

	@commands.command(name="tradecord_instructions", aliases=["tci", "tc_instructions"], hidden=True) 
	async def sysbot_instructions(self, ctx):
		"""A useful command that displays TradeCord instructions."""
		version = "v1.1.0"

		embed = nextcord.Embed(
			title=f"__Greninja SysBot Commands__",
			description=f"__**Commands:**__\n", 
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)   
		embed.add_field(name="1", value=f"`$catch / $k` - Will 'catch' a random Pokémon with an optional (but highly recommended) cool down.\n\n"
										f"`$tc <catch id> / $tc <link code> <catch id>` - Trade a catch. File will be moved to a backup folder just in case.\n\n"
										f"`$tis` - Set custom trainer info via an attached .pk8 file. Type $tis, attach a file, send as one message. Bot will automatically set trainer info.\n\n"
										f"`$ti` - Display currently set trainer info.\n\n"
										f"`$list <name/shinies/all/egg/ball> / $l <name/shinies/all/egg/ball>` - Displays a list of specific species or a list of shinies a user has.\n\n", inline=False)
		embed.add_field(name="2", value=f"`$dc` - Display daycare.\n\n"
										f"`$dc w <catch id or 'all'> / $dc withdraw <catch id or 'all'>` - Withdraw a specific Pokémon from daycare, or withdraw everything.\n\n"
										f"`$dc d <catch id> / $dc deposit <catch id>` - Deposit a specific Pokémon to daycare.\n\n"
										f"`$release <catch id> / $r <catch id>` - Release a specific Pokémon. File will be deleted.\n\n"
										f"`$massrelease <optional species-form, cherish or shiny>/ $mr <optional species-form, cherish or shiny>` - Will release everything that's not shiny, not a Ditto, not in a Cherish Ball, not in favorites, and not in daycare. If species and/or form specified, will release just that (still obeys prior criteria). Files will be deleted.\n\n", inline=False)
		embed.add_field(name="3", value=f"`$info <catch id> / $i <catch id>` - Displays a Showdown set for a specific Pokémon.\n\n"
										f"`$gift <catch id> <@user> / $g <catch id> <@user>` - Gift a Pokémon to another user. If the receiving user has fewer than 10 Dex completions and hasn't registered the Pokémon being gifted, it will be registered to their Dex.\n\n"
										f"`$fav` - Displays a list of favorite Pokémon.\n\n"
										f"`$fav <catch id or 'clear''>` - Adds a Pokémon to favorites (or removes it if it's already added to favorites). If keyword 'clear' is entered, it will unfavorite everything. Favorite Pokémon cannot be released or mass released.\n\n"
										f"`$dex <optional 'missing' parameter>` - Shows your TradeCordDex progress (catches, level), or a list of Pokémon you haven't caught yet. Whenever a full dex is completed, level is increased. Levels can be used as points for perk selection.\n\n", inline=False)
		embed.add_field(name="4", value=f"`$perks` - Display available perks and point investment into each one.\n\n"
										f"`$perks <clear, or perk and amount of points>` - $perks clear will remove all assigned points for redistribution. $perks cherishboost 5 will add 5 points (if available) to overall mystery gift roll chance.\n\n"
										f"`$boost <Pokémon>` - Will boost the catch rate of a particular Pokémon, if at least one SpeciesBoost perk has been added. $boost Charizard would slightly increase the chance of Charizard appearing.\n\n"
										f"`$buddy` - Will display active buddy if you have one. If the buddy is an egg, it will hatch after a little while.\n\n"
										f"`$buddy <id>` - Will set the specified catch ID as your active buddy.\n\n", inline=False)
		embed.add_field(name="5", value=f"`$buddy remove` - Will remove the active buddy.\n\n"
										f"`$nickname <some text, or 'clear'>` - Will nickname an active buddy. If keyword 'clear' is used, it will remove the nickname.\n\n"
										f"`$evolve <optional parameter with item name or Alcremie form>` - Will evolve your active buddy, if applicable. To use an evolution item, specify an item name. To specify an Alcremie form if evolving Milcery, type in the form (e.g. Ice Stone for a usable item, Caramel Swirl for an Alcremie form; e.g. $evolve galarica cuff to evolve a Slowpoke-Galar to Slowbro-Galar).\n\n"
										f"`$giveitem <item name>` - Will give an item for your buddy to hold. Some evolutions require held items (e.g. $giveitem ice stone).\n\n"
										f"`$takeitem` - If your buddy is holding an item, it will remove it and place it back to your 'pouch'.\n\n", inline=False)
		embed.add_field(name="6", value=f"`$giftitem <item name> <item count> <user mention>` - Will gift an X amount of a specified item to the mentioned user (e.g. $giftitem ice stone 5 @user).\n\n"
										f"`$itemlist/$il <item name or 'all'>` - Similarly to $list, it will display items in your 'pouch' (e.g. $list ice stone).\n\n"
										f"`$dropitem/$drop <item name or 'all'>` - Will remove all of the specified item, or every single item you have (e.g. $drop ice stone).\n\n"
										f"`$timezone/$tz <UTC time offset>` - Will set the UTC time offset to the specified value. Can find out your offset by subtracting the local time from standard UTC time (e.g. $tz -5).", inline=False)

		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.send(embed=embed)

	@commands.command(name="raid_request_instructions", aliases=["rri"], hidden=True) 
	async def sysbot_instructions(self, ctx):
		"""A useful command that displays raid request instructions."""
		version = "v1.1.0"

		embed = nextcord.Embed(
			title="__**Raid Request Intructions**__",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		embed.add_field(name="**Step 1:**", value="Go to <#875571213844488223>", inline=False)
		embed.add_field(name="**Step 2:**", value="Use `.suggest [suggestion]` to submit a raid request", inline=False)
		embed.add_field(name="**Step 3:**", value="Wait for raid host to get to your suggestion", inline=False)
		embed.add_field(name="**EXAMPLE:**", value="`.suggest Den 157`")     
		await ctx.send(embed=embed)
  
	@commands.command(name="server_invite") 
	async def server_invite(self, ctx):
		"""A useful command that displays a permanent invite link."""
		embed = nextcord.Embed(
			title="__Permanent Invite Link__",
			description="https://discord.gg/dm7gSAT68d",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.send(embed=embed)

def setup(bot: commands.Bot):
	bot.add_cog(CustomCommands(bot))
