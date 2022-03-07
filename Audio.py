import discord
from gtts import gTTS


class Audio:
    def __init__(self, text, channel, language):
        super(Audio, self).__init__()
        self.text = text
        self.language = 'zh-TW'
        self.output = gTTS(text=self.text, lang=language, slow=False)
        self.saveAudio(channel)

    def saveAudio(self, channel):
        self.output.save(f'./audio/{channel}.mp3')
