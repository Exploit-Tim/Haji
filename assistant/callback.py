import asyncio
import os
import sys
import traceback
from gc import get_objects
from uuid import uuid4

import requests
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.helpers import ikb
from pyrogram.types import InlineKeyboardButton as Ikb
from pyrogram.types import InlineKeyboardMarkup, InputMediaAnimation, InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo


from pyrogram.utils import unpack_inline_message_id

from config import COPY_ID, SUDO_OWNERS
from Haji import bot, haji
from Haji.database import dB, state
from Haji.helpers import (CMD, ButtonUtils, Tools, gens_font, query_fonts,
                          trigger)
from Haji.logger import logger
from plugins.pmpermit import LIMIT

from .create_users import mari_buat_userbot
from .eval import eval_tasks, update_kode
from .help import cek_plugins
from .restart import (reset_costum_text, reset_emoji, reset_prefix,
                      restart_userbot)
from .start import start_home
from .status import cek_status_akun
from .support import pengguna_nanya

MESSAGE_DICT = {}


@CMD.REGEX(trigger)
async def _(client, message):
    try:
        text = message.text
        if text in [
            "✨ Mulai Buat Userbot",
            "✨ Pembuatan Ulang Userbot",
            "✅ Lanjutkan Buat Userbot",
        ]:
            return await mari_buat_userbot(client, message)
        elif text == "❓ Status Akun":
            return await cek_status_akun(client, message)
        elif text.startswith("🔄 Reset"):
            data = text.split(" ")[2]
            if data == "Emoji":
                return await reset_emoji(client, message)
            elif data == "Prefix":
                return await reset_prefix(client, message)
            elif data == "Text":
                return await reset_costum_text(client, message)
        elif text == "🔄 Restart Userbot":
            return await restart_userbot(client, message)
        elif text == "🚀 Updates":
            return await update_kode(client, message)
        elif text == "🛠️ Cek Fitur":
            return await cek_plugins(client, message)
        elif text == "🤔 Pertanyaan":
            return await pengguna_nanya(client, message)
        elif text == "💬 Hubungi Admins":
            return await contact_admins(client, message)
        elif text == "↩️ Beranda":
            return await start_home(client, message)
    except Exception as er:
        logger.error(f"Terjadi error: {str(er)}")


@CMD.CALLBACK("^Canceleval")
async def _(_, callback_query):
    await callback_query.answer()
    reply_message_id = callback_query.message.reply_to_message_id
    if not reply_message_id:
        return

    def cancel_task(task_id) -> bool:
        task = eval_tasks.get(task_id, None)
        if task and not task.done():
            task.cancel()
            return True
        return False

    canceled = cancel_task(reply_message_id)
    if not canceled:
        return


async def contact_admins(client, message):
    new_msg = """
<b>ᴅɪʙᴀᴡᴀʜ ɪɴɪ ᴀᴅᴀʟᴀʜ ᴀᴅᴍɪɴ ꜱᴀʏᴀ. ᴋᴀᴍᴜ ᴅᴀᴘᴀᴛ ᴍᴇɴɢʜᴜʙᴜɴɢɪ ꜱᴀʟᴀʜ ꜱᴀᴛᴜ ᴅᴀʀɪ ᴍᴇʀᴇᴋᴀ.</b>"""
    tombol = []
    row = []
    for admin in SUDO_OWNERS:
        try:
            try:
                user = await client.get_users(admin)
            except Exception:
                continue
            owner_name = user.first_name
            row.append(Ikb(owner_name, user_id=f"{user.id}"))
            if len(row) == 2:
                tombol.append(row)
                row = []
        except Exception as e:
            continue
    if row:
        tombol.append(row)
    last_row = [
        Ikb(text="❌ Tutup", callback_data="closed"),
    ]
    tombol.append(last_row)

    markup = InlineKeyboardMarkup(tombol)
    return await message.reply(new_msg, reply_markup=markup)


