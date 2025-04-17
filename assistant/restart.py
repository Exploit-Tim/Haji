import asyncio
import importlib

from pyrogram.helpers import kb

from config import BOT_NAME
from Haji import UserBot, bot, haji
from Haji.database import dB
from Haji.helpers import CMD, Emoji
from plugins import PLUGINS

keyboard = kb([["↩️ Beranda"]], resize_keyboard=True, one_time_keyboard=True)


async def reset_costum_text(client, message):
    user_id = message.from_user.id
    proses = await message.reply("<b>ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    if user_id not in haji._get_my_id:
        return await proses.edit(
            f"<b>ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ @{bot.me.username}!!</b>", reply_markup=keyboard
        )
    try:
        await dB.set_var(user_id, "text_ping", "ᴘɪɴɢ")
        await dB.set_var(user_id, "text_uptime", "ᴜᴘᴛɪᴍᴇ")
        owner_name = f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
        await dB.set_var(user_id, "text_owner", f"ᴏᴡɴᴇʀ: {owner_name}")
        await dB.set_var(user_id, "text_ubot", f"{BOT_NAME}")
        await dB.set_var(user_id, "text_gcast", "ᴍᴇᴍᴘʀᴏsᴇs")
        await dB.set_var(user_id, "text_sukses", "ɢᴄᴀsᴛ sᴜᴋsᴇs ᴘᴀᴋ")
        await asyncio.sleep(1)
        return await proses.edit(
            "<b>ᴛᴇᴋꜱ ᴋᴜꜱᴛᴏᴍ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴅɪᴀᴛᴜʀ ᴜʟᴀɴɢ</b>", reply_markup=keyboard
        )
    except Exception as er:
        return await proses.edit(f"<b>ERROR: `{str(er)}`</b>", reply_markup=keyboard)


async def reset_emoji(client, message):
    user_id = message.from_user.id
    proses = await message.reply("<b>ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    if user_id not in haji._get_my_id:
        return await proses.edit(
            f"<b>ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ @{bot.me.username}!!</b>", reply_markup=keyboard
        )
    for User in haji._ubot:
        if user_id == User.me.id:
            try:
                em = Emoji(User)
                await em.reset_emoji()
                await asyncio.sleep(1)
                return await proses.edit(
                    "<b>ᴇᴍᴏᴊɪ ᴋᴜꜱᴛᴏᴍ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴅɪᴀᴛᴜʀ ᴜʟᴀɴɢ.!!</b>", reply_markup=keyboard
                )
            except Exception as er:
                return await proses.edit(
                    f"<b>ERROR: `{str(er)}`</b>", reply_markup=keyboard
                )


async def reset_prefix(client, message):
    mepref = [".", ",", "?", "+", "!"]
    proses = await message.reply("<b>ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = message.from_user.id
    if user_id not in haji._get_my_id:
        return await proses.edit(
            f"<b>ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ @{bot.me.username}!!</b>", reply_markup=keyboard
        )
    for x in haji._ubot:
        if x.me.id == user_id:
            x.set_prefix(x.me.id, mepref)
            await dB.set_pref(x.me.id, mepref)
            return await proses.edit(
                f"<b>ᴘʀᴇꜰɪx ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴅɪᴀᴛᴜʀ ᴜʟᴀɴɢ ᴋᴇ : `{' '.join(mepref)}` .</b>",
                reply_markup=keyboard,
            )


async def restart_userbot(client, message):
    proses = await message.reply("<b>ᴍᴇᴍᴘʀᴏsᴇs...</b>")
    user_id = message.from_user.id
    if user_id not in haji._get_my_id:
        return await proses.edit(
            f"<b>ᴀɴᴅᴀ ʙᴜᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ @{bot.me.username}!!</b>", reply_markup=keyboard
        )
    for X in await dB.get_userbots():
        if user_id == int(X["name"]):
            try:
                ubot = UserBot(**X)
                await ubot.start()
                for modul in PLUGINS:
                    importlib.reload(importlib.import_module(f"plugins.{modul}"))
                return await proses.edit(
                    f"<b>✅ ᴜꜱᴇʀʙᴏᴛ ᴛᴇʟᴀʜ ᴅɪ ʀᴇꜱᴛᴀʀᴛ {ubot.me.first_name} {ubot.me.last_name or ''} | {ubot.me.id}.</b>",
                    reply_markup=keyboard,
                )
            except Exception as error:
                return await proses.edit(f"<b>{error}</b>", reply_markup=keyboard)


@CMD.BOT("restart")
async def _(client, message):
    return await restart_userbot(client, message)
