from discord.ext import commands
from discord_slash import SlashCommand, cog_ext
from Audio import Audio
import discord
import queue
import json
import threading
import time
import asyncio


# ctx為context的縮寫

class VoiceBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messageList = {}
        self.ctx = {}

    async def playAudio(self, channel):
        for message in self.messageList[self.ctx[channel].author.voice.channel.name]:
            print(message, 'task generating...')
            Audio(message)
            print(message, 'task start talking...')
            self.ctx[channel].voice_client.play(
                discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source='output.mp3'))

            while self.ctx[channel].voice_client.is_playing():
                await asyncio.sleep(1)

            print(message, 'task finished')

        self.messageList[self.ctx[channel].author.voice.channel.name] = []

    @cog_ext.cog_slash(name='join')
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        self.ctx[ctx.author.voice.channel.name] = ctx
        self.messageList[ctx.author.voice.channel.name] = []
        await ctx.author.voice.channel.connect()
        return await ctx.send("哈哈，4我啦。", delete_after=2.)

    @cog_ext.cog_slash(name='leave')
    async def leave(self, ctx):
        """leaves a voice channel"""

        if ctx.voice_client is None:
            return await ctx.send("蛤?", delete_after=2.)

        await ctx.send("債眷。", delete_after=2.)
        return await ctx.voice_client.disconnect()

    @cog_ext.cog_slash(name='talk')
    async def talk(self, ctx, message):
        """plays the audio from message"""

        if ctx.voice_client is None:
            return await ctx.send('沒進頻道歐', delete_after=2.)

        print(ctx.author.display_name + '說' + message, 'add to queue')

        if len(self.messageList[ctx.author.voice.channel.name]) != 0:
            self.messageList[ctx.author.voice.channel.name].append(ctx.author.display_name + '說' + message)

        else:
            self.messageList[ctx.author.voice.channel.name].append(ctx.author.display_name + '說' + message)
            asyncio.ensure_future(self.playAudio(ctx.author.voice.channel.name))

        return await ctx.send(ctx.author.display_name + '說' + message + ' 已加入列隊，你們要自立自強阿', delete_after=2.)


def main():
    try:
        bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                           description='py')
        slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

        @bot.event
        async def on_ready():
            print('Logged in as {0} ({0.id})'.format(bot.user))

        vb = VoiceBot(bot)
        bot.add_cog(vb)
        with open('config.json', 'r') as f:
            token = json.load(f)
        bot.run(token['token'])

    except RuntimeError:
        main()


if __name__ == '__main__':
    main()
