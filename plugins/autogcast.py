import asyncio
import random

from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait

from config import BLACKLIST_GCAST
from Haji.database import dB
from Haji.helpers import CMD, Emoji

from .spambot import spam_bot

__MODULES__ = "Autobc"
__HELP__ = """
<blockquote>⪼ **--Command help AutoBc--**</blockquote>

<blockquote>**Tambahkan teks autobc**</blockquote>
**ᐉ Keterangan: Tambahkan teks untuk autogcast**
`{0}autogcast add` (balas teks)

<blockquote>**On off autobc**</blockquote>
**ᐉ Keterangan: Set auto gcast on atau off, sebelum Anda set ini harap tambahkan teks terlebih dahulu**
ᐈ Perintah: `{0}autogcast` (on/off)

<blockquote>**Menghapus teks autobc**</blockquote>
**ᐉ Keterangan: Menghapus teks dari list auto gcast**
ᐈ Perintah: `{0}autogcast del` (nomor)

<blockquote>**Autobc cek limit**</blockquote>
**ᐉ Keterangan: Anda bisa set on untuk mendapatkan notifikasi limit dari @spambot**
ᐈ Perintah: `{0}autogcast limit` (on/off)

<blockquote>**Set delay autobc**</blockquote>
**ᐉ Keterangan: Anda bisa mengatur delay untuk auto gcast**
ᐈ Perintah: `{0}autogcast delay` (nomor)

<blockquote>**Melihat teks autobc**</blockquote>
**ᐉ Keterangan: Anda bisa memeriksa semua pesan auto gcast**
ᐈ Perintah: `{0}autogcast get`
 
<blockquote>**Note**: Jika kamu ingin mengaktifkan autobc, mohon tambahkan teks terlebih dahulu.</blockquote>

<b>   {1}</b>
"""

AG = []
LT = []


def extract_type_and_text(message):
    args = message.text.split(None, 2)
    if len(args) < 2:
        return None, None

    type = args[1]
    msg = (
        message.reply_to_message.text
        if message.reply_to_message
        else args[2] if len(args) > 2 else None
    )
    return type, msg


async def text_autogcast(client):
    auto_text_vars = await dB.get_var(client.me.id, "AUTO_GCAST")
    list_ids = []
    list_text = []
    for data in auto_text_vars:
        list_ids.append(int(data["message_id"]))
    for ids in list_ids:
        msg = await client.get_messages("me", ids)
        list_text.append(msg.text)
    return list_text


