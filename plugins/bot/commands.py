"""
VideoPlayerBot, Telegram Video Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import os
import sys
from config import Config
from logger import LOGGER
from utils import update, is_admin
from pyrogram import Client, filters
from plugins.bot.controls import is_admin
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument


HOME_TEXT = "👋🏻 **Salut\Buna [{}](tg://user?id={})**, \n\nEu sunt @OTRmoviebot ! \nPot face stream video, Radio, YouTube & la fisiere de pe Telegram audio / video direct in grup pe voice chat. Hai sa ne bucuram impreuna de acest bot pe @filme4kpetelegram 😉! \n\n**Made With ❤️ By @OTRofficial ❌ LupiiDinHaita !** 🐺"
HELP_TEXT = """
🏷️ --**Cum sa setezi BOT'ul**-- :

\u2022 Porneste un voice chat pe grup!
\u2022 Adauga @OTRmoviebot in grupul tau!
\u2022 Foloseste /play [nume video] sau foloseste /play ca raspuns la un fisier video trimis sau link de YouTube.

🏷️ --**Comenzi**-- :

\u2022 `/start` - verifica statusul bot'ului
\u2022 `/help` - arata mesajul de ajutor
\u2022 `/playlist` - arata playlistul

🏷️ --**Comenzi ADMIN ONLY**-- :

\u2022 `/skip` - da skip la video curent
\u2022 `/stream` - porneste un stream live
\u2022 `/pause` - pune pauza la video
\u2022 `/resume` - da resume la video
\u2022 `/leave` - scoate bot'ul de pe voice chat
\u2022 `/shuffle` - amesteca playlist'ul
\u2022 `/volume` - schimba volumul (0-200)
\u2022 `/replay` - da play de la inceput
\u2022 `/clrlist` - sterge tot din playlist'ul curent
\u2022 `/getlogs` - get the ffmpeg bot logs
\u2022 `/restart` - update & restart the bot

© **Powered By** : 
**@OTRofficial | @LupiiDinHaita** 🔥
"""

admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(['start', f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("CAUTA INLINE", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/OTRportal"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/OTRofficial"),
            ],
            [
                InlineKeyboardButton("H.A.I.T.A.🐺🎭😍⚔❤", url="https://t.me/LupiiDinHaita"),
                InlineKeyboardButton("Grupuri Romanesti", url="https://t.me/GrupuriRomanesti"),
            ],
            [
                InlineKeyboardButton("❔ CUM SE FOLOSESTE ❔", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)



@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/OTRportal"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/OTRofficial"),
            ],
            [
                InlineKeyboardButton("H.A.I.T.A.🐺🎭😍⚔❤", url="https://t.me/LupiiDinHaita"),
                InlineKeyboardButton("Grupuri Romanesti", url="https://t.me/GrupuriRomanesti"),
            ],
            [
                InlineKeyboardButton("INAPOI", callback_data="home"),
                InlineKeyboardButton("INCHIDE MENIU", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if Config.msg.get('help') is not None:
        await Config.msg['help'].delete()
    Config.msg['help'] = await message.reply_text(
        HELP_TEXT,
        reply_markup=reply_markup
        )

@Client.on_message(filters.command(['restart', 'update', f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter)
async def update_handler(client, message):
    k=await message.reply_text("🔄 **Ma restartez ...**")
    await update()
    try:
        await k.edit("✅ **Restart reusit! \nViziteaza @OTRofficial ❌ @LupiiDinHaita 🐺!**")
    except:
        pass

@Client.on_message(filters.command(['getlogs', f"getlogs@{Config.BOT_USERNAME}"]) & admin_filter)
async def get_logs(client, message):
    logs=[]
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("ffmpeg.txt", caption="FFMPEG Logs"))
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("botlog.txt", caption="@AsmSafone Bot Logs"))
    if logs:
        await message.reply_media_group(logs)
        logs.clear()
    else:
        await message.reply_text("❌ **Nu am gasit fisiere LOG !**")
