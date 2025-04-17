from Haji import bot
from Haji.helpers import CMD, ButtonUtils, Emoji

__MODULES__ = "Alive"
__HELP__ = """
<blockquote>⪼ **--Command help Alive--**</blockquote>

<blockquote>**Status Userbot**</blockquote>
**ᐉ Keterangan: Untuk mengetahui status userbot Anda**
ᐈ Perintah: `{0}alive`
    
<b>   {1}</b>
"""

@CMD.UBOT("alive")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    query = "alive"
    try:
        inline = await ButtonUtils.send_inline_bot_result(
            message, message.chat.id, bot.me.username, query
        )
        if inline:
            return await message.delete()
    except Exception as error:
        return await message.reply(f"{em.gagal}Error: {str(error)}")
