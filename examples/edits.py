import nextcord
import asyncio

from nextcord.ext import commands


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message_edit(self, before, after):
        msg = f'**{before.author}** edited their message:\n{before.content} -> {after.content}'
        await before.channel.send(msg)

bot = Bot(command_prefix='$')

@bot.command()
async def editme(ctx):
    msg = await ctx.send('10')
    await asyncio.sleep(3.0)
    await msg.edit(content='40')


bot.run('token')
