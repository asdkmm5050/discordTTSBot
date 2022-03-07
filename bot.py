from discord.ext import commands
from discord_slash import SlashCommand, cog_ext
from audio import Audio
import discord
import json
import asyncio
import re


# ctx為context的縮寫


def makeNicknameSorter(nickname):
    """
    make nickname shorter.
    RULE:Chinese characters > English characters > numbers > others
    remove useless char in nickname with RULE
    """
    if re.compile(u'[\u4E00-\u9FFF]+', re.I).findall(nickname):
        newNickName = re.compile(u'[\u4E00-\u9FFF]+', re.I).findall(nickname)
        print(newNickName)
        print(nickname + ' short to ' + newNickName[-1])
        return newNickName[-1][-3:]

    if re.compile(r'[a-z]|[A-Z]+', re.I).findall(nickname):
        newNickName = re.compile(r'[a-z]|[A-Z]+', re.I).findall(nickname)
        print(nickname + ' short to ' + ''.join(newNickName))
        print(newNickName)
        return ''.join(newNickName)

    if re.compile(r'[0-9]+', re.I).findall(nickname):
        newNickName = re.compile(r'[0-9]+', re.I).findall(nickname)
        print(nickname + ' short to ' + ''.join(newNickName))
        print(newNickName)
        return ''.join(newNickName)[0:3]

    if re.compile(r'[^a-zA-Z0-9]+', re.I).findall(nickname):
        newNickName = re.compile(r'[^a-zA-Z0-9]+', re.I).findall(nickname)
        print(nickname + ' short to ' + ''.join(newNickName))
        print(newNickName)
        return ''.join(newNickName)[0:2]

    return nickname


class VoiceBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messageList = {}
        self.ctx = {}
        self.languageList = {}

    async def playAudio(self, channel):
        for message in self.messageList[channel]:
            print(message, 'task generating...')
            Audio(message, channel, self.languageList[channel])
            print(message, 'task start talking...')
            self.ctx[channel].voice_client.play(
                discord.FFmpegPCMAudio(executable='C:/ffmpeg/bin/ffmpeg.exe', source=f'./audio/{channel}.mp3'))

            while self.ctx[channel].voice_client.is_playing():
                await asyncio.sleep(0.1)
            await asyncio.sleep(0.5)

            print(message, 'task finished')

        self.messageList[channel] = []

    @cog_ext.cog_slash(name='join')
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.author.voice is None:
            return await ctx.send("你不在頻道裡歐", delete_after=2.)

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        channel = str(ctx.author.voice.channel.id)
        self.ctx[channel] = ctx
        self.messageList[channel] = []
        self.languageList[channel] = 'zh'
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

        fullMessage = message + ', from ' + makeNicknameSorter(ctx.author.display_name)
        print(fullMessage, 'add to queue')

        channel = str(ctx.author.voice.channel.id)

        if len(self.messageList[channel]) != 0:
            self.messageList[channel].append(fullMessage)

        else:
            self.messageList[channel].append(fullMessage)
            asyncio.ensure_future(self.playAudio(channel))

        return await ctx.send(fullMessage + ' - 已加入列隊', delete_after=2.)

    @cog_ext.cog_slash(name='language')
    async def changeLanguage(self, ctx, language):
        """
        Support language : en (English), fr (French), zh (Mandarin), pt (Portuguese), es (Spanish)
        """

        channel = str(ctx.author.voice.channel.id)
        self.languageList[channel] = language
        try:
            Audio('test', channel, self.languageList[channel])
            return await ctx.send('Change language: ' + language, delete_after=2.)
        except ValueError:
            self.languageList[channel] = 'zh'
            return await ctx.send('Language not supported: ' + language, delete_after=2.)


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
