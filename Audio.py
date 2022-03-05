import discord
from gtts import gTTS


class Audio:
    def __init__(self, text):
        super(Audio, self).__init__()
        self.text = text
        self.language = 'zh-TW'
        self.output = gTTS(text=self.text, lang='zh', slow=False)
        self.saveAudio()

    def saveAudio(self):
        self.output.save('output.mp3')
