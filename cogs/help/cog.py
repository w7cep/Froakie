import nextcord
from nextcord.ext import commands
import platform
from .help_command import NewHelpCommand


class HelpCog(commands.Cog, name="Help"):
	"""Displays help information for commands and cogs"""

	def __init__(self, bot: commands.Bot):
		self.__bot = bot
		self.__original_help_command = bot.help_command
		bot.help_command = NewHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.__bot.help_command = self.__original_help_command

	@commands.command(name="support")
	async def support(self, ctx, *, reason = None):
		"""Command to get support from the Admins."""
		guild = ctx.guild
		user = ctx.author
		amount2 = 1
		await ctx.channel.purge(limit=amount2)
		channel = await guild.create_text_channel(f'Ticket {user}')
		await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
		perms = channel.overwrites_for(user)
		await channel.set_permissions(user, view_channel=not perms.view_channel)
		await channel.set_permissions(user, read_message_history=not perms.read_message_history)
		await channel.set_permissions(user, send_messages=not perms.send_messages)
		await ctx.channel.trigger_typing()
		await channel.send(f"{user.mention}")
		embed = nextcord.Embed(title=f"{user} requested support.", description= "Either an admin or support staff will be with you shortly...", color=0x00ff00)
		embed.add_field(name="Reason", value=f"``{reason}``")
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name="Frogadier", icon_url="https://cdn.discordapp.com/attachments/891852099653083186/904941718200283146/Frogadier_Avatar.png")
		await ctx.channel.trigger_typing()
		await channel.send(embed=embed)

	@commands.command(name="ping")
	async def ping(self, ctx: commands.Context):
		"""Checks for a response from the bot"""
		await ctx.channel.trigger_typing()
		await ctx.send(f"Pong! (Latency: {round(self.bot.latency * 1000)}ms)")

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def instructions(self, ctx):
		"""Server instructions."""
		await ctx.send("invalid sub-command passed.")

	@instructions.command(name="pkhex")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def pkhex(self, ctx):
		"PKHeX Instructions"
		await ctx.send("Havvox#3700 guide to PKHeX: https://docs.google.com/document/d/1b3z8qCQ2mM4dfhbyGlkak6H0b0zuEaeQKy5mTHwdnug/edit?usp=sharing")

	@instructions.command(name="sysbot") 
	async def sysbot(self, ctx):
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
		embed.add_field(name="????How To Use A Sysbot**Part 1 - Showdown format**????", value="-Go to https://play.pokemonshowdown.com/teambuilder\n-In Format Tab Select 'Ubers' under 'SWSH'\n-Now Go To New Team'\n-You Should now see 'Add Pok??mon'\n-Either select or type the Pok??mon you want to create\n-You have control over stuff like the nickname, items, abilities, moveset\n-Now that you have finished the Pok??mon click validate to check that the import is legal\n-If you want to make sure the Pok??mon are usable in ranked/VGC and other online competitions for Format select VGC 2020\n-When everything is finished click Import/Export and copy the text\n-Type command of the sysbot then space and Paste the text in the bot channel\n\n-The sysbot will send a personal message aka DM to you with a Link Trade Code for an online trade in Sword or Shield.\n-Type the code the bot sent you and start searching, once found, trade the bot a junkmon (no trade evolutions or illegals).\n-Once the trade is complete cancel trade and you're all set.\n-The bot will then proceed to send you a PK8 file of the Pok??mon you sent.\n", inline=False)
		embed.add_field(name="????How To Use A Sysbot Part 2 - PK8 Files????", value="-Make, request or check #cloning-requests for PK8 files.\n-Type $trade and add the PK8 file as an attachment to the message in the bot channel.\n-The sysbot will send a personal message aka DM to you with a Link Trade Code for an online trade in Sword or Shield.\n-Type the code the bot sent you and start searching, once found, trade the bot a junkmon (no trade evolutions or illegals).\n-Once the trade is complete cancel trade and you're all set.\n-The bot will then proceed to send you a PK8 file of the Pok??mon you sent.\n\n-If you can't add a file to the message or you don't want to download a file, go back to Part 1.", inline=False)
		embed.add_field(name="????How To Use A Sysbot Part 3 - Clone????", value="-Type $clone in the bot channel.\n-The sysbot will send a personal message aka DM to you with a Link Trade Code for an online trade in Sword or Shield.\n-Type the code the bot sent you and start searching, once found, trade the bot the Pok??mon you want to clone.\n-The bot will message you to cancel the trade by pressing B. When done correctly, the bot will send you a PK8 file of the Pok??mon you want to clone.\n-Then trade the bot a junkmon (no trade evolutions or illegals).\n-Once the trade is complete cancel trade and you're all set.\n-The bot will then proceed to send you a PK8 file of the Pok??mon you sent.", inline=False)
		embed.add_field(name="__???? New bot, Extra commands!????__", value="`$trade, $t`\n__E.G.__\n```$trade Scorbunny (M) @ Life Orb\nAbility: Libero\nLevel: 5\nShiny: Square\nBall: Poke Ball\nOT: FreshBot\nOTGender: Male\nTID: 035481\nSID: 0231\nEVs: 116 HP / 188 Atk/ 204 Spe\nIVs: 30 SpA\nJolly Nature\n- Blaze Kick\n- Sucker Punch\n- Gunk Shot\n- High Jump Kick\n```", inline=False)
		embed.add_field(name="__We all know the random mon command__", value="`$ga random`\n-And when the pool has been released, the actual number of the one you want.\n`$ga ###`", inline=False)
		embed.add_field(name="__But it can do more!__", value="-Got a pesky admon and you want it fixed?\n-This will change the OT to yours. (You can trick the bot by renaming it to a website for any OT change)\n`$fixot, $fix`", inline=False)
		embed.add_field(name="__Want an egg?__", value="`$trade egg <showdown format>`\n__E.G.__\n```$trade egg (Scorbunny) (F)\nShiny: Square\nJolly Nature\n- Tackle\n- Growl\n- Sucker Punch\n- High Jump Kick```", inline=False)
		embed.add_field(name="_Reminder_", value="-Always ask for eggmoves, others will be illegal (or leave em blank when you just don't care)\n-Put brackets around the mon's name. ", inline=False)
		embed.add_field(name="__Unlimited items__", value="-Need an extra Master Ball or 20 or any other item?\n-The bot will send a Delibird with your item!\n`$itemtrade <item name>`\n`$item <item name>`\n`$it <item name>`\n__E.G.__\n`$item Beast Ball`", inline=False)
		embed.add_field(name="__Breeding Dittos__", value="`$dittotrade, $ditto, $dt <Stats> <Languages> <Nature>`\n\n`Stats:`\nChoosing one of these or all 3 will make that IV 0 or No Good. 6IV will always yield 31 or Best\n-ATK\n-SPA\n-SPE\n-6IV\n\nCombinations can be made, no spaces between them.\n__E.G.__\n'ATKSPE' will give you a ditto with 0 ATK & SPE\n`Language:`\nThese Locales in the games can be chosen:\n-Japanese\n-English\n-French\n-Italian\n-German\n`Nature:`\nHardy / Docile / Serious / Bashful\nQuirky / Lonely / Brave / Adamant\nNaughty / Bold / Relaxed / Impish\nLax / Modest / Mild / Quiet / Naive \nRash / Calm / Gentle / Sassy\nCareful / Timid / Hasty / Jolly\n\n__**E.G. of the full command:**__\n`$ditto ATKSPE Japanese Brave`\n-Will give you a 0 Speed Japanese Ditto with a Brave nature\n`$ditto 6IV German Timid`\n-Will give you a 6IV German Ditto with a Timid nature.", inline=False)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)

	@instructions.command(name="tradecord") 
	async def tradecord(self, ctx):
		"""A useful command that displays TradeCord instructions."""
		version = "v1.1.0"

		embed = nextcord.Embed(
			title=f"__Greninja SysBot Commands__",
			description=f"__**Commands:**__\n", 
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.add_field(name="1", value=f"`$catch / $k` - Will 'catch' a random Pok??mon with an optional (but highly recommended) cool down.\n\n"
										f"`$tc <catch id> / $tc <link code> <catch id>` - Trade a catch. File will be moved to a backup folder just in case.\n\n"
										f"`$tis` - Set custom trainer info via an attached .pk8 file. Type $tis, attach a file, send as one message. Bot will automatically set trainer info.\n\n"
										f"`$ti` - Display currently set trainer info.\n\n"
										f"`$list <name/shinies/all/egg/ball> / $l <name/shinies/all/egg/ball>` - Displays a list of specific species or a list of shinies a user has.\n\n", inline=False)
		embed.add_field(name="2", value=f"`$dc` - Display daycare.\n\n"
										f"`$dc w <catch id or 'all'> / $dc withdraw <catch id or 'all'>` - Withdraw a specific Pok??mon from daycare, or withdraw everything.\n\n"
										f"`$dc d <catch id> / $dc deposit <catch id>` - Deposit a specific Pok??mon to daycare.\n\n"
										f"`$release <catch id> / $r <catch id>` - Release a specific Pok??mon. File will be deleted.\n\n"
										f"`$massrelease <optional species-form, cherish or shiny>/ $mr <optional species-form, cherish or shiny>` - Will release everything that's not shiny, not a Ditto, not in a Cherish Ball, not in favorites, and not in daycare. If species and/or form specified, will release just that (still obeys prior criteria). Files will be deleted.\n\n", inline=False)
		embed.add_field(name="3", value=f"`$info <catch id> / $i <catch id>` - Displays a Showdown set for a specific Pok??mon.\n\n"
										f"`$gift <catch id> <@user> / $g <catch id> <@user>` - Gift a Pok??mon to another user. If the receiving user has fewer than 10 Dex completions and hasn't registered the Pok??mon being gifted, it will be registered to their Dex.\n\n"
										f"`$fav` - Displays a list of favorite Pok??mon.\n\n"
										f"`$fav <catch id or 'clear''>` - Adds a Pok??mon to favorites (or removes it if it's already added to favorites). If keyword 'clear' is entered, it will unfavorite everything. Favorite Pok??mon cannot be released or mass released.\n\n"
										f"`$dex <optional 'missing' parameter>` - Shows your TradeCordDex progress (catches, level), or a list of Pok??mon you haven't caught yet. Whenever a full dex is completed, level is increased. Levels can be used as points for perk selection.\n\n", inline=False)
		embed.add_field(name="4", value=f"`$perks` - Display available perks and point investment into each one.\n\n"
										f"`$perks <clear, or perk and amount of points>` - $perks clear will remove all assigned points for redistribution. $perks cherishboost 5 will add 5 points (if available) to overall mystery gift roll chance.\n\n"
										f"`$boost <Pok??mon>` - Will boost the catch rate of a particular Pok??mon, if at least one SpeciesBoost perk has been added. $boost Charizard would slightly increase the chance of Charizard appearing.\n\n"
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
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)

	@instructions.command(name="host_request")
	async def host_request(self, ctx):
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
		embed.add_field(name="**Step 2:**", value="Use `!request <suggestion>` to request a Den or Max Lair Path.", inline=False)
		embed.add_field(name="**Step 3:**", value="Wait for an admin to get to your suggestion", inline=False)
		embed.add_field(name="**EXAMPLE:**", value="`!request Den 127`\n`!request Tapu Koko`")
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	async def info(self, ctx):
		await ctx.send("Invalid sub-command specified")

	@info.command(name="stats") 
	async def stats(self, ctx):
		"""A useful command that displays bot statistics."""
		pythonVersion = platform.python_version()
		dpyVersion = nextcord.__version__
		serverCount = len(self.bot.guilds)
		memberCount = len(set(self.bot.get_all_members()))
		version = "v1.1.0"
		developer = "<@741118153299591240>"
		embed = nextcord.Embed(
			title=f"{self.bot.user.name} Stats",
			description="Useful stats.",
			colour=ctx.author.colour,
			timestamp=ctx.message.created_at,
		)
		embed.add_field(name="Bot Version:", value=version)
		embed.add_field(name="Python Version:", value=pythonVersion)
		embed.add_field(name="nextcord Version", value=dpyVersion)
		embed.add_field(name="Total Guilds:", value=serverCount)
		embed.add_field(name="Total Users:", value=memberCount)
		embed.add_field(name="Bot Developers:", value=developer)

		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)

	@info.command(name="wiki")
	@commands.guild_only()
	async def wiki(self, ctx, msg):
		"""Get info from wikipedia."""
		url: str = f"https://wikipedia.org/wiki/{msg}"
		await ctx.channel.trigger_typing()
		await ctx.send(f"Here : {url}")

	@info.command(name="emoji")
	@commands.has_role(829942684947841024)
	async def emoji(self, ctx, emoji: nextcord.Emoji = None):
		"""Display information about an emoji in the server."""
		if not emoji:
					await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

		try:
					emoji = await emoji.guild.fetch_emoji(emoji.id)
		except nextcord.NotFound:
					await ctx.channel.trigger_typing()
					await ctx.send("I could not find this emoji in the given guild.")

		is_managed = "Yes" if emoji.managed else "No"
		is_animated = "Yes" if emoji.animated else "No"
		requires_colons = "Yes" if emoji.require_colons else "No"
		creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
		can_use_emoji = (
			"Everyone"
			if not emoji.roles
			else " ".join(role.name for role in emoji.roles)
		)

		description = f"""
		**General:**
		**- Name:** {emoji.name}
		**- Id:** {emoji.id}
		**- URL:** [Link To Emoji]({emoji.url})
		**- Author:** {emoji.user.name}
		**- Time Created:** {creation_time}
		**- Usable by:** {can_use_emoji}
		
		**Other:**
		**- Animated:** {is_animated}
		**- Managed:** {is_managed}
		**- Requires Colons:** {requires_colons}
		**- Guild Name:** {emoji.guild.name}
		**- Guild Id:** {emoji.guild.id}
		"""

		embed = nextcord.Embed(
		title=f"**Emoji Information for:** `{emoji.name}`",
		description=description,
		colour=0xADD8E6,
		)
		embed.set_thumbnail(url=emoji.url)
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)


# setup functions for bot
def setup(bot: commands.Bot):
	bot.add_cog(HelpCog(bot))
