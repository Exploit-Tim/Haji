from Haji import haji
from Haji.helpers import AFK_, CMD, Emoji

__MODULES__ = "AFK"
__HELP__ = """
<blockquote>⪼ **--Command help Afk--**</blockquote>

<blockquote>**Aktifkan mode afk**</blockquote>
**ᐉ Keterangan: Mengatur status akun Anda ke mode AFK**
ᐈ Perintah: `{0}afk` (alasan)
    
<blockquote>**Nonaktifkan mode afk**</blockquote>
**ᐉ Keterangan: Setelah mode AFK aktif, Anda dapat mengatur ke mode UNAFK**
ᐈ Perintah: `{0}unafk`

<b>   {1}</b>
"""


@CMD.NO_CMD("REP_BLOCK", haji)
async def _(client, message):
    em = Emoji(client)
    await em.get()
    return await message.reply_text(
        f"{em.block}**Dilarang reply chat gua, Lu udah gua blokir mek!!**"
    )


@CMD.UBOT("afk")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    rep = message.reply_to_message
    if not rep:
        return await message.reply(f"{emo.gagal}<b>Harap balas ke pesan!!</b>")
    return await AFK_.set_afk(client, message, emo)


@CMD.NO_CMD("AFK", haji)
@CMD.capture_err
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    return await AFK_.get_afk(client, message, emo)


@CMD.UBOT("unafk")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    return await AFK_.unset_afk(client, message, emo)
