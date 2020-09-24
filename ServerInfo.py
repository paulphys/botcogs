import discord
from discord.ext import commands
from typing import Optional
import datetime
from typing import Union
from utils.global_utils import bright_color
from utils.time import human_timedelta
from utils.converters import CaseInsensitiveMember, CachedUserID

class ServerInfo(commands.Cog, name='Info'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='serverinfo', aliases=['guildinfo'])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        roles = ['@everyone']
        roles.extend([role.mention for role in guild.roles[1:]])
        roles = ", ".join(roles)
        e = discord.Embed(title='Server Info', color=bright_color())
        e.set_author(icon_url=guild.icon_url, name=guild.name)
        e.add_field(name='ID', value=guild.id)
        e.add_field(name='Owner', value=guild.owner)
        e.add_field(name='Region', value=guild.region)
        e.add_field(name='Members', value=guild.member_count)
        e.add_field(name='Channels', value=f'{text_channels} Text | {voice_channels} Voice')
        e.add_field(name='Created', value=human_timedelta(guild.created_at))
        e.add_field(name='Roles', value=roles)
        await ctx.send(embed=e)

    
    @commands.command(name='shareall', hidden=True)
    async def sharescreen_all(self, ctx):
        """Returns all voice channel's video links"""

        template = f'https://discordapp.com/channels/{ctx.guild.id}/'
        links = [f'[{vc.name}]({template}{vc.id})' for vc in ctx.guild.voice_channels]
        formatted = discord.utils.escape_markdown('\n'.join(links))  # because some ppl like to have ||name|| for some reason

        e = discord.Embed(title="Video Links for all Voice Channels",
                          colour=6430916,
                          description=formatted)

        await ctx.send(embed=e)
        await ctx.send(f'You can use {ctx.prefix}share to get the link for a single voice channel or your current voice channel', delete_after=5)


    @commands.command(name='sharescreen', aliases=['share', 'ss', 'video'], hidden=True)
    async def video_in_VC(self, ctx, *, channel: Optional[discord.VoiceChannel] = None):
        """Enables video call in a voice channel.
        Defaults to your current voice channel or you can specify a voice channel"""
        author = ctx.message.author

        if author.voice is None and channel is None:
            return await ctx.send('Either you did not enter a valid channel or you are not in a voice channel! <:beemad:545443640323997717>')

        if channel is None:
            channel = author.voice.channel

        link = discord.utils.escape_markdown(f'https://discordapp.com/channels/{ctx.message.guild.id}/{channel.id}/')
        name = discord.utils.escape_markdown(channel.name)
        e = discord.Embed(colour=author.color,
                          description=f"[Click here to join video session for __**{name}**__]({link})\n"
                                      f"You must be in the voice channel to use this link")

        await ctx.send(embed=e)


    @commands.command(name='perms', hidden=True)
    async def get_permissions(self, ctx, *, member: CaseInsensitiveMember = None):
        """Lists permissions of a member.
        If a member is not provided, the author will be checked."""

        if not member:
            member = ctx.author
        # Check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # Embeds look nicer
        e = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        e.set_author(icon_url=member.avatar_url, name=str(member))

        e.add_field(name='\uFEFF', value=perms)  # zero-width space

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(ServerInfo(bot))
