from discord.ext import commands
from discord_slash import SlashCommand, cog_ext

from Audio import Audio
import discord


# ctx為context的縮寫

class VoiceBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name='join')
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        await ctx.author.voice.channel.connect()
        return await ctx.send("哈哈，4我啦。", delete_after=1.)

    @cog_ext.cog_slash(name='leave')
    async def leave(self, ctx):
        """leaves a voice channel"""

        await ctx.voice_client.disconnect()
        return await ctx.send("債眷。", delete_after=1.)

    @cog_ext.cog_slash(name='talk')
    async def talk(self, ctx, arg):
        """plays the audio from ctx"""

        if ctx.voice_client is None:
            return await ctx.send('沒進頻道歐')
        if arg is None:
            return await ctx.send('我只會讀稿不會讀心歐')
        if ctx.voice_client.is_playing():
            return await ctx.send('我只有一張嘴吧，你們要自立自強阿')
        Audio(arg)
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='output.mp3'))
        return await ctx.send('已送出', delete_after=1.)


def main():
    bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                       description='py')
    slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

    @bot.event
    async def on_ready():
        print('Logged in as {0} ({0.id})'.format(bot.user))
        print('------')

    bot.add_cog(VoiceBot(bot))
    bot.run('your token')


if __name__ == '__main__':
    main()