@CMD.CALLBACK("^close")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        user = callback_query.from_user
        split = callback_query.data.split(maxsplit=1)[1]
        # logger.info(f"ini split {split}")
        data = state.get(user.id, split)
        # logger.info(f"ini data {data}")
        if not data:
            return await callback_query.answer("ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ʙᴜᴀᴛ ʟᴜ ᴛᴏᴅ!!", True)
        message = next(
            (obj for obj in get_objects() if id(obj) == int(data["idm"])), None
        )
        c = message._client
        state.clear_client(c.me.id)
        return await c.delete_messages(int(data["chat"]), int(data["_id"]))
    except Exception as er:
        logger.error(f"{str(er)}")


@CMD.CALLBACK("^cb_pm")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        data = callback_query.data.split()
        user = callback_query.from_user.id
        maling = int(data[3])
        polisi = int(data[2])
        pm_ok = await dB.get_list_from_var(polisi, "PM_OKE")
        if data[1] == "ok":
            if user != polisi:
                return await callback_query.answer(
                    "ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ʙᴜᴀᴛ ʟᴜ ᴛᴏᴅ!!", True
                )
            if maling not in pm_ok:
                await dB.add_to_var(polisi, "PM_OKE", maling)
                return await callback_query.edit_message_text(
                    "<b>ᴘᴇɴɢɢᴜɴᴀ ᴛᴇʟᴀʜ ᴅɪꜱᴇᴛᴜᴊᴜɪ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ.</b>"
                )
            else:
                return await callback_query.edit_message_text(
                    "<b>ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ ꜱᴜᴅᴀʜ ᴅɪꜱᴇᴛᴜᴊᴜɪ</b>"
                )
        elif data[1] == "no":
            if user != polisi:
                return await callback_query.answer(
                    "ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ʙᴜᴀᴛ ʟᴜ ᴛᴏᴅ!!", True
                )
            if maling in pm_ok:
                await dB.remove_from_var(polisi, "PM_OKE", maling)
                return await callback_query.edit_message_text(
                    "<b>ᴘᴇɴɢɢᴜɴᴀ ᴛᴇʟᴀʜ ᴅɪᴛᴏʟᴀᴋ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ.</b>"
                )
            else:
                return await callback_query.edit_message_text(
                    "<b>ᴘᴇɴɢɢᴜɴᴀ ɪɴɪ ꜱᴜᴅᴀʜ ᴅɪᴛᴏʟᴀᴋ</b>"
                )
        elif data[1] == "warn":
            Flood = state.get(polisi, maling)
            pm_warns = await dB.get_var(polisi, "PMLIMIT") or LIMIT
            return await callback_query.answer(
                f"⚠️ ᴋᴀᴍᴜ ᴘᴜɴʏᴀ ᴋᴇꜱᴇᴍᴘᴀᴛᴀɴ {Flood}/{pm_warns} ❗\n\nᴊɪᴋᴀ ᴋᴀᴍᴜ ᴛᴇʀᴜꜱ ᴍᴇɴᴇʀᴜꜱ ᴍᴇɴɢɪʀɪᴍ ᴘᴇꜱᴀɴ ᴋᴀᴍᴜ ᴀᴋᴀɴ ⛔ ᴋᴀᴍᴜ ᴀᴋᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ ᴛᴇʀʙʟᴏᴋɪʀ ᴅᴀɴ ꜱᴀʏᴀ ᴀᴋᴀɴ 📢 ᴍᴇʟᴀᴘᴏʀᴋᴀɴ ᴀᴋᴜɴ ᴀɴᴅᴀ ꜱᴇʙᴀɢᴀɪ ꜱᴘᴀᴍ",
                True,
            )
    except Exception as er:
        logger.error(f"ERROR: {str(er)}, line: {sys.exc_info()[-1].tb_lineno}")


