import nextcord
from nextcord.ext import commands

class Channel(commands.Cog, name="Channel"):
	"""Channel Commands"""
	def __init__(self, bot: commands.Bot):
		self.bot = bot

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
  	
	@ch.command(name="lock")
	@commands.has_permissions(manage_channels=True)
	async def lock(self, ctx, *, channel: nextcord.TextChannel = None):
		"Lock the channel."
		if channel == None:
			channel = ctx.message.channel
		await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked {channel.name} with --server", send_messages=False, read_messages=None, view_channel=None)
		await ctx.channel.trigger_typing()
		await channel.send(f"{channel.mention} has been locked 🔒")

	@ch.command(name="unlock")
	@commands.has_permissions(manage_channels=True)
	async def unlock(self, ctx, *, channel: nextcord.TextChannel = None):
		"""Unlock the channel."""
		if channel == None:
			channel = ctx.message.channel
		await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} unlocked {channel.name}", send_messages=None, read_messages=None, view_channel=None)
		await ctx.channel.trigger_typing()
		await channel.send(f"{channel.mention} has been unlocked 🔓")

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
		"""Create a new category."""
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
		"""Create a new channel."""
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
		"""Delete a category."""
		await category.delete(reason=reason)
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey man! I deleted {category.name} for ya!")

	@delete.command(name='channel')
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def _channel(self, ctx, channel: nextcord.TextChannel=None, *, reason=None):
		"""Delete a channel."""
		channel = channel or ctx.channel
		await channel.delete(reason=reason)
		await ctx.channel.trigger_typing()
		await ctx.send(f"Hey man! I deleted {channel.name} for ya!")

	@commands.group(invoke_without_command=True)
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def embed(self, ctx):
		"""Embed messages."""
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
		"""Forkbot release link."""
		forkbot = nextcord.Embed(title=f"__ForkBot.NET Release__", url="https://dev.azure.com/koigithub3088/SysBot_KoiFork/_build?definitionId=2&_a=summary", description="sys-botbase client for remote control automation of Nintendo Switch consoles. - Home · Koi-3088/ForkBot.NET Wiki")
		forkbot.set_thumbnail(url="https://cdn.mee6.xyz/guild-images/829558837609889804/ab3f13c97f829fe30ddcb9d8d4a9da4c7d17e2ebedf54ff60d51eb95947084b4.gif")
		forkbot.set_image(url="https://cdn-longterm.mee6.xyz/guild-images/829558837609889804/3edbea766c12a30e4540cb729a5bb50608a8866dbdcd18c55e25458d188c9784.png")
		forkbot.set_author(name=f"Frogadier Mod", icon_url="https://cdn.discordapp.com/avatars/892620195342987274/cb32b40409c7df4d147c400582f939ac.webp?size=128")
		await ctx.send(embed=forkbot)

	@embed.command(name="server_navigation")
	@commands.guild_only()
	@commands.has_role(829942684947841024)
	async def server_navigation(self, ctx):
		"""Server navigation embed."""
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

def setup(bot: commands.Bot):
	bot.add_cog(Channel(bot))
