from pyrogram.errors import MessageTooLong

from config import API_BOTCHAX
from Haji.helpers import CMD, Emoji, Tools

__MODULES__ = "Chord"
__HELP__ = """
<blockquote>⪼ **--Command help Chord--**</blockquote>

<blockquote>**Cari chord lagu**</blockquote>
**ᐉ Keterangan: Anda bisa mendapatkan chord dari lagu**
ᐈ Perintah: `{0}chord` (title)

<blockquote>**Cari lirik lagu**</blockquote>
**ᐉ Keterangan: Anda bisa mendapatkan lirik dari lagu**
ᐈ Perintah: `{0}lirik` (title)
 
<b>   {1}</b>
"""


@CMD.UBOT("chord")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    prs = await message.reply_text(f"{em.proses}**{proses_[4]}**")
    rep = message.reply_to_message
    if len(message.command) < 2 and not rep:
        return await prs.edit(f"{em.gagal}**Please give song or lyrics.!!**")
    arg = client.get_text(message)
    url = f"https://api.botcahx.eu.org/api/search/chord?song={arg}&apikey={API_BOTCHAX}"
    msg = ""
    respon = await Tools.fetch.get(url)
    if respon.status_code == 200:
        data = respon.json()
        fileds = {
            "Song title": data["result"].get("title", "-"),
            "Song chord": data["result"].get("chord", "-"),
        }
        msg = "\n".join([f"{key}: {value}" for key, value in fileds.items()])
        try:
            await prs.delete()
            return await message.reply(msg)
        except MessageTooLong:
            await prs.delete()
            konten = str(msg)
            link = await Tools.paste(konten)
            return await message.reply(
                f"{em.sukses}**[Click here]({link}) to view song of the chord.**",
                disable_web_page_preview=True,
            )
    else:
        return await prs.edit(f"**{em.gagal}Please try again: {respon.status_code}!**")


@CMD.UBOT("lirik")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    prs = await message.reply_text(f"{em.proses}**{proses_[4]}**")
    rep = message.reply_to_message
    if len(message.command) < 2 and not rep:
        return await prs.edit(f"{em.gagal}**Please give song title or lyrics.!!**")
    arg = client.get_text(message)
    url = (
        f"https://api.botcahx.eu.org/api/search/lirik?lirik={arg}&apikey={API_BOTCHAX}"
    )
    msg = ""
    respon = await Tools.fetch.get(url)
    if respon.status_code == 200:
        data = respon.json()
        fileds = {
            "Song title": data["result"].get("title", "-"),
            "Lyrics": data["result"].get("lyrics", "-"),
        }
        msg = "\n".join([f"{key}: {value}" for key, value in fileds.items()])
        try:
            await prs.delete()
            return await message.reply(msg)
        except MessageTooLong:
            await prs.delete()
            konten = str(msg)
            link = await Tools.paste(konten)
            return await message.reply(
                f"{em.sukses}**[Click here]({link}) to view song of the chord.**",
                disable_web_page_preview=True,
            )
    else:
        return await prs.edit(f"**{em.gagal}Please try again: {respon.status_code}!**")
