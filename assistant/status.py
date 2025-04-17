from time import time

from pyrogram.helpers import kb
from pyrogram.raw.functions import Ping
from pyrogram.types import ReplyKeyboardRemove
from pytz import timezone

from config import BOT_NAME, SUDO_OWNERS
from Haji import haji
from Haji.database import dB
from Haji.helpers import CMD, get_time, start_time


@CMD.BOT("close")
async def _(client, message):
    return await message.reply_text(
        "<b>ᴋᴇʏʙᴏᴀʀᴅ ᴅɪᴛᴜᴛᴜᴘ</b>", reply_markup=ReplyKeyboardRemove()
    )


async def cek_status_akun(client, message):
    user_id = message.from_user.id
    seles = await dB.get_list_from_var(client.me.id, "SELLER")
    if user_id not in haji._get_my_id:
        status2 = "tidak aktif"
    else:
        status2 = "aktif"
    if user_id in SUDO_OWNERS:
        status = "<b>[Admins]</b>"
    elif user_id in seles:
        status = "<b>[Seller]</b>"
    else:
        status = "<b>[Costumer]</b>"
    uptime = await get_time((time() - start_time))
    await client.invoke(Ping(ping_id=0))
    exp = await dB.get_expired_date(user_id)
    habis = (
        exp.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
        if exp
        else "None"
    )
    prefix = client.get_prefix(user_id)
    keyboard = kb([["↩️ Beranda"]], resize_keyboard=True, one_time_keyboard=True)
    return await message.reply(
        f"""
<blockquote>
<b>{BOT_NAME}</b>
    <b>ꜱᴛᴀᴛᴜꜱ ᴜʙᴏᴛ :</b> <code>{status2}</code>
      <b>ꜱᴛᴀᴛᴜꜱ ᴘᴇɴɢɢᴜɴᴀ :</b> <i>{status}</i>
      <b>ᴘʀᴇꜰɪxᴇꜱ :</b> <code>{' '.join(prefix)}</code>
      <b>ᴛᴀɴɢɢᴀʟ ᴋᴇᴅᴀʟᴜᴡᴀʀꜱᴀ :</b> <code>{habis}</code>
      <b>ᴜᴘᴛɪᴍᴇ ᴜʙᴏᴛ :</b> <code>{uptime}</code>
</blockquote>
""",
        reply_markup=keyboard,
    )
