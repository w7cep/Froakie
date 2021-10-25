import config
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import MissingPermissions

from .confirm_view import ConfirmView
from .self_role_view import SelfRoleView
from .sysbot_role_view import SysBotRuleView

"""//TODO Refine reaction roles"""
class ButtonRolesCog(commands.Cog, name="Roles"):
	"""Give and remove roles based on button presses"""

	def __init__(self, bot: commands.Bot):
		self.__bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		"""When the bot is ready, load the role views"""
		# skip this function if views are already added
		if self.__bot.persistent_views_added:
			return
		self.__bot.add_view(SelfRoleView())
		self.__bot.add_view(ConfirmView())
		self.__bot.add_view(SysBotRuleView())
		# set flag
		self.__bot.persistent_views_added = True
		print("Button views added")

	@commands.command()
	@commands.is_owner()
	async def sysbot_roles(self, ctx: commands.Context, message_id: str):
		"""Starts a bot role view"""
		bot_rules_channel = await ctx.guild.fetch_channel(config.BOT_RULES_CHANNEL_ID)
		message = await bot_rules_channel.fetch_message(message_id)
		await message.edit(view=SysBotRuleView())
  
	@commands.command()
	@commands.is_owner()
	async def roles(self, ctx: commands.Context):
		"""Starts a role view"""
		embed=nextcord.Embed(
			title="Click on a button to select a role"
		)
		embed.add_thumbnail(file=nextcord.File("assets/imgs/greninja-frogadier.gif"))
		embed.add_field(name="**General Access**", value=	f"**SysBot Channel Access**: Giveaway\n"
                 											f"**TradeCord Channel Access**: TradeCord")
		await ctx.send(embed=embed, view=SelfRoleView())

	@commands.command()
	@commands.is_owner()
	async def add_confirm(self, ctx: commands.Context, message_id: str):
		"""Starts a confirm view"""
		rules_channel = await ctx.guild.fetch_channel(config.RULES_CHANNEL_ID)
		message = await rules_channel.fetch_message(message_id)
		await message.edit(view=ConfirmView())
		
	@commands.command(name="role")
	@commands.has_permissions(administrator=True) #permissions
	async def role(self, ctx, user : nextcord.Member, *, role : nextcord.Role):
		'''Give role to member.'''
		if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
			return await ctx.send('**:x: | That role is above your top role!**')
		if role in user.roles:
			await user.remove_roles(role) #removes the role if user already has
			await ctx.send(f"Removed {role} from {user.mention}") 
		else:
			await user.add_roles(role) #adds role if not already has it
			await ctx.send(f"Added {role} to {user.mention}")
			
	@role.error
	async def role_error(self, ctx, error):
		if isinstance(error, MissingPermissions):
			await ctx.send('**:x: | You do not have permission to use this command!**')
			
		


# setup functions for bot
def setup(bot):
	bot.add_cog(ButtonRolesCog(bot))
