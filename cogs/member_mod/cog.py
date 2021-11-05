import nextcord, datetime
import nextcord.errors
from better_profanity import profanity
from nextcord.ext import commands, tasks
from nextcord.ext.commands import MissingPermissions
import aiohttp
from io import BytesIO

profanity.load_censor_words_from_file("./data/profanity.txt")

# This prevents staff members from being punished 
class Sinner(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
		permission = argument.guild_permissions.manage_messages # can change into any permission
		if not permission: # checks if user has the permission
			return argument # returns user object
		else:
			raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member

# Checks if you have a muted role
class Redeemed(commands.Converter):
	async def convert(self, ctx, argument):
		argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
		muted = nextcord.utils.get(ctx.guild.roles, name="Muted") # gets role object
		if muted in argument.roles: # checks if user has muted role
			return argument # returns member object if there is muted role
		else:
			raise commands.BadArgument("The user was not muted.") # self-explainatory
			
# Checks if there is a muted role on the server and creates one if there isn't
async def mute(ctx, user, reason):
	role = nextcord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
	await user.add_roles(role)
	await ctx.channel.trigger_typing()# adds already existing muted role
	await ctx.send(f"{user.mention} has been muted for {reason}")

class Moderation(commands.Cog, name="Moderation"):
	"""Moderation commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.bot_reminder.start()

		self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
	
	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def member(self, ctx):
		await ctx.send("Invalid sub-command specified")
 
	@member.command(name="ban")
	@commands.has_role(829942684947841024)
	async def ban(self, ctx, id: int):
		"""Ban a user from the server."""
		user = await self.bot.fetch_user(id)
		await ctx.guild.ban(user)

		ban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		ban.add_field(name='User Affected:', value=f'`{user.name}{user.discriminator}`', inline=True)
		ban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		ban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		ban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		ban.add_field(name='Action Performed:', value='`Ban`', inline=True)
		ban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		ban.set_thumbnail(url=user.avatar.url)
		ban.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		ban.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=ban)

	@member.command(name="softban")
	@commands.has_role(829942684947841024) 
	async def softban(self, ctx, id: int):
		"""Softban a user from the server."""
		user = await self.bot.fetch_user(id)

		softban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		softban.add_field(name='User Affected:', value=f'`{user.name}{user.discriminator}`', inline=True)
		softban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		softban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		softban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		softban.add_field(name='Action Performed:', value='`Softban`', inline=True)
		softban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		softban.set_thumbnail(url=user.avatar.url)
		softban.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		softban.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		await ctx.guild.ban(user)
		await ctx.guild.unban(user)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=softban)
	
	@member.command(name="unban")
	@commands.has_role(829942684947841024)
	async def unban(self, ctx, id: int):
		"""Unban a user from the server."""
		user = await self.bot.fetch_user(id)
		await ctx.guild.unban(user)

		unban= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		unban.add_field(name='User Affected:', value=f'`{user.name}{user.discriminator}`', inline=True)
		unban.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		unban.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=False)
		unban.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		unban.add_field(name='Action Performed:', value='`Unban`', inline=True)
		unban.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		unban.set_thumbnail(url=user.avatar.url)
		unban.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		unban.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=unban)

	@member.command(name="kick")
	@commands.has_role(829942684947841024)
	async def kick(self, ctx, id: int):
		"""Kick a user from the server."""
		user = await self.bot.fetch_user(id)
		await ctx.guild.kick(user)

		kick= nextcord.Embed(title=f'A moderation action has been performed!', description='', color=0x90fd05)
		kick.add_field(name='User Affected:', value=f'`{user.name}{user.discriminator}`', inline=True)
		kick.add_field(name='User ID:', value=f'`{user.id}`', inline=True)
		kick.add_field(name='Moderator Name:', value=f'`{ctx.author}`', inline=True)
		kick.add_field(name='Moderator ID:', value=f'`{ctx.author.id}`', inline=True)
		kick.add_field(name='Action Performed:', value='`Kick`', inline=True)
		kick.set_author(name=f'{ctx.guild}', icon_url=ctx.guild.icon.url)
		kick.set_thumbnail(url=user.avatar.url)
		kick.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		kick.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=kick)

	@member.command(name="mute")
	@commands.has_role(829942684947841024) 
	async def mute(self, ctx, user: Sinner, reason=None):
		"""Gives them hell."""
		await mute(ctx, user, reason or "being sus") # uses the mute function

	@member.command(name="unmute")
	@commands.has_role(829942684947841024)
	async def unmute(self, ctx, user: Redeemed):
		"""Unmutes a muted user"""
		await user.remove_roles(nextcord.utils.get(ctx.guild.roles, name="Muted"))
		await ctx.channel.trigger_typing()# removes muted role
		await ctx.send(f"{user.mention} has been unmuted")

	# TODO #4 Make: temp_mute command
	# TODO #5 Add: """docstring to the block and unblock commands"""

	@member.command(name="block")
	@commands.has_role(829942684947841024) 
	async def block(self, ctx, user: Sinner=None, channel: nextcord.TextChannel = None, reason = None):

		if not user: # checks if there is user
			return await ctx.send("You must specify a user")
		if channel == None:
			channel = ctx.channel
		if reason == None:
			reason = "no reason"
		await channel.set_permissions(user, send_messages=False, view_channel=True, read_message_history=True)# sets permissions for current channel
		await ctx.channel.trigger_typing()
		await channel.send(f"🚫{user.mention} has been blocked in {channel.mention} 🚫 for {reason}")

	@member.command(name="unblock")
	@commands.has_role(829942684947841024) 
	async def unblock(self, ctx, user: Sinner=None, channel: nextcord.TextChannel = None, reason = None):

		if not user: # checks if there is user
			return await ctx.send("You must specify a user")
		if channel == None:
			channel = ctx.channel

		await channel.set_permissions(user, send_messages=None, view_channel=None, read_message_history=None) # sets permissions for current channel
		await ctx.channel.trigger_typing()
		await channel.send(f"✅{user.mention} has been unblocked in {channel.mention}✅")

	@member.command(name="addrole")
	@commands.is_owner() #permissions
	async def give_role(self, ctx, user : nextcord.Member, *, role : nextcord.Role):
		"""Give role to member."""
		if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
			return await ctx.send('**:x: | That role is above your top role!**')
		if role in user.roles:
			await user.remove_roles(role) #removes the role if user already has
			await ctx.send(f"Removed {role} from {user.mention}") 
		else:
			await user.add_roles(role) #adds role if not already has it
		await ctx.channel.trigger_typing()
		await ctx.send(f"Added {role} to {user.mention}")

	@give_role.error
	async def role_error(self, ctx, error):
		if isinstance(error, MissingPermissions):
			await ctx.channel.trigger_typing()
			await ctx.send('**:x: | You do not have permission to use this command!**')

	@member.command(name="info") 
	@commands.has_role(829942684947841024)
	@commands.guild_only()
	async def memberinfo(self, ctx, *, user : nextcord.Member = None):

		"""
		Get information about you, or a specified user.
		`$$ui <user>`
		`user`: The user who you want information about. Can be an ID, mention or name.
		"""
		if user is None:
			user = ctx.author

		embed = nextcord.Embed(title=f"{user.name}'s Stats and Information.")
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"ID: {user.id}")
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		embed.add_field(name="__**ID:**__", value=f"{user.id}")
		embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user}\n"
																   f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}", inline=False)
		embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
																		  f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
																		  f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}")
		await ctx.channel.trigger_typing()
		return await ctx.send(embed=embed)

	@tasks.loop(hours=8)  # you can even use hours and minutes
	async def bot_reminder(self):
		print("Sending message")
		channel = self.bot.get_channel(843271842931933224)
		await channel.send("**Reminder**\n\nUsing the bot is fun, to keep it fun for everyone, please complete your trade with the bot. Even when making a mistake and you've started the trade, complete it.\nSee it as a free item and fodder you don't have to catch.\n\nPlease don't delete messages. Even when it's a mistake.\nMakes trouble-shooting difficult.\n\nBot access will be revoked for multiple offenders.")

	@bot_reminder.before_loop
	async def before_bot_reminder(self):
		print('waiting...')
		await self.bot.wait_until_ready()

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def profanity(self, ctx):
		await ctx.send("Invalid sub-command specified")
	
	@profanity.command(name="add")
	@commands.has_role(829942684947841024)
	async def add(self, ctx, *words):
		'''Add cuss word to file.'''
		with open("./data/profanity.txt", "a", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.channel.trigger_typing()
		await ctx.send("Action complete.")

	@profanity.command(name="del")
	@commands.has_role(829942684947841024)
	async def remove_profanity(self, ctx, *words):
		'''Delete cuss word from file.'''
		with open("./data/profanity.txt", "r", encoding="utf-8") as f:
			stored = [w.strip() for w in f.readlines()]

		with open("./data/profanity.txt", "w", encoding="utf-8") as f:
			f.write("".join([f"{w}\n" for w in stored if w not in words]))

		profanity.load_censor_words_from_file("./data/profanity.txt")
		await ctx.channel.trigger_typing()
		await ctx.send("Action complete.")

	@commands.Cog.listener()
	async def on_message(self, message):
		def _check(m):
			return (m.author == message.author
					and len(m.mentions)
					and (datetime.utcnow()-m.created_at).seconds < 60)

		if profanity.contains_profanity(message.content):
			await message.delete()
			await message.channel.send("You can't use that word here.", delete_after=10)

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def embed(self, ctx):
		await ctx.send("Invalid sub-command specified")

	@embed.command(name="sysbot_access")
	@commands.is_owner()
	async def sysbot_access(self, ctx):
		"""Sysbot access embed."""
		embed=nextcord.Embed(title="__**Sysbot Access**__", 
							description=f"Check out <#868914000572846120> for access to the sysbot.\n")
		embed.add_field(name="__**Reminder**__", value="Don't delete messages in the bot channel. It makes it harder to trouble shoot problems with the bot.")
	   
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_author(name="Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		embed.set_footer(text="Bot is running v1.0.0") 
		await ctx.channel.trigger_typing() 
		await ctx.send(embed=embed)

	@embed.command(name="forkbot_release")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def forkbot_release(self, ctx):
		forkbot = nextcord.Embed(title=f"__ForkBot.NET Release__", url="https://dev.azure.com/koigithub3088/SysBot_KoiFork/_build?definitionId=2&_a=summary", description="sys-botbase client for remote control automation of Nintendo Switch consoles. - Home · Koi-3088/ForkBot.NET Wiki")
		forkbot.set_thumbnail(url="https://cdn.mee6.xyz/guild-images/829558837609889804/ab3f13c97f829fe30ddcb9d8d4a9da4c7d17e2ebedf54ff60d51eb95947084b4.gif")
		forkbot.set_image(url="https://cdn-longterm.mee6.xyz/guild-images/829558837609889804/3edbea766c12a30e4540cb729a5bb50608a8866dbdcd18c55e25458d188c9784.png")
		forkbot.set_author(name=f"Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		await ctx.send(embed=forkbot)

	@embed.command(name="server_navigation")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def server_navigation(self, ctx):
		version = "1.1.0"
		navigation = nextcord.Embed(title="__Navigating the server__")
		navigation.set_footer(text=f"{version}")
		navigation.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		navigation.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		navigation.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		navigation.add_field(name="#📃rules📃", value="• First channel you see, right after #👋welcome👋. \n• To get out and view the whole server, react to the rules with :thumbsup:", inline=False)
		navigation.add_field(name="#📡get-roles📡", value="• Pick up any roles you'd like, first category is the only that will receive pings. \n• Other categories are optional, not obligatory. \n• Pronouns are to be respected", inline=False)
		navigation.add_field(name="#🧾bot-rules🧾", value="• The rules of #🤖greninja-bot🤖 . \n• React with either 🤖 or 🎁  in #🧾bot-rules🧾 for access", inline=False)
		navigation.add_field(name="#tradecord", value="• Instructions: `!tci` / #❓tradecord-instructions❓.\n• Our version of Pokécord",inline=False)
		navigation.add_field(name="#🤖greninja-bot🤖", value="• Prefix:`$`.\n• Instructions: #❓greninja-bot-instructions❓.\n• Generate any Pokémon in SwSh, illegals won't work (List of illegals `!illegal`.", inline=False)
		navigation.add_field(name="#📥request-a-mon📥", value="• Request any Pokémon, we'll provide a PK8 file asap", inline=False)
		navigation.add_field(name="#🛰auto-hosting🛰", value="• Where the host will post their raid info.\n\n#💭host-request💭  \n•Use `.suggest  <Your suggestion here>` to suggest a shiny den or max lair path.", inline=False)
		navigation.add_field(name="#💭host-request💭", value="• Use `!request <Your suggestion here>` to request a Den or Max Lair Path.", inline=False)
		navigation.add_field(name="__**Support**__", value="• Use `!support` to open a support channel\n• An @💪Admin💪 or @💪Moderator💪 will be with you shortly.")
		await ctx.send(embed=navigation)

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def ch(self, ctx):
		"""Channel mod commands"""
		await ctx.channel.trigger_typing()
		await ctx.send("Invalid sub-command passed")

	@ch.command(name="purge")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def purge(self, ctx, amount=5):
		"""Purge a number of messages in a channel"""
		if amount is None:
			await ctx.send("Please specify a number of messages to purge")
		else:
			await ctx.channel.purge(limit=amount + 1)
			embed = nextcord.Embed(
				title=f"{ctx.author.name} purged: {ctx.channel.name}",
				description=f"{amount} messages were cleared",
			)
			await ctx.channel.trigger_typing()
		await ctx.send(embed=embed, delete_after=5)

	@ch.command(name="clean")
	@commands.has_role(829942684947841024)
	async def clean(self, ctx):
		"""Cleans the chat of the bot's messages."""
		def is_me(m):
			return m.author == self.bot.user
		await ctx.channel.trigger_typing()
		await ctx.message.channel.purge(limit=100, check=is_me)
  	
	@ch.command(name="lockdown")
	@commands.has_permissions(manage_channels=True)
	async def lock(self, ctx, *, channel: nextcord.TextChannel = None):
		"Lock the channel"
		if channel == None:
			channel = ctx.message.channel
		await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name} with --server", send_messages=False, read_messages=None, view_channel=None)
		await ctx.channel.trigger_typing()
		await channel.send(f"{channel.mention} has been locked 🔒")

	@ch.command(name="unlockdown")
	@commands.has_permissions(manage_channels=True)
	async def unlock(self, ctx, *, channel: nextcord.TextChannel = None):
		"""Unlock the channel"""
		if channel == None:
			channel = ctx.message.channel
		await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name}", send_messages=None, read_messages=None, view_channel=None)
		await ctx.channel.trigger_typing()
		await channel.send(f"{channel.mention} has been unlocked 🔓")

	@commands.command(name="lock")
	@commands.guild_only()
	@commands.has_permissions(manage_channels=True)
	async def lockdown(self, ctx, channel : nextcord.TextChannel = None, setting = None):

		if channel == None:
			channel = ctx.message.channel
		await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name} with --server", send_messages=False, read_messages=None, view_channel=None)
		await ctx.channel.trigger_typing()
		await channel.send(f"{channel.mention} has been locked 🔒")
  
		if setting == '--server':
			for channel in ctx.guild.channels:
				await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name} with --server", send_messages=False, read_messages=None, view_channel=None)
			await ctx.send('locked down server 🔒')

	@commands.command(name="unlock")
	@commands.guild_only()
	@commands.has_permissions(manage_channels=True)
	async def unlockdown(self, ctx, channel : nextcord.TextChannel = None, setting = None):

		if channel == None:
			channel = ctx.message.channel
		await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name}", send_messages=None, read_messages=None, view_channel=None)
		await ctx.channel.trigger_typing()
		await channel.send(f"{channel.mention} has been unlocked 🔓")

		if setting == '--server':
			for channel in ctx.guild.channels:
				await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name} with --server", send_messages=None, read_messages=None, view_channel=None)
			await ctx.send('unlocked server 🔒')

	@ch.command(name="stats")
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def stats(self, ctx):
		"""
		Sends a nice fancy embed with some channel stats
		"""
		channel = ctx.channel
		embed = nextcord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",)
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/891852099653083186/895902400416710666/greninja-frogadier.gif")
		embed.set_image(url="https://cdn.discordapp.com/attachments/859634488593743892/891612213654192168/greninja_banner.jpg")
		embed.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
		embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
		embed.add_field(name="Channel Id", value=channel.id, inline=False)
		embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
		embed.add_field(name="Channel Position", value=channel.position, inline=False)
		embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
		embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
		embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
		embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
		embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
		#!FIX: #3 embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)

	@lock.error
	async def lock_error(ctx, error):
		if isinstance(error,commands.CheckFailure):
			await ctx.send('You do not have permission to use this command!')
   
	@ch.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def new(self, ctx):
		"""Create new channels and categories.
		($$new category @role "name of category")
		($$new channel @role "name of channel")
		"""
		await ctx.channel.trigger_typing()
		await ctx.send("Invalid sub-command passed.")

	@new.command()
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def category(self, ctx, role: nextcord.Role, *, name):
		overwrites = {
		ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
		ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
		role: nextcord.PermissionOverwrite(read_messages=True)
		}
		category = await ctx.guild.create_category(name=name, overwrites=overwrites)
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey dude, I made {category.name} for ya!")

	@new.command()
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def channel(self, ctx, role: nextcord.Role, *, name):
		overwrites = {
		ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
		ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
		role: nextcord.PermissionOverwrite(read_messages=True)
		}
		channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites, category=self.bot.get_channel(709002944879656960))
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey dude, I made {channel.name} for ya!")

	@ch.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def delete(self, ctx):
		"""Delete channels and categories.
		($$delete category @role "name of category")
		($$delete channel @role "name of channel")
		"""   
		await ctx.channel.trigger_typing()
		await ctx.send("Invalid sub-command passed.")

	@delete.command(name='category')
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def _category(self, ctx, category: nextcord.CategoryChannel, *, reason=None):
		await category.delete(reason=reason)
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey man! I deleted {category.name} for ya!")

	@delete.command(name='channel')
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def _channel(self, ctx, channel: nextcord.TextChannel=None, *, reason=None):
		channel = channel or ctx.channel
		await channel.delete(reason=reason)
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey man! I deleted {channel.name} for ya!")  

	@commands.command()
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def toggle(self, ctx, *, command):
		command = self.bot.get_command(command)
		if command == None:
			await ctx.send('couldnt find that command ._.')
		elif ctx.command == command:
			await ctx.send('you can not disable this command._.')
		else:
			command.enabled = not command.enabled
			ternary = "enabled" if command.enabled else "disabled"
			await ctx.send(f'command {command.qualified_name} has been {ternary}')

def setup(bot: commands.Bot):
	bot.add_cog(Moderation(bot))
	