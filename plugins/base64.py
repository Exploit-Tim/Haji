import base64
from pyrogram.types import Message
from Haji import haji
from Haji.helpers import CMD

__MODULES__ = "Base64"
__HELP__ = """
<blockquote>⪼ **--Command help Base64--**</blockquote>

<blockquote>**Enkripsi teks**</blockquote>
**ᐉ Keterangan: Anda bisa mengenkripsi teks dengan base64**
ᐈ Perintah: `{0}encode`
<blockquote>**Membuka enkripsi**</blockquote>
**ᐉ Keterangan: Anda bisa membuka enkripsi base64**
ᐈ Perintah: `{0}decode`

<b>   {1}</b>
"""


# Fungsi untuk memastikan hanya akun userbot yang bisa akses
def is_self_userbot(message: Message) -> bool:
    return message.from_user and message.from_user.is_self

@CMD.UBOT("encode")
async def encode_b64(_, message: Message):
    if not is_self_userbot(message):
        return

    if len(message.command) < 2:
        return await message.reply("❗ Masukkan teks yang ingin di-encode.")

    text = " ".join(message.command[1:])
    try:
        encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        await message.reply(
            f"📥 <b>Teks Asli:</b>\n<code>{text}</code>\n\n"
            f"📤 <b>Base64:</b>\n<code>{encoded}</code>"
        )
    except Exception as e:
        await message.reply(f"🚫 Terjadi kesalahan saat encode:\n<code>{e}</code>")

@CMD.UBOT("decode")
async def decode_b64(_, message: Message):
    if not is_self_userbot(message):
        return

    if len(message.command) < 2:
        return await message.reply("❗ Masukkan teks base64 yang ingin di-decode.")

    b64text = " ".join(message.command[1:])
    try:
        decoded = base64.b64decode(b64text.encode("utf-8")).decode("utf-8")
        await message.reply(
            f"📤 <b>Base64:</b>\n<code>{b64text}</code>\n\n"
            f"📥 <b>Teks Asli:</b>\n<code>{decoded}</code>"
        )
    except Exception as e:
        await message.reply(f"🚫 Terjadi kesalahan saat decode:\n<code>{e}</code>")
