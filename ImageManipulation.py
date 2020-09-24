import discord
import requests
import random
import io
from PIL import Image
from typing import Optional
from discord.ext import commands
from utils.global_utils import bright_color, last_image, is_image
from config import WAIFU2X_KEY

API_URL = 'https://api.deepai.org/api/waifu2x'
HEADERS = {'api-key': WAIFU2X_KEY}


def make_more_jpeg(content,amount):
    img = Image.open(content)
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, "jpeg", quality=int(amount))
    buffer.seek(0)
    return buffer

class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def upscale(self, ctx, url=None):
        url = url or await last_image(ctx)
        if url is None:
            return await ctx.send('Unable to find an image')
        if not await is_image(ctx, url):
            return await ctx.send('That is not a valid image url')
        data = {
            'image': url
        }

        r = requests.post(API_URL,data=data,headers=HEADERS)
        upscaled_image = r.json()
        img_url = upscaled_image['output_url']
        if img_url is None:
            return await ctx.send('Failed')
        e = discord.Embed(colour=bright_color())
        e.set_image(url=img_url)
        e.set_author(name='Upscaled Image', url=img_url)
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    async def lastimage(self, ctx):
        url = await last_image(ctx)
        if url is None:
            return await ctx.send('Unable to find an image')
        e = discord.Embed(colour=bright_color())
        e.set_image(url=url)
        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    async def jpg(self, ctx,amount, url=None):
        url = url or await last_image(ctx)
        if url is None:
            return await ctx.send('Unable to find an image')
        if not await is_image(ctx, url):
            return await ctx.send('That is not a valid image url')
        async with self.bot.session.get(url) as resp:
            data = io.BytesIO(await resp.read())
        jpeg = make_more_jpeg(data,amount)
        await ctx.send(file=discord.File(jpeg, filename='more_jpeg.jpg'))

def setup(bot):
    bot.add_cog(ImageManipulation(bot))