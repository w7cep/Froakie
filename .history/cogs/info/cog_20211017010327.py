import nextcord
import platform
from nextcord.ext import commands
from nextcord.member import Member

class Information(commands.Cog, name="Information"):
	"""Information commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(
		name="stats", 
		  description="A useful command that displays bot statistics."
	)
	async def stats(self, ctx):
		pythonVersion = platform.python_version()
		dpyVersion = nextcord.__version__
		serverCount = len(self.bot.guilds)
		memberCount = len(set(self.bot.get_all_members()))
		version = "v1.0.0"
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

		embed.set_footer(text=f"{ctx.author.name}")
		embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)

		await ctx.send(embed=embed)
   
	@commands.command(name="wiki")
	@commands.guild_only()
	async def wiki(self, ctx, msg):
		"""Get info from wikipedia."""
		url: str = f"https://wikipedia.org/wiki/{msg}"
		await ctx.send(f"Here : {url}")
  
	@commands.command(name="memberinfo", aliases=["mi"]) 
	@commands.has_permissions(administrator=True)
	@commands.guild_only()
	async def memberinfo(self, ctx, *, user am : Member = None):
		
		"""
		Get information about you, or a specified user.
		`$$mi <user>`
		`user`: The user who you want information about. Can be an ID, mention or name.
		"""

		if user is None:
			user = ctx.author
			
		embed = nextcord.Embed(
			
			title=f"{user.name}'s Stats and Information.",
			
		)
		embed.set_footer(text=f"ID: {user.id}")
		embed.set_thumbnail(url=user.avatar.url(format="png"))
		embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user}\n"
																   f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}", inline=False)        
		embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
																		  f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
																		  f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}")
		return await ctx.send(embed=embed)

	@commands.command(name="emojiinfo", aliases=["ei"])
	@commands.has_permissions(administrator=True)
	async def emoji_info(self, ctx, emoji: nextcord.Emoji = None):
		if not emoji:
					await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

		try:
					emoji = await emoji.guild.fetch_emoji(emoji.id)
		except nextcord.NotFound:
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
		await ctx.send(embed=embed)
		
	@commands.command(aliases=['cs'])
	@commands.has_permissions(administrator=True)
	@commands.bot_has_guild_permissions(manage_channels=True)
	async def channelstats(self, ctx):
		"""
		Sends a nice fancy embed with some channel stats
		"""
		channel = ctx.channel
		embed = nextcord.Embed(title=f"Stats for **{channel.name}**", description=f"{'Category: {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",)
		embed.add_field(name="Channel Guild", value=ctx.guild.name, inline=False)
		embed.add_field(name="Channel Id", value=channel.id, inline=False)
		embed.add_field(name="Channel Topic", value=f"{channel.topic if channel.topic else 'No topic.'}", inline=False)
		embed.add_field(name="Channel Position", value=channel.position, inline=False)
		embed.add_field(name="Channel Slowmode Delay", value=channel.slowmode_delay, inline=False)
		embed.add_field(name="Channel is nsfw?", value=channel.is_nsfw(), inline=False)
		embed.add_field(name="Channel is news?", value=channel.is_news(), inline=False)
		embed.add_field(name="Channel Creation Time", value=channel.created_at, inline=False)
		embed.add_field(name="Channel Permissions Synced", value=channel.permissions_synced, inline=False)
		embed.add_field(name="Channel Hash", value=hash(channel), inline=False)

		await ctx.send(embed=embed)


def setup(bot: commands.Bot):
	bot.add_cog(Information(bot))        
		