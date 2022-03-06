from discord.ext import commands
from discord_slash import SlashCommand, cog_ext
from audio import Audio
import discord
import json
import asyncio


# ctx為context的縮寫

class VoiceBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messageList = {}
        self.ctx = {}

    async def playAudio(self, channel):
        for message in self.messageList[channel]:
            print(message, 'task generating...')
            Audio(message, channel)
            print(message, 'task start talking...')
            self.ctx[channel].voice_client.play(
                discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=f'./audio/{channel}.mp3'))

            while self.ctx[channel].voice_client.is_playing():
                await asyncio.sleep(1)

            print(message, 'task finished')

        self.messageList[channel] = []

    @cog_ext.cog_slash(name='join')
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        channel = str(ctx.author.voice.channel.id)
        self.ctx[channel] = ctx
        self.messageList[channel] = []
        print('connected to:', channel)
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
        channel = str(ctx.author.voice.channel.id)

        if len(self.messageList[channel]) != 0:
            self.messageList[channel].append(ctx.author.display_name + '說' + message)
            print(1)

        else:
            self.messageList[channel].append(ctx.author.display_name + '說' + message)
            asyncio.ensure_future(self.playAudio(channel))
            print(2)

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
