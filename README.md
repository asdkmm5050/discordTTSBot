# discordTTSBot

### Other language
- [中文](README-ZH.md)

### What is this?
- This is a Discord TTS bot, let it join a voice channel and  speak for you.

### Need
- docker

### How to use
- add a config.json file in ./
  ```
  {
  "token":"your token"
  }
  ```
- run 
  - ```docker build -t "your image name" .```
  - ```docker run "your image name"```

### Commands
- `/join`
- `/talk "message"`
- `/leave `
- `/language "lang-code"`

### Bot link
- [Bot](https://discord.com/api/oauth2/authorize?client_id=949268140267806743&permissions=2150639616&scope=bot%20applications.commands)
- **I can see all the messages sent by this bot.**
- The server is hosted on my own computer, may turn off anytime.