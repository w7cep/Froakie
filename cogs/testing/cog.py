DB_HOST = "ec2-34-196-34-142.compute-1.amazonaws.com"
DB_NAME = "dt0eoc4qkg069"
DB_USER = "ghcwcqouluyzad"
DB_PASS = "56d59cc9563df874d5ec6a3b85a7ac40b648e20d18580ad62ea88134534159a2"

import random
from typing import Optional

import nextcord
from aiohttp import request
from nextcord import Embed, Member
from nextcord.ext import commands
from nextcord.ext.commands import BadArgument
import psycopg2
import psycopg2.extras

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
class Testing(commands.Cog, name="Testing"):
	"""Test commands"""

	def __init__(self, bot: commands.Bot):
		self.bot = bot
  
	@commands.command()
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def warn_db(self, ctx,):  
		with conn:
			with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
		
				cur.execute("CREATE TABLE warnings (id SERIAL PRIMARY KEY, name VARCHAR);")
				await ctx.send("Database created")
		conn.close()
		
	'''	
	@commands.command(name="add", descripton="Adds two numbers together.", hidden=True)
	async def add(ctx, left: int, right: int):
			await ctx.send(left + right)

	@commands.command(
		 name="repeat",
		description="Repeat a message a number of times.", hidden=True
	)
	async def repeat(ctx, times: int, content='repeating...'):
			for i in range(times):
				await ctx.send(content)
    '''

def setup(bot: commands.Bot):
	bot.add_cog(Testing(bot))
