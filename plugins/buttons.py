import asyncio

from config import DICT_BUTTON
from Haji import bot
from Haji.database import state
from Haji.helpers import CMD, ButtonUtils, Emoji

__MODULES__ = "Button"
__HELP__ = """
<blockquote>⪼ **--Command help Button--**</blockquote>

<blockquote>**Membuat button dari**</blockquote>
**ᐉ Keterangan: Anda bisa membuat button dari teks, harap baca format markdown terlebih dahulu**
ᐈ Perintah: `{0}button` (reply text)
 
<b>   {1}</b>
"""


@CMD.UBOT("buttonch")
async def _(client, message):
    proses = await message.reply_text("Memproses...")
    rep = message.reply_to_message
    if not rep and len(message.command) < 2:
        return await proses.edit("Reply ke pesan!!")
    state.set(client.me.id, "edit_reply_markup", rep.text)
    link = message.text.split(None, 1)[1]
    await client.send_message(bot.me.username, f"/button {link}")
    return await proses.edit("Done")


@CMD.UBOT("button")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    reply = message.reply_to_message
    if not reply:
        return await message.reply(
            f"{em.gagal}<b>Harap membalas pesan dengan format button!</b>"
        )
    teks = client.get_text(message)
    DICT_BUTTON[client.me.id] = client.get_arg(message)
    chat_id = message.chat.id if len(message.command) < 2 else message.text.split()[1]
    if reply.media:
        copy = await reply.copy(bot.me.username)
        sent = await client.send_message(
            bot.me.username, "/id button_media", reply_to_message_id=copy.id
        )
        await asyncio.sleep(1)
        await sent.delete()
        await copy.delete()
        state.set(client.me.id, "button", DICT_BUTTON[client.me.id])
    else:
        state.set(client.me.id, "button", DICT_BUTTON[client.me.id])
    text, keyboard = ButtonUtils.parse_msg_buttons(teks)
    try:
        if keyboard:
            try:
                inline = await ButtonUtils.send_inline_bot_result(
                    message, chat_id, bot.me.username, f"make_button {client.me.id}"
                )
                if inline:
                    return await message.delete()
            except Exception as er:
                return await message.reply(f"{em.gagal}<b>ERROR: {str(er)}</b>")
        else:
            return await message.reply(
                f"{em.gagal}<b>Harap membalas pesan dengan format button!</b>"
            )
    except IndexError:
        return await message.reply(
            f"{em.gagal}<b>Harap membalas pesan dengan format button!</b>"
        )
