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

from asyncio import sleep
from config import Config
from logger import LOGGER
from pyrogram import Client
from pyrogram.errors import MessageNotModified
from plugins.bot.commands import HOME_TEXT, HELP_TEXT
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils import get_admins, get_buttons, get_playlist_str, pause, restart_playout, resume, shuffle_playlist, skip

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    admins = await get_admins(Config.CHAT_ID)
    if query.from_user.id not in admins and query.data != "help":
        await query.answer(
            "Nu ai acces! 🤣",
            show_alert=True
            )
        return
    if query.data == "shuffle":
        if not Config.playlist:
            await query.answer("🚫 Empty Playlist !", show_alert=True)
            return
        await shuffle_playlist()
        await sleep(1)
        await query.answer("🔁 Shuffling !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(
                    f"{pl}",
                    parse_mode="Markdown",
                    reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "pause":
        if Config.PAUSE:
            await query.answer("⏸ Am pus deja pauza !", show_alert=True)
        else:
            await pause()
            await sleep(1)
            await query.answer("⏸ Pauza !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass
    
    elif query.data.lower() == "resume":   
        if not Config.PAUSE:
            await query.answer("▶️ Am dat deja resume !", show_alert=True)
        else:
            await resume()
            await sleep(1)
            await query.answer("▶️ Redau din nou !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data=="skip":   
        if not Config.playlist:
            await query.answer("🚫 Empty Playlist !", show_alert=True)
        else:
            await skip()
            await sleep(1)
            await query.answer("⏭ Am dat skip !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data=="replay":
        if not Config.playlist:
            await query.answer("🚫 Empty Playlist !", show_alert=True)
        else:
            await restart_playout()
            await sleep(1)
            await query.answer("🔂 Replay !", show_alert=True)
        pl=await get_playlist_str()
        try:
            await query.message.edit(f"{pl}",
                disable_web_page_preview=True,
                reply_markup=await get_buttons()
            )
        except MessageNotModified:
            pass

    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("CHANNEL", url="https://t.me/AsmSafone"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/SafoTheBot"),
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

        try:
            await query.message.edit(
                HELP_TEXT,
                reply_markup=reply_markup

            )
        except MessageNotModified:
            pass

    elif query.data=="home":
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
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass
    await query.answer()

