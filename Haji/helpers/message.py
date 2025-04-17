from typing import Optional

from pytz import timezone

from config import BOT_ID, BOT_NAME
from Haji import haji
from Haji.database import dB


class Message:
    """Enhanced message templates with modern formatting"""

    JAKARTA_TZ = timezone("Asia/Jakarta")

    # HTML formatting templates
    USER_MENTION = "<a href=tg://user?id={id}>{name}</a>"
    CODE_BLOCK = "<code>{text}</code>"
    SECTION_START = "<b>❏ {title}</b>"
    SECTION_ITEM = "<b>├ {label}:</b> {value}"
    SECTION_END = "<b>╰ {label}</b> {value}"

    @staticmethod
    def ReplyCheck(message):
        reply_id = None
        if message.reply_to_message:
            reply_id = message.reply_to_message.id
        elif not message.from_user:
            reply_id = message.id
        return reply_id

    @staticmethod
    async def _ads() -> str:
        txt = await dB.get_var(BOT_ID, "ads")
        if txt:
            msg = txt
        else:
            msg = "@DaddyHaji"
        return msg

    @classmethod
    def _format_user_mention(
        cls, user_id: int, first_name: str, last_name: Optional[str] = None
    ) -> str:
        """Format user mention with full name"""
        full_name = f"{first_name} {last_name or ''}".strip()
        return cls.USER_MENTION.format(id=user_id, name=full_name)

    @classmethod
    def expired_message(cls, client) -> str:
        """Generate expired account notification"""
        return f"""
{cls.SECTION_START.format(title="Notifikasi")}
{cls.SECTION_ITEM.format(
    label="Akun",
    value=cls._format_user_mention(client.me.id, client.me.first_name, client.me.last_name)
)}
{cls.SECTION_ITEM.format(label="ID", value=cls.CODE_BLOCK.format(text=client.me.id))}
{cls.SECTION_END.format(label="Status", value="Masa Aktif Telah Habis")}
"""

    @classmethod
    def welcome_message(cls, client, message) -> str:
        """Generate personalized welcome message"""
        return f"""
<blockquote><b>✨ sᴇʟᴀᴍᴀᴛ ᴅᴀᴛᴀɴɢ, {cls._format_user_mention(
    message.from_user.id,
    message.from_user.first_name,
    message.from_user.last_name
)}!</b>

<b>🤖 [{BOT_NAME}](https://t.me/{client.me.username})</u>, sᴀʏᴀ ᴀᴅᴀʟᴀʜ ʙᴏᴛ ʏᴀɴɢ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ᴅᴇɴɢᴀɴ ᴍᴜᴅᴀʜ.</b>

<b>ᴘᴀsᴛɪᴋᴀɴ sᴇʙᴇʟᴜᴍ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ᴀɴᴅᴀ ᴍᴇᴍʙᴀᴄᴀ ᴋᴇᴛᴇɴᴛᴜᴀɴ ᴘᴇᴍʙᴜᴀᴛᴀɴ ᴜsᴇʀʙᴏᴛ ᴀɢᴀʀ ᴍᴇɴᴄᴇɢᴀʜ ᴀᴋᴜɴ ᴀɴᴅᴀ ᴅᴀʀɪ ʙᴀɴɴᴇᴅ ᴀᴛᴀᴜᴘᴜɴ ᴛᴇʀ-ʟᴏɢᴏᴜᴛ.</b></blockquote>

<b>👉🏻 [ᴋᴇᴛᴇɴᴛᴜᴀɴ ᴘᴇᴍʙᴜᴀᴛᴀɴ ᴜsᴇʀʙᴏᴛ ʙᴀᴄᴀ ᴅɪ sɪɴɪ ⚠️](https://telegra.ph/RESIKO-USERBOT-03-07)</b>

<blockquote>ᴛᴇᴋᴀɴ ᴛᴏᴍʙᴏʟ <b>✨Mulai Buat Userbot</b> ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ.</blockquote>
"""

    @staticmethod
    async def userbot(count):
        expired_date = await dB.get_expired_date(haji._ubot[int(count)].me.id)
        expir = expired_date.astimezone(timezone("Asia/Jakarta")).strftime(
            "%Y-%m-%d %H:%M"
        )
        return f"""
<b>❏ ᴜꜱᴇʀʙᴏᴛ ᴋᴇ </b> <code>{int(count) + 1}/{len(haji._ubot)}</code>
<b>├ ᴀᴋᴜɴ :</b> <a href=tg://user?id={haji._ubot[int(count)].me.id}>{haji._ubot[int(count)].me.first_name} {haji._ubot[int(count)].me.last_name or ''}</a> 
<b>├ ɪᴅ :</b> <code>{haji._ubot[int(count)].me.id}</code>
<b>╰ ᴇxᴘɪʀᴇᴅ </b> <code>{expir}</code>
"""

    @staticmethod
    def deak(X):
        return f"""
<b>ᴀᴛᴛᴇɴᴛɪᴏɴ !!</b>
<b>ᴀᴋᴜɴ :</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>ɪᴅ :</b> <code>{X.me.id}</code>hak pengembalian dana
<b>ᴀʟᴀꜱᴀɴ :</b> <code>ᴅɪ ʜᴀᴘᴜs ᴅᴀʀɪ ᴛᴇʟᴇɢʀᴀᴍ</code>
"""

    @staticmethod
    async def policy_message() -> str:
        """Generate enhanced policy and terms message"""
        return f"""
<b>🤖 {BOT_NAME} - ᴋᴇʙɪᴊᴀᴋᴀɴ & ᴋᴇᴛᴇɴᴛᴜᴀɴ</b>

<b>💫 ᴋᴇʙɪᴊᴀᴋᴀɴ ᴘᴇɴɢᴇᴍʙᴀʟɪᴀɴ ᴅᴀɴᴀ</b>
• ᴀɴᴅᴀ ᴍᴇᴍɪʟɪᴋɪ ʜᴀᴋ ᴘᴇɴɢᴇᴍʙᴀʟɪᴀɴ ᴅᴀɴᴀ ᴅᴀʟᴀᴍ 𝟺𝟾 ᴊᴀᴍ ꜱᴇᴛᴇʟᴀʜ ᴘᴇᴍʙᴇʟɪᴀɴ
• ᴘᴇɴɢᴇᴍʙᴀʟɪᴀɴ ʜᴀɴʏᴀ ʙᴇʀʟᴀᴋᴜ ᴊɪᴋᴀ ᴀɴᴅᴀ ʙᴇʟᴜᴍ ᴍᴇɴɢɢᴜɴᴀᴋᴀɴ ʟᴀʏᴀɴᴀɴ
• ᴘᴇɴɢɢᴜɴᴀᴀɴ ꜰɪᴛᴜʀ ᴀᴘᴀᴘᴜɴ ᴍᴇɴɢʜɪʟᴀɴɢᴋᴀɴ ʜᴀᴋ ᴘᴇɴɢᴇᴍʙᴀʟɪᴀɴ ᴅᴀɴᴀ

<b>🛟 ᴅᴜᴋᴜɴɢᴀɴ ᴘᴇʟᴀɴɢɢᴀɴ</b>
• ᴘᴀɴᴅᴜᴀɴ ʟᴇɴɢᴋᴀᴘ ᴛᴇʀꜱᴇᴅɪᴀ ᴅɪ ʙᴏᴛ ɪɴɪ
• ɪɴꜰᴏʀᴍᴀꜱɪ ʀᴇꜱɪᴋᴏ ᴜꜱᴇʀʙᴏᴛ : [Baca Di Sini](https://telegra.ph/RESIKO-USERBOT-03-07)
• ᴘᴇᴍʙᴇʟɪᴀɴ = ᴘᴇʀꜱᴇᴛᴜᴊᴜᴀɴ ᴛᴇʀʜᴀᴅᴀᴘ ꜱᴇᴍᴜᴀ ʀᴇꜱɪᴋᴏ

<b>✅ ꜱᴇʟᴀɴᴊᴜᴛɴʏᴀ</b>
• ᴛᴇᴋᴀɴ 📃 <b>Saya Setuju</b> ᴜɴᴛᴜᴋ ᴍᴇʟᴀɴᴊᴜᴛᴋᴀɴ ᴘᴇᴍʙᴇʟɪᴀɴ
• ᴛᴇᴋᴀɴ 🏠 <b>Menu Utama</b> ᴜɴᴛᴜᴋ ᴋᴇᴍʙᴀʟɪ

<b>📢 {await Message._ads()}</b>
"""

    @staticmethod
    def TEXT_PAYMENT(harga, total, bulan):
        return f"""
<blockquote><b>ꜱɪʟᴀᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ, ᴀᴛᴀᴜ ʜᴜʙᴜɴɢɪ @PakHajiCabul ᴜɴᴛᴜᴋ ᴍᴇɴᴅᴀᴘᴀᴛᴋᴀɴ ᴀᴋꜱᴇꜱ ᴜꜱᴇʀʙᴏᴛ. </b>

<b> ʜᴀʀɢᴀ ʙᴜʟᴀɴᴀɴ : <code>{harga}</code></b>


<b> 🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ : Rp.<code>{total}</code> </b>
<b> 🗓️ ᴛᴏᴛᴀʟ ʙᴜʟᴀɴ : <code> {bulan} </code> </b> 

<b> ✅ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴊɪᴋᴀ ᴀɴᴅᴀ ꜱᴜᴅᴀʜ ᴍᴇɴᴇɴᴛᴜᴋᴀɴ ᴘɪʟɪʜᴀɴ.</b></blockquote>
"""