@CMD.CALLBACK("^cb_gc_info")
async def _(client, callback_query):
    await callback_query.answer()
    cek = state.get(client.me.id, "gc_info")
    state.set(client.me.id, "desc_gc", cek)
    usr = cek["username"]
    if usr is None:
        keyb = ikb([[("Desc", f"cb_desc {cek['id']}", "callback_data")]])
    else:
        keyb = ikb(
            [
                [
                    ("Chat", f"https://t.me/{usr}", "url"),
                    ("Desc", f"cb_desc {cek['id']}", "callback_data"),
                ]
            ]
        )
    cdesc = cek["desc"]
    if cdesc is None:
        pass
    else:
        pass
    msg = f"""
<b>ChatInfo:</b>
   <b>name:</b> <b>{cek['name']}</b>
      <b>id:</b> <code>{cek['id']}</code>
      <b>type:</b> <b>{cek['type']}</b>
      <b>dc_id:</b> <b>{cek['dc_id']}</b>
      <b>username:</b> <b>@{cek['username']}</b>
      <b>member:</b> <b>{cek['member']}</b>
      <b>protect:</b> <b>{cek['protect']}</b>
"""
    return await callback_query.edit_message_text(msg, reply_markup=keyb)


@CMD.CALLBACK("^cb_desc")
async def _(client, callback_query):
    await callback_query.answer()
    query = callback_query.data.split(None, 1)
    id_gc = query[1]
    data = state.get(client.me.id, "gc_info")
    if int(id_gc) == int(data["id"]):
        return await callback_query.answer(f"{data['desc']}", True)
    else:
        return await callback_query.answer("Tidak ada perasaan ini", True)


@CMD.CALLBACK("^copymsg")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id = int(callback_query.data.split("_", 1)[1])
        message = [obj for obj in get_objects() if id(obj) == get_id][0]
        await message._client.unblock_user(bot.me.username)
        await callback_query.edit_message_text("<b>ᴘʀᴏꜱᴇꜱ ᴜᴘʟᴏᴀᴅ...</b>")
        copy = await message._client.send_message(
            bot.me.username, f"/kontol {message.text.split()[1]}"
        )
        msg = message.reply_to_message or message
        await asyncio.sleep(1.5)
        await copy.delete()
        async for get in message._client.search_messages(bot.me.username, limit=1):
            await message._client.copy_message(
                message.chat.id, bot.me.username, get.id, reply_to_message_id=msg.id
            )
            await message._client.delete_messages(
                message.chat.id, COPY_ID[message._client.me.id]
            )
            await get.delete()
    except Exception as error:
        await callback_query.edit_message_text(f"**ERROR:** <code>{error}</code>")


async def close_user(callback_query, user_id):
    pass


