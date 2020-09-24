import discord
from discord.ext import commands
import datetime
import googletrans
from utils.global_utils import upload_hastebin, bright_color

class LanguageProcessing(commands.Cog, name='NLP'):
    def __init__(self, bot):
        self.bot = bot
        self.translator = googletrans.Translator()

    @commands.command(pass_context=True)
    async def translate(self, ctx, *, text: commands.clean_content=None):
        """Translates a message to English using Google translate.
        If no message is given, find the last message with text"""
        if text is None:
            async for message in ctx.channel.history(limit=25, before=ctx.message):
                if message.content:
                    text = message.content
                    break
            if text is None:
                return await ctx.send('Unable to find text to translate!')
        loop = self.bot.loop
        try:
            res = await loop.run_in_executor(None, self.translator.translate, text)
        except Exception as e:
            return await ctx.send(f'An error occurred: {e.__class__.__name__}: {e}')

        embed = discord.Embed(title='Translated', color=bright_color())
        src = googletrans.LANGUAGES.get(res.src, '(auto-detected)').title()
        dest = googletrans.LANGUAGES.get(res.dest, 'Unknown').title()
        original = res.origin if len(res.origin) < 1024 else f'[Text too long to send, uploaded instead]({await upload_hastebin(ctx, res.origin)})'
        translated = res.text if len(res.text) < 1024 else f'[Text too long to send, uploaded instead]({await upload_hastebin(ctx, res.text)})'
        embed.add_field(name=f'From {src}', value=original, inline=False)
        embed.add_field(name=f'To {dest}', value=translated, inline=False)
        if len(res.origin) > 1024 or len(res.text) > 1024:
            embed.description = 'Text too long to send, uploaded instead'
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LanguageProcessing(bot))