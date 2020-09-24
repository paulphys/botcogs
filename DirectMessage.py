import discord
from discord.ext import commands

class DirectMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def dm(self,ctx, member: discord.Member, *, content):
        channel = await member.create_dm() # creates a DM channel for mentioned user
        await channel.send(content) # send whatever in the content to the mentioned user.

    #Send a message as someone else#
    @commands.command()
    async def quote(self, ctx, member: discord.Member, *, message: commands.clean_content()):
        webhook = await ctx.channel.create_webhook(name=member.display_name)
        await webhook.send(message, avatar_url=member.avatar_url_as(format='png'))
        await webhook.delete()
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.HTTPException):
            pass

def setup(bot):
    bot.add_cog(DirectMessage(bot))