@CMD.CALLBACK("^cb")
async def _(client, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    btn_close = state.get("close_notes", "get_note")
    dia = callback_query.from_user
    type_mapping = {
        "photo": InputMediaPhoto,
        "video": InputMediaVideo,
        "animation": InputMediaAnimation,
        "audio": InputMediaAudio,
        "document": InputMediaDocument,
    }
    try:
        notetag = data[-2].replace("cb_", "")
        gw = data[-1]
        item = [x for x in haji._ubot if int(gw) == x.me.id]
        noteval = await dB.get_var(int(gw), notetag, "notes")

        if not noteval:
            await callback_query.answer("ᴄᴀᴛᴀᴛᴀɴ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.", True)
            return

        full = (
            f"<a href=tg://user?id={dia.id}>{dia.first_name} {dia.last_name or ''}</a>"
        )
        await dB.add_userdata(
            dia.id,
            dia.first_name,
            dia.last_name,
            dia.username,
            dia.mention,
            full,
            dia.id,
        )

        for me in item:
            tks = noteval["result"].get("text")
            note_type = noteval["type"]
            file_id = noteval.get("file_id")
            note, button = ButtonUtils.parse_msg_buttons(tks)
            teks = await Tools.escape_tag(bot, dia.id, note, Tools.parse_words)
            button = ButtonUtils.create_inline_keyboard(button, int(gw))
            for row in btn_close.inline_keyboard:
                button.inline_keyboard.append(row)
            try:
                if note_type == "text":
                    await callback_query.edit_message_text(
                        text=teks, reply_markup=button
                    )

                elif note_type in type_mapping and file_id:
                    InputMediaType = type_mapping[note_type]
                    media = InputMediaType(media=file_id, caption=teks)
                    await callback_query.edit_message_media(
                        media=media, reply_markup=button
                    )

                else:
                    await callback_query.edit_message_caption(
                        caption=teks, reply_markup=button
                    )

            except FloodWait as e:
                return await callback_query.answer(
                    f"FloodWait {e}, Please Waiting!!", True
                )
            except MessageNotModified:
                pass

    except Exception as e:
        print(f"Error in notes callback: {str(e)}")
        return await callback_query.answer(
            "ᴛᴇʀᴊᴀᴅɪ ᴋᴇꜱᴀʟᴀʜᴀɴ ꜱᴀᴀᴛ ᴍᴇᴍᴘʀᴏꜱᴇꜱ ᴄᴀᴛᴀᴛᴀɴ.", True
        )


@CMD.CALLBACK("^get_font")
async def _(_, callback_query):
    await callback_query.answer()
    try:
        data = int(callback_query.data.split()[1])
        new = str(callback_query.data.split()[2])
        text = state.get(data, "FONT")
        get_new_font = gens_font(new, text)
        await callback_query.answer("Wait a minute!!", True)
        return await callback_query.edit_message_text(
            f"<b>ʀᴇꜱᴜʟᴛ :\n<code>{get_new_font}</code></b>"
        )
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^prev_font")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id, current_batch = map(int, callback_query.data.split()[1:])
        prev_batch = current_batch - 1

        if prev_batch < 0:
            prev_batch = len(query_fonts) - 1

        keyboard = ButtonUtils.create_font_keyboard(
            query_fonts[prev_batch], get_id, prev_batch
        )

        buttons = InlineKeyboardMarkup(keyboard)
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^next_font")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id, current_batch = map(int, callback_query.data.split()[1:])
        next_batch = current_batch + 1

        if next_batch >= len(query_fonts):
            next_batch = 0

        keyboard = ButtonUtils.create_font_keyboard(
            query_fonts[next_batch], get_id, next_batch
        )

        buttons = InlineKeyboardMarkup(keyboard)
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^refresh_cat")
async def _(client, callback_query):

    await callback_query.answer("ᴍᴏʜᴏɴ ᴛᴜɴɢɢᴜ ꜱᴇʙᴇɴᴛᴀʀ", True)
    buttons = ikb([[("ʀᴇꜰʀᴇꜱʜ ᴄᴀᴛ", "refresh_cat")], [("ᴄʟᴏꜱᴇ", "close inline_cat")]])
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            await callback_query.edit_message_animation(
                cat_url,
                caption="<blockquote><b>ᴍᴇᴏᴡ 😽</b></blockquote>",
                reply_markup=buttons,
            )
        else:
            await callback_query.edit_message_media(
                InputMediaPhoto(
                    media=cat_url, caption="<blockquote><b>ᴍᴇᴏᴡ 😽</b></blockquote>"
                ),
                reply_markup=buttons,
            )
    else:
        await callback_query.edit_message_text("ɢᴀɢᴀʟ ᴜɴᴛᴜᴋ ʀᴇꜰʀᴇꜱʜ ᴄᴀᴛ ᴘɪᴄᴛᴜʀᴇ 🙀")


@CMD.CALLBACK("^prev_textpro")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id, current_batch = map(int, callback_query.data.split()[1:])
        prev_batch = current_batch - 1

        if prev_batch < 0:
            prev_batch = len(Tools.query_textpro) - 1

        keyboard = ButtonUtils.create_buttons_textpro(
            Tools.query_textpro[prev_batch], get_id, prev_batch
        )

        buttons = InlineKeyboardMarkup(keyboard)
        state.set(get_id, "page_textpro", prev_batch)
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^next_textpro")
async def _(client, callback_query):
    await callback_query.answer()
    try:
        get_id, current_batch = map(int, callback_query.data.split()[1:])
        next_batch = current_batch + 1

        if next_batch >= len(Tools.query_textpro):
            next_batch = 0

        keyboard = ButtonUtils.create_buttons_textpro(
            Tools.query_textpro[next_batch], get_id, next_batch
        )

        buttons = InlineKeyboardMarkup(keyboard)
        state.set(get_id, "page_textpro", next_batch)
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@CMD.CALLBACK("^genpro")
async def _(client, callback_query):
    await callback_query.answer()
    await callback_query.answer("Wait a minute!!", True)
    query = callback_query.data.split()
    userid = int(query[1])
    command = str(query[2])
    text = state.get(userid, "TEXT_PRO")
    result_image = await Tools.gen_text_pro(text, command)
    page = state.get(userid, "page_textpro")
    keyboard = ButtonUtils.create_buttons_textpro(
        Tools.query_textpro[0], userid, current_batch=int(page)
    )
    buttons = InlineKeyboardMarkup(keyboard)
    if not result_image.startswith("ERROR"):
        logger.info(f"ʀᴇꜱᴜʟᴛ ᴛᴇxᴛᴘʀᴏ : {result_image}")
        try:
            image = InputMediaPhoto(
                media=result_image,
                caption=f"<blockquote>**ᴄᴜꜱᴛᴏᴍ ᴛᴇxᴛ :**\n\n{text}</blockquote>",
            )
            await callback_query.edit_message_media(media=image, reply_markup=buttons)
        except Exception as e:

            logger.error(f"Line 656: {traceback.format_exc()}")
            await callback_query.edit_message_text(f"ɢᴀɢᴀʟ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍᴋᴀɴ ɢᴀᴍʙᴀʀ : {str(e)}")
    else:
        logger.error(f"Line 659: {traceback.format_exc()}")
        await callback_query.edit_message_text(
            f"ɢᴀɢᴀʟ ᴜɴᴛᴜᴋ ɢᴇɴᴇʀᴀᴛᴇ ᴛᴇxᴛ ᴘʀᴏ :\n{result_image}"
        )


@CMD.CALLBACK("^nxttsearch")
async def _(_, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    userid = int(data[2])
    page = int(data[1])
    uniq = str(data[3])
    videos = state.get(userid, uniq)
    if videos is None:
        await callback_query.answer("ᴛɪᴅᴀᴋ ᴀᴅᴀ ʜᴀʟᴀᴍᴀɴ ʙᴇʀɪᴋᴜᴛɴʏᴀ.", show_alert=True)
        return
    await callback_query.answer()
    buttons = []
    for video in videos[page * 5 : (page + 1) * 5]:
        title = video["title"]
        video_link = video["play"]
        caption = f"<blockquote>{title}</blockquote>"

    if page > 0:
        buttons.append(
            [
                Ikb(
                    "ᴘʀᴇᴠ ᴠɪᴅᴇᴏ", callback_data=f"nxttsearch_{page - 1}_{userid}_{uniq}"
                ),
                Ikb(
                    "ᴄʟᴏꜱᴇ", callback_data=f"nxttsearch_{page + 1}_{userid}_{uniq}"
                ),
            ]
        )
        buttons.append([Ikb("ᴄʟᴏꜱᴇ", callback_data=f"close inline_ttsearch {uniq}")])
    else:
        buttons.append(
            [
                Ikb(
                    "ɴᴇxᴛ ᴠɪᴅᴇᴏ", callback_data=f"nxttsearch_{page + 1}_{userid}_{uniq}"
                ),
            ]
        )
        buttons.append([Ikb("ᴄʟᴏꜱᴇ", callback_data=f"close inline_ttsearch {uniq}")])
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_media(
        media=InputMediaVideo(
            media=video_link,
            caption=caption,
        ),
        reply_markup=reply_markup,
    )


@CMD.CALLBACK("^cqtiktok")
async def _(client, callback_query):
    await callback_query.answer()

    try:
        data = callback_query.data.split("_")
        userid = int(data[2])
        query = str(data[1])
        results = state.get(userid, "result_ttdownload")
        get_id = state.get(userid, "idm_ttdownload")
        message = [obj for obj in get_objects() if id(obj) == get_id][0]
        name = f"{str(uuid4())}"
        if query == "videodl":
            video_link = results["video"][0]
            caption = results["title"]
            logger.info(f"Video tiktok link: {video_link}")
            await callback_query.edit_message_text(
                "**ᴍᴏʜᴏɴ ᴛᴜɴɢɢᴜ, ᴍᴇɴᴄᴏʙᴀ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴠɪᴅᴇᴏ...**"
            )
            video = f"downloads/{name.split('-')[1]}.mp4"
            await Tools.bash(f"curl -L {video_link} -o {video}")
            await message.reply_video(video, caption=caption)
            if os.path.exists(video):
                os.remove(video)
            await asyncio.sleep(2)
            ids = (unpack_inline_message_id(callback_query.inline_message_id)).id
            return await message._client.delete_messages(message.chat.id, ids)
        elif query == "audiodl":
            audio_link = results["audio"][0]
            caption = results["title"]
            logger.info(f"Audio tiktok link: {audio_link}")
            await callback_query.edit_message_text(
                "**ᴍᴏʜᴏɴ ᴛᴜɴɢɢᴜ, ᴍᴇɴᴄᴏʙᴀ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴀᴜᴅɪᴏ...**"
            )
            audio = f"downloads/{name.split('-')[1]}.mp3"
            await Tools.bash(f"curl -L {audio_link} -o {audio}")
            await message.reply_audio(audio, caption=caption)
            await asyncio.sleep(2)
            if os.path.exists(audio):
                os.remove(audio)
            ids = (unpack_inline_message_id(callback_query.inline_message_id)).id
            return await message._client.delete_messages(message.chat.id, ids)
    except Exception as er:
        logger.error(f"Cq tiktok dl: {traceback.format_exc()}")
        return await callback_query.edit_message_text(f"**An errror:** {str(er)}")


@CMD.CALLBACK("^nxtspotify")
async def _(_, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    userid = int(data[2])
    page = int(data[1])
    uniq = str(data[3])
    audios = state.get(userid, uniq)
    if audios is None:
        await callback_query.answer("ᴛɪᴅᴀᴋ ᴀᴅᴀ ʜᴀʟᴀᴍᴀɴ ʙᴇʀɪᴋᴜᴛɴʏᴀ.", show_alert=True)
        return
    await callback_query.answer()
    buttons = []
    for audio in audios[page * 5 : (page + 1) * 5]:
        caption = f"""<blockquote>
🎶 **ᴊᴜᴅᴜʟ :** {audio['title']}
👥 **ᴘᴏᴘᴜʟᴀʀɪᴛᴀꜱ :** {audio['popularity']}
⏳ **ᴅᴜʀᴀꜱɪ :** {audio['duration']}
🖇️ **ꜱᴘᴏᴛɪꜰʏ ᴜʀʟ :** <a href='{audio['url']}'>here</a></blockquote>"""
        state.set(userid, "fordlspotify", audio["url"])
        logger.info(f"Url line 796: {audio['url']}")
    buttons.append([Ikb("ᴅᴏᴡɴʟᴏᴀᴅ ᴀᴜᴅɪᴏ", callback_data=f"dlspot_{userid}_{uniq}")])
    if page > 0:
        buttons.append(
            [
                Ikb(
                    "ᴘʀᴇᴠ ᴀᴜᴅɪᴏ", callback_data=f"nxtspotify_{page - 1}_{userid}_{uniq}"
                ),
                Ikb(
                    "ɴᴇxᴛ ᴀᴜᴅɪᴏ", callback_data=f"nxtspotify_{page + 1}_{userid}_{uniq}"
                ),
            ]
        )
        buttons.append([Ikb("ᴄʟᴏꜱᴇ", callback_data=f"close inline_spotify {uniq}")])
    else:
        buttons.append(
            [
                Ikb(
                    "ɴᴇxᴛ ᴀᴜᴅɪᴏ", callback_data=f"nxtspotify_{page + 1}_{userid}_{uniq}"
                ),
            ]
        )
        buttons.append([Ikb("ᴄʟᴏꜱᴇ", callback_data=f"close inline_spotify {uniq}")])
    # state.set(userid, "fordlspotify", audio["url"])
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_text(
        caption, reply_markup=reply_markup, disable_web_page_preview=True
    )


@CMD.CALLBACK("^dlspot")
async def _(_, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    userid = int(data[1])
    uniq = str(data[2])
    data = state.get(userid, uniq)
    get_id = state.get(userid, "idm_spotdl")
    message = [obj for obj in get_objects() if id(obj) == get_id][0]
    link = data[0]["url"]
    audio, caption = await Tools.download_spotify(link)
    await callback_query.edit_message_text(
        "**ᴍᴏʜᴏɴ ᴛᴜɴɢɢᴜ, ᴍᴇɴᴄᴏʙᴀ ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴀᴜᴅɪᴏ...**"
    )
    await message.reply_audio(audio, caption=caption)
    await asyncio.sleep(2)
    ids = (unpack_inline_message_id(callback_query.inline_message_id)).id
    if os.path.exists(audio):
        os.remove(audio)
    try:
        return await message._client.delete_messages(
            message.chat.id,
            ids,
        )
    except Exception:
        logger.error(f"Cant delete inline_message_id: {traceback.format_exc()}")


@CMD.CALLBACK("^nxpinsearch")
async def _(_, callback_query):
    await callback_query.answer()
    data = callback_query.data.split("_")
    page = int(data[1])
    uniq = str(data[2])
    photos = state.get(uniq, uniq)

    if not photos:
        await callback_query.answer(
            "ᴛɪᴅᴀᴋ ᴀᴅᴀ ꜰᴏᴛᴏ ᴜɴᴛᴜᴋ ᴅɪᴛᴀᴍᴘɪʟᴋᴀɴ.", show_alert=True
        )
        return

    total_photos = len(photos)

    if page < 0 or page >= total_photos:
        await callback_query.answer("ʜᴀʟᴀᴍᴀɴ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.", show_alert=True)
        return

    buttons = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            Ikb("⬅️ ᴘʀᴇᴠ", callback_data=f"nxpinsearch_{page - 1}_{uniq}")
        )
    if page < total_photos - 1:
        nav_buttons.append(
            Ikb("➡️ ɴᴇxᴛ", callback_data=f"nxpinsearch_{page + 1}_{uniq}")
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([Ikb("❌ ᴄʟᴏꜱᴇ", callback_data=f"close inline_pinsearch {uniq}")])

    reply_markup = InlineKeyboardMarkup(buttons)

    await callback_query.edit_message_media(
        media=InputMediaPhoto(media=photos[page]), reply_markup=reply_markup
    )


@CMD.CALLBACK("^bola_date")
async def _(client, callback_query):
    await callback_query.answer()
    split = callback_query.data.split()
    if len(split) > 1:
        state_key = split[1]
        stored_data = state.get(state_key, state_key)

        buttons = []
        temp_row = []
        for liga_date in stored_data:
            button = Ikb(
                text=liga_date["LigaDate"],
                callback_data=f"bola_matches {state_key} {liga_date['LigaDate']}",
            )
            temp_row.append(button)

            if len(temp_row) == 3:
                buttons.append(temp_row)
                temp_row = []

        if temp_row:
            buttons.append(temp_row)

        buttons.append([Ikb(text="ᴄʟᴏꜱᴇ", callback_data="close inline_bola")])
        keyboard = InlineKeyboardMarkup(buttons)

        return await callback_query.edit_message_text(
            text="<b>ᴘɪʟɪʜ ᴛᴀɴɢɢᴀʟ ᴜɴᴛᴜᴋ ᴍᴇɴᴏɴᴛᴏɴ ᴘᴇʀᴛᴀɴᴅɪɴɢᴀɴ ꜱᴇᴘᴀᴋ ʙᴏʟᴀ :</b>",
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
    else:
        return await callback_query.edit_message_text("ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀᴛᴀ ʏᴀɴɢ ᴅɪᴛᴇᴍᴜᴋᴀɴ.")


@CMD.CALLBACK("^bola_matches")
async def _(client, callback_query):
    await callback_query.answer()
    split = callback_query.data.split()
    if len(split) > 2:
        state_key = split[1]
        selected_date = split[2]
        stored_data = state.get(state_key, state_key)

        date_matches = next(
            (
                date
                for date in stored_data
                if date["LigaDate"].split()[0] == selected_date.split()[0]
            ),
            None,
        )

        if date_matches:
            text = f"ᴘᴇʀᴛᴀɴᴅɪɴɢᴀɴ ꜱᴇᴘᴀᴋ ʙᴏʟᴀ ᴅɪ {selected_date}\n\n"
            for league in date_matches["LigaItem"]:
                text += f"🏆 {league['NameLiga']}\n"
                for match in league["Match"]:
                    text += f"⚽ {match['team']} at {match['time']}\n"

            buttons = [
                [Ikb(text="« ᴋᴇᴍʙᴀʟɪ", callback_data=f"bola_date {state_key}")],
                [Ikb(text="ᴄʟᴏꜱᴇ", callback_data="close inline_bola")],
            ]
            keyboard = InlineKeyboardMarkup(buttons)

            return await callback_query.edit_message_text(
                text=f"<blockquote><b>{text}</b></blockquote>",
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
        else:
            return await callback_query.answer("ꜱɪʟᴀʜᴋᴀɴ ᴜʟᴀɴɢɪ ꜰɪᴛᴜʀ ʙᴏʟᴀ!!", True)


@CMD.CALLBACK("^news_")
async def _(client, callback_query):
    data = callback_query.data.split("_")
    page = int(data[1])
    uniq = str(data[2])
    berita = state.get(uniq, uniq)

    if not berita:
        await callback_query.answer(
            "ᴛɪᴅᴀᴋ ᴀᴅᴀ ʙᴇʀɪᴛᴀ ᴜɴᴛᴜᴋ ᴅɪᴛᴀᴍᴘɪʟᴋᴀɴ.", show_alert=True
        )
        return

    total_photos = len(berita)

    if page < 0 or page >= total_photos:
        await callback_query.answer("ʜᴀʟᴀᴍᴀɴ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ.", show_alert=True)
        return

    buttons = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(Ikb("⬅️ ᴘʀᴇᴠ", callback_data=f"news_{page - 1}_{uniq}"))
    if page < total_photos - 1:
        nav_buttons.append(Ikb("➡️ ɴᴇxᴛ", callback_data=f"news_{page + 1}_{uniq}"))

    if nav_buttons:
        buttons.append(nav_buttons)

    buttons.append([Ikb("❌ ᴄʟᴏꜱᴇ", callback_data=f"close inline_news {uniq}")])
    date = berita[page].get("berita_diupload", "-")
    caption = f"**ᴊᴜᴅᴜʟ :** {berita[page]['berita']}\n**ʟɪɴᴋ :** {berita[page]['berita_url']}\n**ᴅɪᴜᴘʟᴏᴀᴅ :** {date}"

    photo = berita[page]["berita_thumb"]
    reply_markup = InlineKeyboardMarkup(buttons)
    return await callback_query.edit_message_media(
        media=InputMediaPhoto(media=photo, caption=caption),
        reply_markup=reply_markup,
    )
