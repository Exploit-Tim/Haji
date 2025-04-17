__MODULES__ = "Bola"
__HELP__ = """
<blockquote>⪼ **--Command help Bola--**</blockquote>

<blockquote>**Dapatkan pertandingan sepak bola hari ini**</blockquote>
**ᐉ Keterangan: Dapatkan jadwal berita bola hari ini**
ᐈ Perintah: `{0}bola`

<b>   {1}</b>
"""

from Haji import bot
from Haji.helpers import CMD, ButtonUtils


@CMD.UBOT("bola")
async def _(_, message):
    try:
        inline = await ButtonUtils.send_inline_bot_result(
            message, message.chat.id, bot.me.username, "inline_bola"
        )
        if inline:
            return await message.delete()
    except Exception as er:
        return await message.reply(f"**ERROR**: {str(er)}")
