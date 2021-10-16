import nextcord
import platform
from nextcord.ext import commands

class Reactions(commands.Cog, name="Reactions"):
    """Reaction commands"""

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

def setup(bot: commands.Bot):
    bot.add_cog(Reactions(bot))        
        