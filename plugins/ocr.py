import requests

from Haji.helpers import CMD, Emoji, Tools

__MODULES__ = "Ocr"
__HELP__ = """
<blockquote>⪼ **--Command help Ocr--**</blockquote>

<blockquote>**Read text from image**</blockquote>
**ᐉ Keterangan: Perintah ini bisa mendapatkan teks dari gambar**
ᐈ Perintah: `{0}ocr` (reply image)

<b>   {1}</b>
"""


@CMD.UBOT("ocr|read")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    reply = message.reply_to_message
    if not reply or not reply.photo and not reply.sticker and not reply.animation:
        return await message.reply_text(
            f"{em.gagal}`{message.text.split()[0]}` **reply to media!**"
        )
    proses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_[4]}**")
    try:
        url = await Tools.upload_media(message)
        req = requests.get(
            f"https://script.google.com/macros/s/AKfycbwURISN0wjazeJTMHTPAtxkrZTWTpsWIef5kxqVGoXqnrzdLdIQIfLO7jsR5OQ5GO16/exec?url={url}"
        ).json()
        return await proses.edit(f"{em.sukses}<code>{req['text']}</code>")
    except Exception as e:
        return await proses.edit(f"{em.gagal}**ERROR:** {str(e)}")
