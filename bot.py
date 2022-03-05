from discord.ext import commands
from tqdm import asyncio
from Audio import Audio
import discord


# ctx為context的縮寫

class VoiceBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        """leaves a voice channel"""

        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, arg):
        """plays the audio from ctx"""

        if ctx.voice_client is None:
            return await ctx.send("沒進頻道歐")
        if arg is None:
            return await ctx.send("我只會讀稿不會讀心歐")
        if ctx.voice_client.is_playing():
            return await ctx.send("我只有一張嘴吧，你們要自立自強阿")
        Audio(arg)
        ctx.voice_client.play(discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='output.mp3'))


def main():
    bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                       description='Relatively simple music bot example')

    @bot.event
    async def on_ready():
        print('Logged in as {0} ({0.id})'.format(bot.user))
        print('------')

    bot.add_cog(VoiceBot(bot))
    bot.run('your token')


if __name__ == '__main__':
    main()
