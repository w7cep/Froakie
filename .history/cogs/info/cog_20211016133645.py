import nextcord
from nextcord.ext import commands

class Reactions(commands.Cog, name="Reactions"):
    """Reaction commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot



def setup(bot: commands.Bot):
    bot.add_cog(Reactions(bot))        
        