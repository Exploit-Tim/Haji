import asyncio
import os

import cv2
from PIL import Image

from Haji.helpers import CMD, Emoji, Message, Sticker, Tools

__MODULES__ = "Tiny"
__HELP__ = """
<blockquote>⪼ **--Command help Tiny--**</blockquote>

<blockquote>**Convert to small size** </blockquote>
**ᐉ Keterangan: Anda dapat mengubah ukuran stiker menjadi kecil**
ᐈ Perintah: `{0}tiny` (reply image)

<b>   {1}</b>
"""


@CMD.UBOT("tiny")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    await Sticker.dl_font()
    rep = message.reply_to_message
    proses_ = await em.get_costum_text()
    pros = await message.reply(f"{em.proses}**{proses_[4]}**")
    if not rep:
        return await pros.edit(f"{em.gagal}**Please reply to sticker or photo!**")
    doc = await client.download_media(rep)
    im1 = Image.open("font-module/bahan2.png")
    if doc.endswith(".tgs"):
        await client.download_media(rep, "man.tgs")
        await Tools.bash("lottie_convert.py man.tgs json.json")
        json = open("json.json", "r")
        jsn = json.read()
        jsn = jsn.replace("512", "2000")
        ("json.json", "w").write(jsn)
        await Tools.bash("lottie_convert.py json.json man.tgs")
        file = "man.tgs"
        os.remove("json.json")
    elif doc.endswith((".gif", ".mp4")):
        idoc = cv2.VideoCapture(doc)
        busy = idoc.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(doc)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    await asyncio.gather(
        pros.delete(),
        client.send_sticker(
            message.chat.id,
            sticker=file,
            reply_to_message_id=Message.ReplyCheck(message),
        ),
    )
    os.remove(file)
    os.remove(doc)
    return
