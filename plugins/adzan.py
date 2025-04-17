__MODULES__ = "Adzan"
__HELP__ = """
<blockquote>⪼ **--Command help Adzan--**</blockquote>

<blockquote>**Dapatkan jadwal adzan hari ini**</blockquote>
**ᐉ Keterangan: Dapatkan jadwal adzan**
ᐈ Perintah: `{0}adzan` (kota+negara)
    
<b>   {1}</b>
"""


from config import API_MAELYN
from Haji.helpers import CMD, Emoji, Tools


@CMD.UBOT("adzan")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    prs = await message.reply_text(f"{em.proses}**{proses_[4]}**")
    message.reply_to_message
    if len(message.command) < 3:
        return await prs.edit(
            f"{em.gagal}**Tolong berikan nama kota+negara!!\nContoh : `{message.text.split()[0]} jakarta indonesia`**"
        )
    city = message.text.split(None, 1)[1]
    coutry = message.text.split(None, 2)[2]
    url = f"https://api.maelyn.tech/api/jadwalsholat?city={city}&country={coutry}&apikey={API_MAELYN}"
    msg = ""
    respon = await Tools.fetch.get(url)
    if respon.status_code == 200:
        data = respon.json()
        date = data["result"]["date"]
        timings = data["result"]["timings"]
        meta = data["result"]["meta"]
        msg += f"**📅 Date**\n"
        msg += f"• Gregorian: {date['gregorian']}\n"
        msg += f"• Hijri: {date['hijri']}\n\n"
        msg += f"**🕰️ waktu**\n"
        msg += f"• Imsak: {timings['Imsak']}\n"
        msg += f"• Subuh: {timings['Fajr']}\n"
        msg += f"• Syuruq: {timings['Sunrise']}\n"
        msg += f"• Dhuhr: {timings['Dhuhr']}\n"
        msg += f"• Asr: {timings['Asr']}\n"
        msg += f"• Maghrib: {timings['Maghrib']}\n"
        msg += f"• Isha: {timings['Isha']}\n\n"
        msg += f"**🌍 Meta**\n"
        msg += f"• Timezone: {meta['timezone']}\n"
        msg += f"• Method: {meta['method']}\n"
        msg += f"• Location: {meta['location']}"
    else:
        msg = f"{em.gagal}**Error: {respon.status_code}**"
    return await prs.edit(f"<blockquote>{msg}</blockquote>")
