import random
from typing import Optional
import nextcord, datetime
import nextcord.errors
from nextcord.ext import commands
from datetime import time
from nextcord.ext.commands import MissingPermissions
import asyncio
from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional
from better_profanity import profanity
from nextcord import Embed, Member, NotFound, Object
from nextcord.utils import find
from nextcord.ext.commands import Cog, Greedy, Converter
from nextcord.ext.commands import CheckFailure, BadArgument
from nextcord.ext.commands import command, has_permissions, bot_has_permissions
from nextcord.ext import commands
from db import db
import requests
import json

class Support(commands.Cog, name="Support"):
		"""Channel commands"""

def __init__(self, bot: commands.Bot):
	self.bot = bot

	@commands.command(name="support")
	async def support(self, ctx, *, reason = None):
		guildid = ctx.guild.id
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
		await channel.send(f"{user.mention}")
		supem = nextcord.Embed(title=f"{user} requested support.", description= "", color=0x00ff00)
		supem.add_field(name="Reason", value=f"``{reason}``")
		supem.set_footer(text=f"Either an admin or support staff will be with you shortly...")
		await channel.send(embed=supem)
	 
def setup(bot: commands.Bot):
	bot.add_cog(Support(bot))