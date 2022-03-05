import threading
import time

from discord.ext import commands
from discord_slash import SlashCommand, cog_ext

from Audio import Audio
import discord
import queue


# ctx為context的縮寫

class VoiceBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.q = queue.Queue()
        self.ctx = None
        self.threadTalking = threading.Thread(target=self.worker)

    def worker(self):
        while True:
            if self.ctx is not None:
                if not self.ctx.voice_client.is_playing():
                    task = self.q.get()
                    Audio(task)
                    self.ctx.voice_client.play(
                        discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='output.mp3'))
                    while self.ctx.voice_client.is_playing():
                        time.sleep(1)
                    self.q.task_done()

    @cog_ext.cog_slash(name='join')
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        await ctx.author.voice.channel.connect()
        self.ctx = ctx
        self.threadTalking.start()
        return await ctx.send("哈哈，4我啦。", delete_after=2.)

    @cog_ext.cog_slash(name='leave')
    async def leave(self, ctx):
        """leaves a voice channel"""
        await ctx.send("債眷。", delete_after=2.)

        return await ctx.voice_client.disconnect()

    @cog_ext.cog_slash(name='talk')
    async def talk(self, ctx, message):
        """plays the audio from message"""

        if ctx.voice_client is None:
            return await ctx.send('沒進頻道歐', delete_after=2.)

        self.q.put(ctx.author.display_name + '說' + message)
        return await ctx.send('已加入列隊，你們要自立自強阿', delete_after=2.)


def main():
    try:
        bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                           description='py')
        slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

        @bot.event
        async def on_ready():
            print('Logged in as {0} ({0.id})'.format(bot.user))
            print('------')

        vb = VoiceBot(bot)
        bot.add_cog(vb)
        bot.run('OTQ5MjY4MTQwMjY3ODA2NzQz.YiH42Q.6bRQssOqSZ5ilANPxGQLFBAZDew')

    except RuntimeError:
        main()


if __name__ == '__main__':
    main()
