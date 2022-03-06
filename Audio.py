import discord
from gtts import gTTS


class Audio:
    def __init__(self, text, channel):
        super(Audio, self).__init__()
        self.text = text
        self.language = 'zh-TW'
        self.output = gTTS(text=self.text, lang='zh', slow=False)
        self.saveAudio(channel)

    def saveAudio(self, channel):
        self.output.save(f'{channel}.mp3')
