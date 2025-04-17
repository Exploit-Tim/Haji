import asyncio
import random
from random import choice

from pyrogram.enums import MessagesFilter
from pyrogram import enums, types

from config.config import DEVS
from Haji.helpers import CMD, Emoji

__MODULES__ = "Bokep"
__HELP__ = """
<blockquote>⪼ **--Command help Bokep--**</blockquote>

<blockquote>**Cari bokep**</blockquote>
**ᐉ Keterangan: Buat nyari bokep**
ᐈ Perintah: `{0}bokep`
    
<b>   {1}</b>
"""


@CMD.UBOT("bokep")
async def _(client, message):
    rep = message.reply_to_message or message
    pros = await message.reply("🔍 Sedang mencari video...")

    try:
        await client.join_chat("https://t.me/+-mGIUzA6HvhmZGQx")
    except Exception:
        pass  # Tidak masalah jika gagal join, bisa tetap lanjut

    try:
        bokepnya = []
        async for bokep in client.search_messages(
            -1002482574579, filter=MessagesFilter.VIDEO
        ):
            bokepnya.append(bokep)

        if not bokepnya:
            return await pros.edit("⚠️ Tidak ada video ditemukan.")

        video = random.choice(bokepnya)
        await video.copy(
            message.chat.id,
            caption=f"<b>Video by <a href='tg://user?id={client.me.id}'>{client.me.first_name}</a></b>",
            reply_to_message_id=rep.id,
        )
        await pros.delete()
    except Exception as er:
        await pros.edit(f"❌ Terjadi error: `{str(er)}`")
    if client.me.id not in DEVS:
        return await client.leave_chat(-1002482574579)

