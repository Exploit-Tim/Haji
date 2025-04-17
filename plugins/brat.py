import os
import uuid
import requests
from Haji.helpers import CMD, Emoji
from config import API_BOTCHAX

__MODULES__ = "Brat"
__HELP__ = 
"""<blockquote>⪼ **--Command help Brat--**</blockquote>

<blockquote>**Create brat-style image**</blockquote>
*ᐉ Keterangan: *Generate a brat-style image from text**
ᐈ Perintah: `{0}brat` (text or reply)

<b>   {1}</b>
"""

@CMD.UBOT("brat")
async def _(client, message):
    em = Emoji(client)
    await em.get()

    args = message.text.split(" ", 1)

    if len(args) >= 2:
        pepek = args[1]
    elif message.reply_to_message and message.reply_to_message.text:
        pepek = message.reply_to_message.text
    else:
        await message.reply_text(f"**{em.gagal} Use `.brat ` or reply to a text message.**")
        return

    processing = await message.reply_text(f"**{em.proses} Generating image...**")

    try:
        url = f"https://api.botcahx.eu.org/api/maker/brat?text={pepek}&apikey={API_BOTCHAX}"
        response = requests.get(url)
        response.raise_for_status()

        if response.headers.get("Content-Type", "").startswith("image/"):
            temp_file = f"brat_{uuid.uuid4().hex}.webp"
            with open(temp_file, "wb") as f:
                f.write(response.content)
 
            await message.reply_sticker(sticker=temp_file)
            await processing.delete()
            os.remove(temp_file)
        else:
            await processing.edit(f"**{em.gagal} Failed to generate image. Try again later.**")
    except:
        await processing.edit(f"**{em.gagal} API error. Please try again later.**")
