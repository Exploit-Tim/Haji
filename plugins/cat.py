__MODULES__ = "Cat"
__HELP__ = """
<blockquote>⪼ **--Command help Cat--**</blockquote>

<blockquote>**Dapatkan gambar kucing random**</blockquote>
**ᐉ Keterangan: Anda bisa mendapatkan gambar random kucing lucu**
ᐈ Perintah: `{0}cats`
    
<b>   {1}</b>
"""


from Haji import bot
from Haji.helpers import CMD, ButtonUtils


@CMD.UBOT("cats")
async def _(_, message):
    try:
        inline = await ButtonUtils.send_inline_bot_result(
            message, message.chat.id, bot.me.username, "inline_cat"
        )
        if inline:
            return await message.delete()
    except Exception as er:
        return await message.reply(f"**ERROR**: {str(er)}")
