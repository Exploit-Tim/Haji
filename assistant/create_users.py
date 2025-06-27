import asyncio
import importlib
from datetime import datetime

import hydrogram
from dateutil.relativedelta import relativedelta
from pyrogram.helpers import ikb, kb
from pyrogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove)
from pytz import timezone

from config import API_HASH, API_ID, LOG_SELLER, MAX_BOT
from Haji import AKSES_DEPLOY, BOT_ID, UserBot, bot, dB, haji
from Haji.helpers import CMD, ButtonUtils, Message, no_trigger
from Haji.logger import logger
from plugins import PLUGINS


async def setExpiredUser(user_id):
    seles = await dB.get_list_from_var(BOT_ID, "SELLER")
    if user_id in seles:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=12)
        await dB.set_expired_date(user_id, expired)
    else:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=1)
        await dB.set_expired_date(user_id, expired)


async def mari_buat_userbot(client, message):
    user_id = message.from_user.id
    if user_id in haji._get_my_id:
        return await client.send_message(
            user_id,
            "<b><blockquote>ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇᴍᴀꜱᴀɴɢ ᴜꜱᴇʀʙᴏᴛ</blockquote></b>",
            reply_markup=ReplyKeyboardRemove(),
        )
    if len(haji._ubot) == MAX_BOT:
        buttons = kb(
            [["💬 Hubungi Admins"]], resize_keyboard=True, one_time_keyboard=True
        )
        return await message.reply(
            f"""
<b>❌ ᴛɪᴅᴀᴋ ᴅᴀᴘᴀᴛ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ !</b>

<b>📚 ᴋᴀʀᴇɴᴀ ᴛᴇʟᴀʜ ᴍᴇɴᴄᴀᴘᴀɪ ʏᴀɴɢ ᴛᴇʟᴀʜ ᴅɪ ᴛᴇɴᴛᴜᴋᴀɴ : {len(haji._ubot)}</b>

<b>👮‍♂ ꜱɪʟᴀᴋᴀɴ ʜᴜʙᴜɴɢɪ ᴀᴅᴍɪɴ . </b>
""",
            reply_markup=buttons,
        )
    if user_id not in AKSES_DEPLOY:
        buttons = ikb([[("📃 Saya Setuju", "go_payment")], [("❌ Tutup", "closed")]])
        text = f"<blockquote>{await Message.policy_message()}</blockquote>"
        return await message.reply(
            text,
            disable_web_page_preview=True,
            reply_markup=buttons,
        )
    else:
        return await create_userbots(client, message)


