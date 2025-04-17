__MODULES__ = "Spotipy"
__HELP__ = """
<blockquote>⪼ **--Command help Spotify--**</blockquote> 

<blockquote>**Download song spotify**</blockquote>
**ᐉ Keterangan: Anda dapat mengunduh lagu di spotify dari judul atau url**
ᐈ Perintah: `{0}spotdl` (title/url)

<b>   {1}</b>
"""

import traceback
from uuid import uuid4

from config import API_BOTCHAX
from Haji import bot
from Haji.database import state
from Haji.helpers import CMD, ButtonUtils, Emoji, Tools
from Haji.logger import logger


@CMD.UBOT("spotify|spotdl")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    arg = client.get_text(message)
    if not arg:
        return await message.reply(
            f"{em.gagal}<b>Please give word or links!!\nExample: `{message.text.split()[0]} https://open.spotify.com/track/1hlHeIZ36Idpr57xPI8OCD` or `{message.text.split()[0]} garam & madu`</b>"
        )
    proses = await message.reply(f"{em.proses}**{proses_[4]}**")
    await proses.edit(f"{em.proses}**Wait a minute this takes some time...**")
    if arg.startswith("https://"):
        try:
            media, caption = await Tools.download_spotify(arg)
            if (media, caption) is not None:
                await proses.edit(f"{em.proses}**Try to sending the audio...**")
                await message.reply_audio(media, caption=caption)
                return await proses.delete()
        except Exception as er:
            logger.error(f"spotdl: {traceback.format_exc()}")
            return await proses.edit(f"{em.gagal}**An error: `{str(er)}`**")
    else:
        url = f"https://api.botcahx.eu.org/api/search/spotify?query={arg}&apikey={API_BOTCHAX}"
        try:
            response = await Tools.fetch.get(url)
            uniq = f"{str(uuid4())}"
            if response.status_code == 200:
                data = response.json()["result"]
                state.set(client.me.id, uniq.split("-")[0], data["data"])
                state.set(client.me.id, "idm_spotdl", id(message))
                inline = await ButtonUtils.send_inline_bot_result(
                    message,
                    message.chat.id,
                    bot.me.username,
                    f"inline_spotify {uniq.split('-')[0]}",
                )
                if inline:
                    await proses.delete()
                return
            else:
                return await proses.edit(
                    f"{em.gagal}**Please try again {response.status_code}**"
                )
        except Exception as er:
            logger.error(f"ttdl: {traceback.format_exc()}")
            return await proses.edit(f"{em.gagal}**An error: `{str(er)}`**")
