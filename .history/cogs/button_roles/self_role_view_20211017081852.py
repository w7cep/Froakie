from cogs.button_roles.role_view import RoleView
from utils.utils import custom_id
import nextcord
import config

VIEW_NAME = "SelfRoleView"


class SelfRoleView(RoleView):
	def __init__(self):
		super().__init__(required_roles=[config.MEMBER_ROLE_ID])

	@nextcord.ui.button(
		label="TradeCord",
		emoji="<:switch:865465918069932063>",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.TRADECORD_ROLE_ID),
	)
	async def tradecord_button(self, button, interaction):
		await self.handle_click(button, interaction)
		
	@nextcord.ui.button(
		label="Giveaway Ping",
		emoji="<:tada:899298638570868776>",
		style=nextcord.ButtonStyle.blurple,
		# set custom id to be the bot name : the class name : the role id
		custom_id=custom_id(VIEW_NAME, config.GIVEAWAY_PING_ROLE_ID),
	)
	async def giveaway_ping_button(self, button, interaction):
		await self.handle_click(button, interaction)

	'''@nextcord.ui.button(
		label="Content Creator",
		emoji="✍",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.CONTENT_CREATOR_ROLE_ID),
	)
	async def content_creator_button(self, button, interaction):
		await self.handle_click(button, interaction)'''

	'''@nextcord.ui.button(
		label="YouTube Ping",
		emoji="🔔",
		style=nextcord.ButtonStyle.primary,
		custom_id=custom_id(VIEW_NAME, config.YOUTUBE_PING_ROLE_ID),
	)
	async def youtube_ping_button(self, button, interaction):
		await self.handle_click(button, interaction)'''
