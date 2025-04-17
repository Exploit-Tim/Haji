from telegraph import Telegraph
from pyrogram.types import Message
from Haji.helpers import CMD
from Haji import haji

__MODULES__ = "Telegraph"
__HELP__ = """
<blockquote>⪼ **--Command help Telegraph--**</blockquote>

**ᐉ Keterangan: Mengupload teks ke Telegraph**
ᐈ Perintah: `{0}telegraph (reply teks) [judul]`

<blockquote>**Contoh:**</blockquote>
ᐈ Perintah: `{0}telegraph Catatan Rapat Hari Ini`

<b>   {1}</b>
"""

telegraph = Telegraph()
telegraph.create_account(short_name="userbot")

@CMD.UBOT("telegraph")
async def upload_to_telegraph(_, m: Message):
    if not m.reply_to_message or not m.reply_to_message.text:
        return await m.reply("❗ Balas ke pesan teks yang ingin diupload.")
    
    title = " ".join(m.command[1:]) if len(m.command) > 1 else "Tanpa Judul"
    content = m.reply_to_message.text

    try:
        response = telegraph.create_page(
            title=title,
            html_content=content.replace("\n", "<br>")
        )
        link = f"https://telegra.ph/{response['path']}"
        await m.reply(f"✅ <b>Berhasil diupload ke Telegraph!</b>\n\n🔗 <a href='{link}'>Klik di sini untuk melihat</a>", disable_web_page_preview=True)
    except Exception as e:
        await m.reply(f"❌ Gagal upload ke Telegraph:\n<code>{e}</code>")
