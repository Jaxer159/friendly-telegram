# Friendly Telegram Userbot Mod
Based on [FTG](https://gitlab.com/friendly-telegram)

A fast, easy to setup telegram userbot running Python 3 which uses the [Telethon](https://github.com/LonamiWebs/Telethon/) Library.

Friendly Telegram, also known as FTG, is not your average Telegram userbot: it's faster, can load modules dynamically and is very easy to use!

## Installation:
* ### Linux computer or Termux paste this command into Termux or a terminal:
 ```sh 
  (. <($(which curl>/dev/null&&echo curl -Ls||echo wget -qO-) https://raw.githubusercontent.com/Jaxer159/friendly_telegram_bot/master/install.sh))
  ```
* ### Windows (7 and higher) paste this command into Windows Powershell:
 ```sh
  iex (New-Object Net.WebClient).DownloadString("https://raw.githubusercontent.com/Jaxer159/friendly_telegram_bot/master/install.ps1")
  ```
* ### Or for Heroku on Windows:
```sh
 iex (New-Object Net.WebClient).DownloadString("https://raw.githubusercontent.com/Jaxer159/friendly_telegram_bot/master/install-heroku.ps1")
 ```
* ### Mac
```sh
$(which curl>/dev/null&&echo curl -LsO||echo wget -q) https://raw.githubusercontent.com/Jaxer159/friendly_telegram_bot/master/install.sh&&(. install.sh --no-web);rm install.sh
```
* ### Heroku
```sh
(. <($(which curl>/dev/null&&echo curl -Ls||echo wget -qO-) https://raw.githubusercontent.com/Jaxer159/friendly_telegram_bot/master/install.sh) --heroku)
```
* ### No Web
The web mode is enabled by default. To disable it, simply append --no-web to the parameters
## Documentation
We've made docs to help you to set-up the bot.
They can be found [here](https://friendly-telegram.gitlab.io).
