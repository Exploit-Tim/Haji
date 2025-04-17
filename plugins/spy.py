import os
from Haji import haji
from Haji.helpers import Emoji, CMD

__MODULES__ = "Spy"
__HELP__ = """
<blockquote>⪼ **--Command help Spy--**</blockquote>
  
**ᐉ Keterangan: Curi pengatur waktu pap (bukan hanya tampilan satu kali)**
ᐈ Perintah: `{0}spy`
    
<b>   {1}</b>
"""


@CMD.UBOT("curi|spy")
async def _(c: haji, m):
    em = Emoji(c)
    dia = m.reply_to_message
    if not dia:
        return
    logs = "me"
    anjing = dia.caption or ""
    await m.delete()

    if dia.photo or dia.video or dia.audio or dia.voice or dia.document:
        anu = await c.download_media(dia)

        if os.path.getsize(anu) == 0:
            os.remove(anu)
            return await c.send_message(logs, f"{em.gagal} Gagal mengunduh media.")

        try:
            if dia.photo:
                return await c.send_photo(logs, anu, anjing)
            elif dia.video:
                return await c.send_video(logs, anu, anjing)
            elif dia.audio:
                return await c.send_audio(logs, anu, anjing)
            elif dia.voice:
                return await c.send_voice(logs, anu, anjing)
            elif dia.document:
                return await c.send_document(logs, anu, anjing)
        except Exception as e:
            return await c.send_message(logs, f"{em.gagal} Gagal mengirim media.\n<b>Error:</b> <code>{e}</code>")
    else:
        return await c.send_message(logs, f"{em.sukses} Pesan berhasil disadap dan dikirim ke log.")
