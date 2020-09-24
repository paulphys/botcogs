import discord
from discord.ext import commands
import praw

reddit = praw.Reddit(client_id='id',
                     client_secret='secret',
                     user_agent='windows 10: Meme Scraper (by /u/PotatoLord1207)')


class RedditIntegration(commands.Cog, name='Reddit'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='redditmeme')
    async def meme(self, ctx,subreddit_raw: str = None):
        if subreddit_raw:
            embed = discord.Embed(title="some title if you want", description=f'some description if you want',
                              colour=discord.Colour(0x0AFA02))
            embed_list = '' 
            for submission in reddit.subreddit(subreddit_raw).hot(limit=3):
                if not submission.over_18 and not submission.stickied: #put them together
                    embed_list += f'{submission.url} \n\n' #new line at end of string
            print(embed_list)
            embed.add_field(name='urls', value=embed_list)
            await ctx.send(embed=embed)

        else:
            await ctx.send('please provide a subreddit')



    
def setup(bot):
    bot.add_cog(RedditIntegration(bot))
