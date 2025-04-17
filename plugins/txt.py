from pyrogram.types import Message
from Haji.helpers import CMD
import io

__MODULES__ = "Txt"
__HELP__ = """
<blockquote>⪼ **--Command help Txt--**</blockquote>

<blockquote>**Fitur mengubah pesan menjadi file .txt**</blockquote>
**ᐉ Keterangan: Bot akan mengubah pesan menjadi dokumen .txt**
ᐈ Perintah: `{0}txt` (reply) (namafile)
**ᐉ Keterangan: Menampilkan isi file .txt**
ᐈ Perintah: `{0}readtxt` (reply file .txt)

<b>   {1}</b>
"""

@CMD.UBOT("txt")
async def save_txt_handler(client, message: Message):
    reply = message.reply_to_message
    if not reply:
        return await message.reply("❗ Balas pesan yang ingin disimpan sebagai file .txt")

    content = ""
    if reply.text:
        content = reply.text
    elif reply.caption:
        content = reply.caption
    else:
        return await message.reply("❗ Pesan tidak memiliki teks yang bisa disimpan.")

    # Ambil nama file dari teks setelah perintah
    custom_name = message.text.split(" ", 1)[1] if " " in message.text else None
    filename = f"{custom_name}.txt" if custom_name else f"saved_message_{reply.id}.txt"

    file_stream = io.BytesIO(content.encode("utf-8"))
    file_stream.name = filename

    await message.reply_document(file_stream, caption=f"✅ Disimpan sebagai <code>{filename}</code>")

@CMD.UBOT("readtxt")
async def read_txt_handler(client, message: Message):
    reply = message.reply_to_message
    if not reply or not reply.document:
        return await message.reply("❗ Balas file .txt yang ingin dibaca.")

    if not reply.document.file_name.endswith(".txt"):
        return await message.reply("❗ File bukan berformat .txt.")

    file = await reply.download()
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return await message.reply(f"❌ Gagal membaca file:\n<code>{e}</code>")

    if len(content) > 4096:
        return await message.reply("❗ Isi file terlalu panjang untuk dikirim sebagai pesan.")

    await message.reply(f"📄 <b>Isi file:</b>\n\n<code>{content}</code>")