@CMD.UBOT("autogcast")
async def _(client, message):
    em = Emoji(client)
    await em.get()

    proses_ = await em.get_costum_text()
    msg = await message.reply(f"{em.proses}**{proses_[4]}**")
    type, value = extract_type_and_text(message)
    reply = message.reply_to_message
    logs = "me"
    auto_text_vars = await dB.get_var(client.me.id, "AUTO_GCAST")
    send_msg = []
    if type == "on":
        if not auto_text_vars:
            return await msg.edit(
                f"{em.gagal}**Mohon tambahkan pesan sebelum anda mengaturnya menjadi on!!**"
            )
        if client.me.id not in AG:
            await msg.edit(
                f"{em.sukses}<b>Autogcast berjalan! Ketik `{message.text.split()[0]} off` untuk stop autogcast.</b>"
            )
            AG.append(client.me.id)
            done = 0
            while client.me.id in AG:
                delay = await dB.get_var(client.me.id, "DELAY_GCAST") or 1
                blacklist = await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST")
                for ax in auto_text_vars:
                    send_msg.append(int(ax["message_id"]))
                txt = random.choice(send_msg)
                msg_id = await client.get_messages(logs, txt)

                group = 0
                async for dialog in client.get_dialogs():
                    if (
                        dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)
                        and dialog.chat.id not in blacklist
                        and dialog.chat.id not in BLACKLIST_GCAST
                    ):
                        try:
                            await asyncio.sleep(1)
                            await msg_id.copy(dialog.chat.id)
                            group += 1
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            await msg_id.copy(dialog.chat.id)
                            group += 1
                        except Exception:
                            pass

                if client.me.id not in AG:
                    return

                done += 1
                await msg.reply(
                    f"{em.sukses}<b>Autogcast sukses : `{done}`, ke grup : `{group}`. menunggu untuk : `{delay}`</b>"
                )
                await asyncio.sleep(int(60 * int(delay)))
        else:
            return await msg.delete()

    elif type == "off":
        if client.me.id in AG:
            AG.remove(client.me.id)
            return await msg.edit(f"{em.gagal}<b>Autogcast telah dihentikan.</b>")
        else:
            return await msg.delete()

    elif type == "add":
        if not reply:
            return await msg.edit(
                f"{em.gagal}<b>Setidaknya balas teksnya, idiot, untuk membuat pesannya.</b>"
            )
        await add_auto_text(message)
        return await msg.edit(
            f"{em.sukses}<b>Disimpan untuk pesan Auto Gcast.</b>",
        )

    elif type == "delay":
        await dB.set_var(client.me.id, "DELAY_GCAST", value)
        return await msg.edit(
            f"{em.sukses}<b>Auto Gcast delay di atur ke: <code>{value}</code></b>"
        )

    elif type == "del":
        if not value:
            return await msg.edit(
                f"{em.gagal}<b>Setidaknya berikan satu nomor atau semua, idiot, teks mana yang akan dihapus.</b>"
            )
        if value == "all":
            await dB.set_var(client.me.id, "AUTO_GCAST", [])
            return await msg.edit(
                f"{em.sukses}<b>Semua teks Anda yang mengganggu telah dihapus.</b>"
            )
        try:
            value = int(value) - 1
            auto_text_vars.pop(value)
            await dB.set_var(client.me.id, "AUTO_GCAST", auto_text_vars)
            return await msg.edit(
                f"{em.sukses}<b>Nomor Teks : <code>{value+1}</code> dihapus.</b>"
            )
        except Exception as error:
            return await msg.edit(str(error))

    elif type == "get":
        if not auto_text_vars:
            return await msg.edit(
                f"{em.gagal}<b>Teks Auto Gcast Anda kosong, idiot.</b>"
            )
        txt = "<b>Teks Gcast mengganggu Anda</b>\n\n"
        data = await text_autogcast(client)
        for num, x in enumerate(data, 1):
            txt += f"{num}: {x}\n\n"
        return await msg.edit(txt)

    elif type == "limit":
        if value == "off":
            if client.me.id in LT:
                LT.remove(client.me.id)
                return await msg.edit(f"{em.gagal}<b>Auto Limit dimatikan.</b>")
            else:
                return await msg.delete()

        elif value == "on":
            if client.me.id not in LT:
                LT.append(client.me.id)
                await msg.edit(f"{em.sukses}<b>Auto Limit dinyalakan.</b>")
                while client.me.id in LT:
                    for x in range(2):
                        await spam_bot(client, message, _)
                        await asyncio.sleep(5)
                    await asyncio.sleep(1200)
            else:
                return await msg.delete()
        else:
            return await msg.edit(
                f"{em.gagal}<b>Salah goblok!! Makanya baca  Command Help.</b>"
            )
    else:
        return await msg.edit(
            f"{em.gagal}<b>Salah goblok!! Makanya baca  Command Help.</b>"
        )
    return


async def add_auto_text(message):
    client = message._client
    auto_text = await dB.get_var(client.me.id, "AUTO_GCAST") or []
    rep = message.reply_to_message
    value = None
    logs = "me"
    type_mapping = {
        "text": rep.text,
        "photo": rep.photo,
        "voice": rep.voice,
        "audio": rep.audio,
        "video": rep.video,
        "video_note": rep.video_note,
        "animation": rep.animation,
        "sticker": rep.sticker,
        "document": rep.document,
        "contact": rep.contact,
    }
    for media_type, media in type_mapping.items():
        if media:
            send = await rep.copy(logs)
            value = {
                "type": media_type,
                "message_id": send.id,
            }
            break
    if value:
        auto_text.append(value)
        await dB.set_var(client.me.id, "AUTO_GCAST", auto_text)
