import os
from Haji.helpers import CMD
import requests

MODULE = "Fluxai"
HELP = """
<blockquote>⪼ **--Command help Fluxai--**</blockquote>

**ᐉ Keterangan: Untuk Membuat Gambar Text To Img**
ᐈ Perintah: `{0}fluxai` (text)
"""

def fluxai(text):
    url = f"https://api.siputzx.my.id/api/ai/flux"
    params = {
        "prompt": text,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None
        
@CMD.UBOT("fluxai|flux")
async def _(client, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("❌ Gunakan Perintah .fluxai  Untuk Membuat Txt2Img.")
        return

    request_text = args[1]
    await message.reply_text("⏰ Sedang Memproses, Mohon Tunggu...")

    image_content = fluxai(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")
