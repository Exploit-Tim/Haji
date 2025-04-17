import asyncio
import random
from random import choice

from pyrogram import enums, types

from Haji.helpers import CMD, Emoji

__MODULES__ = "Asupan"
__HELP__ = """
<blockquote>⪼ **--Command help Asupan--**</blockquote>

<blockquote>**Cari pap**</blockquote>
**ᐉ Keterangan: Nyari pap cewe**
ᐈ Perintah: `{0}cewek`
**ᐉ Keterangan: Nyari pap cowo**
ᐈ Perintah: `{0}cowok`
**ᐉ Keterangan: Random pap**
ᐈ Perintah: `{0}pap`
**ᐉ Keterangan: Nyari pp couple**
ᐈ Perintah: `{0}ppcp`
    
<blockquote>**Cari video**</blockquote>
**ᐉ Keterangan: Cari video asupan random**
ᐈ Perintah: `{0}asupan`
    
<b>   {1}</b>
"""


@CMD.UBOT("asupan")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    y = await message.reply(f"<b>{em.proses}{proses_[4]}...</b>")
    await asyncio.sleep(3)
    try:
        asupannya = []
        async for asupan in client.search_messages(
            "@AsupanNyaSaiki", filter=enums.MessagesFilter.VIDEO
        ):
            asupannya.append(asupan)
        video = random.choice(asupannya)
        await video.copy(
            message.chat.id,
            caption=f"{em.sukses}<b>Upload by: <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        return await y.delete()
    except Exception:
        return await y.edit(f"{em.gagal}<b>Try a gain!</b>")


@CMD.UBOT("cewek")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    y = await message.reply(f"<b>{em.proses}{proses_[4]}...</b>")
    await asyncio.sleep(3)
    try:
        ayangnya = []
        async for ayang in client.search_messages(
            "@cewekbyzeeb", filter=enums.MessagesFilter.PHOTO
        ):
            ayangnya.append(ayang)
        photo = random.choice(ayangnya)
        await photo.copy(
            message.chat.id,
            caption=f"{em.sukses}<b>Upload by: <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        return await y.delete()
    except Exception:
        return await y.edit(f"{em.gagal}<b>Try a gain!</b>")


@CMD.UBOT("cowok")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    y = await message.reply(f"<b>{em.proses}{proses_[4]}...</b>")
    await asyncio.sleep(3)
    try:
        ayang2nya = []
        async for ayang2 in client.search_messages(
            "@cowokbyzeeb", filter=enums.MessagesFilter.PHOTO
        ):
            ayang2nya.append(ayang2)
        photo = random.choice(ayang2nya)
        await photo.copy(
            message.chat.id,
            caption=f"{em.sukses}<b>Upload by: <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=message.id,
        )
        return await y.delete()
    except Exception:
        return await y.edit(f"{em.gagal}<b>Try a gain!</b>")


@CMD.UBOT("pap")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    y = await message.reply(f"<b>{em.proses}{proses_[4]}...</b>")
    await asyncio.sleep(3)
    await message.reply_photo(
        choice(
            [
                lol.photo.file_id
                async for lol in client.search_messages(
                    "@mm_kyran", filter=enums.MessagesFilter.PHOTO
                )
            ]
        ),
        False,
        caption=f"{em.sukses}<b>Ange ga kamu???</b>",
    )
    await y.delete()


@CMD.UBOT("ppcp")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    pros = await message.reply(
        f"{emo.proses}<b>Proses mengunduh Foto Profil berpasangan ..</b>"
    )

    url = "medialuci"
    ppcp_pairs = []

    try:
        photos = []
        async for media in client.search_messages(
            url, filter=enums.MessagesFilter.PHOTO
        ):
            photos.append(media.photo.file_id)

        if len(photos) < 2:
            return await pros.edit(
                f"{emo.gagal}<b>Gagal menemukan pasangan foto profil. Coba lagi nanti.</b>"
            )

        for i in range(0, len(photos) - 1, 2):
            ppcp_pairs.append([photos[i], photos[i + 1]])

        selected_pair = random.choice(ppcp_pairs)

        media_group = [types.InputMediaPhoto(photo) for photo in selected_pair]

        await client.send_media_group(
            message.chat.id,
            media=media_group,
            reply_to_message_id=message.id,
        )
        await pros.delete()

    except Exception as error:
        await pros.edit(f"{emo.gagal}<b>Error:</b>\n<code>{error}</code>")
