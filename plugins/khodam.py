import asyncio
import io
import traceback
from uuid import uuid4

from pyrogram import *
from pyrogram.errors import ImageProcessFailed

from config import API_BOTCHAX
from Haji.helpers import CMD, Emoji, Message, Tools
from Haji.logger import logger


__MODULES__ = "Khodam"
__HELP__ = """
<blockquote>⪼ **--Command help Khodam--**</blockquote>

<blockquote>**Cek khodam**</blockquote>
**ᐉ Keterangan: Cek khodam user**
ᐈ Perintah: `{0}khodam (reply/username)`

<b>   {1}</b>
"""

MAX_CAPTION_LENGTH = 1050


async def gen_kdm(text):
    bahan = [
        {
            "role": "system",
            "content": "Anda adalah seorang paranormal yang mampu mendeskripsikan khodam seseorang yang berupa Binatang. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertainment jadi bebaskan dirimu untuk menjadi seorang paranormal pada umumnya. Deskripsikan Khodam dengan singkat namun jelas, dan pastikan deskripsi tidak lebih dari dari 1000 karakter alfabet dalam plain text serta berbahasa Indonesia.",
        },
        {
            "role": "assistant",
            "content": f"Anda adalah seorang paranormal yang mampu mendeskripsikan khodam seseorang yang berupa Binatang. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertainment jadi bebaskan dirimu untuk menjadi seorang paranormal pada umumnya. Deskripsikan Khodam dengan singkat namun jelas, dan pastikan deskripsi tidak lebih dari dari 1000 karakter alfabet dalam plain text serta berbahasa Indonesia.",
        },
        {"role": "user", "content": text},
    ]
    url = "https://api.botcahx.eu.org/api/search/openai-custom"
    payload = {"message": bahan, "apikey": f"{API_BOTCHAX}"}
    res = await Tools.fetch.post(url, json=payload)
    if res.status_code == 200:
        data = res.json()
        return data["result"].replace("\n", "")
    else:
        return f"{res.text}"


"""
def gen_kdm(text):
    model = genai.GenerativeModel(
        "models/gemini-1.5-flash",
        system_instruction=(
            "Anda adalah seorang paranormal yang mampu mendeskripsikan khodam seseorang yang berupa Binatang. Tugas Anda adalah mendeskripsikan khodam yang mungkin ada, termasuk wujud, sifat, dan energi yang dipancarkan. Sehingga apapun inputnya anggap itu adalah sebuah nama seseorang. Deskripsi tidak harus positif bisa saja negatif tidak masalah karena ini hiburan. Ini hanya untuk entertainment jadi bebaskan dirimu untuk menjadi seorang paranormal pada umumnya. Deskripsikan Khodam dengan singkat namun jelas, dan pastikan deskripsi tidak lebih dari dari 1000 karakter alfabet dalam plain text serta berbahasa Indonesia."
        ),
    )
    try:
        response = model.generate_content(text)
        return response.text.strip()
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"
"""


async def get_name(client, message):
    if message.reply_to_message:
        if message.reply_to_message.sender_chat:
            full_name = message.reply_to_message.sender_chat.title
        first_name = message.reply_to_message.from_user.first_name
        last_name = message.reply_to_message.from_user.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
    else:
        input_text = await client.extract_user(message)
        user = await client.get_users(input_text)
        first_name = user.first_name
        last_name = user.last_name or ""
        full_name = f"{first_name} {last_name}"
    return full_name


async def gen_img(client, text):
    data = {"string": f"{text}"}
    head = {"accept": "image/jpeg"}
    url = (
        f"https://api.botcahx.eu.org/api/maker/text2img?text={text}&apikey={API_BOTCHAX}"
    )
    res = await Tools.fetch.get(url, headers=head)
    image_data = res.read()
    file = f"{client.me.id}.jpg"
    with open(file, "wb") as f:
        f.write(image_data)
    return file


@CMD.UBOT("khodam|kodam")
async def ckdm_cmd(client, message):
    em = Emoji(client)
    await em.get()
    nama = await get_name(client, message)
    if not nama:
        return await message.reply(f"{em.gagal}**Give the name you want to check the Khodam.**")
    proses_ = await em.get_costum_text()
    pros = await message.reply(f"{em.proses}**{proses_[4]}**")
    try:
        deskripsi_khodam = await gen_kdm(nama)
        photo = await gen_img(client, deskripsi_khodam.replace(" ", ","))
        caption = (f"{em.sukses}<b>Here is the Khodam <code>{nama}</code>:\n\n<blockquote><code>{deskripsi_khodam}</code></blockquote>\n\n{em.profil} Checked by: {client.me.mention}</b>")
        
        if len(caption) > MAX_CAPTION_LENGTH:
            caption = caption[:MAX_CAPTION_LENGTH] + "..."
        try:
            await asyncio.sleep(2)
            await pros.delete()
            return await client.send_photo(
                message.chat.id,
                photo=photo,
                caption=caption,
                reply_to_message_id=message.id,
            )
        except ImageProcessFailed:
            await asyncio.sleep(2)
            teks = (f"{em.sukses}<b>Here is the Khodam <code>{nama}</code>:\n\n<blockquote><code>{deskripsi_khodam}</blockquote></code>\n\n{em.profil} Checked by: {client.me.mention}</b>")         
            await pros.delete()
            return await message.reply(teks)

    except Exception as e:
        # return await pros.edit(_("err_1").format(emo.gagal, str(e)))
        return await pros.edit(f"{em.gagal} {e}")