async def create_userbots(client, message):
    try:
        user_id = message.from_user.id
        anu = ReplyKeyboardMarkup(
            [
                [KeyboardButton(text="Kontak Saya", request_contact=True)],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        anu = ReplyKeyboardMarkup(
            [
                [KeyboardButton(text="Kontak Saya", request_contact=True)],
            ],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        try:
            phone = await client.ask(
                user_id,
                f"<blockquote><b>ꜱɪʟᴀᴋᴀɴ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ <u>Kontak Saya</u> ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍᴋᴀɴ ɴᴏᴍᴏʀ ᴛᴇʟᴇᴘᴏɴ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ.</b></blockquote>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>",
                reply_markup=anu,
            )
            phone_number = phone.contact.phone_number
        except AttributeError:
            try:
                phone = await client.ask(
                    user_id,
                    f"<blockquote><b>ꜱɪʟᴀᴋᴀɴ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ <u>Kontak Saya</u> ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍᴋᴀɴ ɴᴏᴍᴏʀ ᴛᴇʟᴇᴘᴏɴ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ.</b></blockquote>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>",
                    reply_markup=anu,
                )
                phone_number = phone.contact.phone_number
            except Exception:
                return await bot.send_message(
                    user_id,
                    "<blockquote><b>ᴘᴇᴀ, ᴘᴜɴʏᴀ ᴍᴀᴛᴀ ᴅɪᴘᴀᴋᴇ ʙᴜᴀᴛ ʙᴀᴄᴀ!! ᴊᴀɴɢᴀɴ ʙᴏᴋᴇᴘ ᴍᴜʟᴜ.</b></blockquote>",
                    reply_markup=ButtonUtils.start_menu(is_admin=False),
                )
        new_client = hydrogram.Client(
            name=str(user_id),
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True,
        )
        await asyncio.sleep(2)
        get_otp = await client.send_message(
            user_id,
            f"<b><blockquote>ꜱᴇᴅᴀɴɢ ᴍᴇɴɢɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ...</blockquote></b>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>",
            reply_markup=ReplyKeyboardRemove(),
        )
        await new_client.connect()
        try:
            code = await new_client.send_code(phone_number.strip())
        except hydrogram.errors.exceptions.bad_request_400.ApiIdInvalid as AID:
            await get_otp.delete()
            return await client.send_message(user_id, AID)
        except hydrogram.errors.exceptions.bad_request_400.PhoneNumberInvalid as PNI:
            await get_otp.delete()
            return await client.send_message(user_id, PNI)
        except hydrogram.errors.exceptions.bad_request_400.PhoneNumberFlood as PNF:
            await get_otp.delete()
            return await client.send_message(user_id, PNF)
        except hydrogram.errors.exceptions.bad_request_400.PhoneNumberBanned as PNB:
            await get_otp.delete()
            return await client.send_message(user_id, PNB)
        except hydrogram.errors.exceptions.bad_request_400.PhoneNumberUnoccupied as PNU:
            await get_otp.delete()
            return await client.send_message(user_id, PNU)
        except Exception as error:
            await get_otp.delete()
            return await client.send_message(
                user_id,
                f"<b>ERROR:</b> {error}",
                reply_markup=ButtonUtils.start_menu(is_admin=False),
            )
        await get_otp.delete()
        otp = await client.ask(
            user_id,
            f"<b><blockquote>ꜱɪʟᴀᴋᴀɴ ᴘᴇʀɪᴋꜱᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴅᴀʀɪ <a href=tg://openmessage?user_id=777000>ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ</a> ʀᴇꜱᴍɪ. ᴋɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ ᴋᴇ ꜱɪɴɪ ꜱᴇᴛᴇʟᴀʜ ᴍᴇᴍʙᴀᴄᴀ ꜰᴏʀᴍᴀᴛ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ.</b>\n\nᴊɪᴋᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴀᴅᴀʟᴀʜ <code>12345</code> ᴛᴏʟᴏɴɢ <b>[ TAMBAHKAN SPASI ]</b> ᴋɪʀɪᴍᴋᴀɴ ꜱᴇᴘᴇʀᴛɪ ɪɴɪ <code>1 2 3 4 5</code>.</blockquote></b>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>",
        )
        if otp.text in no_trigger:
            return await client.send_message(
                user_id,
                f"<blockquote><b>ᴘʀᴏꜱᴇꜱ ᴅɪ ʙᴀᴛᴀʟᴋᴀɴ.</b></blockquote>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>",
                reply_markup=ButtonUtils.start_menu(is_admin=False),
            )
        otp_code = otp.text
        try:
            await new_client.sign_in(
                phone_number.strip(),
                code.phone_code_hash,
                phone_code=" ".join(str(otp_code)),
            )
        except hydrogram.errors.exceptions.bad_request_400.PhoneCodeInvalid as PCI:
            return await client.send_message(user_id, PCI)
        except hydrogram.errors.exceptions.bad_request_400.PhoneCodeExpired as PCE:
            return await client.send_message(user_id, PCE)
        except hydrogram.errors.exceptions.bad_request_400.BadRequest as error:
            return await client.send_message(
                user_id,
                f"<b>ERROR:</b> {error}",
                reply_markup=ButtonUtils.start_menu(is_admin=False),
            )
        except hydrogram.errors.exceptions.unauthorized_401.SessionPasswordNeeded:
            two_step_code = await client.ask(
                user_id,
                f"<b><blockquote>ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴠᴇʀɪꜰɪᴋᴀꜱɪ ᴅᴜᴀ ʟᴀɴɢᴋᴀʜ. ꜱɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ ᴘᴀꜱꜱᴡᴏʀᴅɴʏᴀ.</blockquote></b>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>",
            )
            if two_step_code.text in no_trigger:
                return await client.send_message(
                    user_id,
                    f"<blockquote><b>ᴘʀᴏꜱᴇꜱ ᴅɪ ʙᴀᴛᴀʟᴋᴀɴ.</b></blockquote>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>",
                    reply_markup=ButtonUtils.start_menu(is_admin=False),
                )
            new_code = two_step_code.text
            try:
                await new_client.check_password(new_code)
                await dB.set_var(user_id, "PASSWORD", new_code)
            except Exception as error:
                return await client.send_message(
                    user_id,
                    f"<b>ERROR:</b> {error}",
                    reply_markup=ButtonUtils.start_menu(is_admin=False),
                )
        session_string = await new_client.export_session_string()
        await new_client.disconnect()
        new_client.storage.session_string = session_string
        new_client.in_memory = False
        bot_msg = await client.send_message(
            user_id,
            f"<b><blockquote>ᴛᴜɴɢɢᴜ ᴘʀᴏꜱᴇꜱ ꜱᴇʟᴀᴍᴀ 𝟷-𝟻 ᴍᴇɴɪᴛ...\nᴋᴀᴍɪ ꜱᴇᴅᴀɴɢ ᴍᴇɴɢʜɪᴅᴜᴘᴋᴀɴ ᴜꜱᴇʀʙᴏᴛ ᴀɴᴅᴀ.</blockquote></b>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>",
            disable_web_page_preview=True,
        )
        await asyncio.sleep(2)
        kn_client = UserBot(
            name=str(user_id),
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
            in_memory=True,
        )
        try:
            await kn_client.start()
        except Exception as e:
            logger.error(f"Error Client: {str(e)}")
        if not await dB.get_expired_date(kn_client.me.id):
            await setExpiredUser(kn_client.me.id)
        await dB.add_ubot(
            user_id=int(kn_client.me.id),
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
        )
        if not user_id == kn_client.me.id:
            haji._ubot.remove(kn_client)
            await dB.remove_ubot(kn_client.me.id)
            await kn_client.log_out()
            return await bot_msg.edit(
                f"<blockquote><b>ɢᴜɴᴀᴋᴀɴ ᴀᴋᴜɴ ᴀɴᴅᴀ ꜱᴇɴᴅɪʀɪ, ʙᴜᴋᴀɴ ᴏʀᴀɴɢ ʟᴀɪɴ!!</b></blockquote>\n<b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>"
            )
        await asyncio.sleep(1)
        for mod in PLUGINS:
            importlib.reload(importlib.import_module(f"plugins.{mod}"))
        seles = await dB.get_list_from_var(BOT_ID, "SELLER")
        if kn_client.me.id not in seles:
            try:
                AKSES_DEPLOY.remove(kn_client.me.id)
            except Exception:
                pass
        try:
            await kn_client.join_chat("noerafuck")
        except Exception:
            pass
        prefix = haji.get_prefix(kn_client.me.id)
        keyb = ButtonUtils.start_menu(is_admin=False)
        exp = await dB.get_expired_date(kn_client.me.id)
        expir = exp.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
        text_done = f"""
    <blockquote><b>🔥 {bot.me.mention} ʙᴇʀʜᴀꜱɪʟ ᴅɪ ᴀᴋᴛɪꜰᴋᴀɴ
    ➡️ ᴀᴋᴜɴ : <a href=tg://openmessage?user_id={kn_client.me.id}>{kn_client.me.first_name} {kn_client.me.last_name or ''}</a>
    ➡️ ɪᴅ : <code>{kn_client.me.id}</code>
    ➡️ ᴘʀᴇꜰɪxᴇꜱ : {' '.join(prefix)}
    ➡️ ᴍᴀꜱᴀ ᴀᴋᴛɪꜰ : {expir}</b></blockquote>
    <b>ᴄʀᴇᴀᴛᴇᴅ ʙʏ {await Message._ads()}</b>"""
        await bot_msg.edit(text_done, disable_web_page_preview=True, reply_markup=keyb)
        return await client.send_message(
            LOG_SELLER,
            f"""
    <b>❏ ɴᴏᴛɪꜰɪᴋᴀꜱɪ ᴜꜱᴇʀʙᴏᴛ ᴀᴋᴛɪꜰ</b>
    <b>├ ᴀᴋᴜɴ :</b> <a href=tg://user?id={kn_client.me.id}>{kn_client.me.first_name} {kn_client.me.last_name or ''}</a> 
    <b>╰ ɪᴅ  :</b> <code>{kn_client.me.id}</code>
    """,
            reply_markup=ikb(
                [
                    [
                        (
                            "Cek Kadaluarsa",
                            f"cek_masa_aktif {kn_client.me.id}",
                            "callback_data",
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    except Exception as er:
        logger.error(f"{str(er)}")


@CMD.CALLBACK("^cek_masa_aktif")
async def _(client, cq):
    user_id = int(cq.data.split()[1])
    try:
        expired = await dB.get_expired_date(user_id)
        habis = expired.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
        return await cq.answer(f"⏳ ᴡᴀᴋᴛᴜ : {habis}", True)
    except Exception:
        return await cq.answer("✅ ꜱᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴀᴋᴛɪꜰ", True)


@CMD.CALLBACK("^closed")
async def _(client, cq):
    await cq.answer()
    return await cq.message.delete()
