import asyncio
import os

from pyrogram.enums import ChatType
from pyrogram.errors import (ChannelPrivate, ChatSendPlainForbidden,
                             ChatWriteForbidden, FloodWait, Forbidden,
                             PeerIdInvalid, SlowmodeWait, UserBannedInChannel)

from config import BLACKLIST_GCAST, DEVS
from Haji import bot
from Haji.database import dB, state
from Haji.helpers import CMD, ButtonUtils, Emoji, Tools, task

__MODULES__ = "Broadcast"
__HELP__ = """
<blockquote>⪼ **--Command help Broadcast--**</blockquote>

<blockquote>**Broadcast ke db**</blockquote>
**ᐉ Keterangan: Kirim pesan broadcast ke grup db**
ᐈ Perintah: `{0}bc db` (teks/reply teks)

<blockquote>**Broadcast ke grup**</blockquote>
**ᐉ Keterangan: Kirim pesan broadcast ke grup**
ᐈ Perintah: `{0}gcast` (teks/reply teks)

<blockquote>**Broadcast ke semua (grup+user)**</blockquote>
**ᐉ Keterangan: Kirim pesan broadcast ke grup dan chat pribadi**
ᐈ Perintah: `{0}bc all` (text/reply teks)

<blockquote>**Broadcast chat pribadi**</blockquote>
**ᐉ Keterangan: Kirim pesan broadcast ke chat pribadi**
ᐈ Perintah: `{0}bc private` (text/reply text)

<blockquote>**Tambahkan blacklist chat**</blockquote>
**ᐉ Keterangan: Tambahkan grup/chat ke blacklist broadcast**
ᐈ Perintah: `{0}addbl` (chatid)

<blockquote>**Hapus blacklist chat**</blockquote>
**ᐉ Keterangan: Hapus grup/chat dari blacklist broadcast**
ᐈ Perintah: `{0}delbl` (chatid)

<blockquote>**List blacklist chat**</blockquote>
**ᐉ Keterangan: Tampilkan semua chat dari blacklist broadcast**
ᐈ Perintah: `{0}listbl`

<blockquote>**Tambahkan broadcast-db**</blockquote>    
**ᐉ Keterangan: Tambahkan grup/chat ke broadcast db**
ᐈ Perintah: `{0}add-bcdb` (chatid)

<blockquote>**Hapus broadcast-db**    </blockquote>
**ᐉ Keterangan: Hapus grup/chat dari broadcast db**
ᐈ Perintah: `{0}del-bcdb` (chatid)

<blockquote>**List broadcast-db**    </blockquote>
**ᐉ Keterangan: Tampilkan grup/chat di broadcast db**
ᐈ Perintah: `{0}list-bcdb`

<blockquote>**Batalkan broadcast**</blockquote>
**ᐉ Keterangan: Batalkan pesan broadcast, berikan taskid**
ᐈ Perintah: `{0}cancel` (taskid)

<b>   {1}</b>
"""


@CMD.UBOT("bc")
@CMD.DEV_CMD("mbc")
@CMD.FAKEDEV("mbc")
async def bc_cmd(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    proses = await message.reply(f"<b>{em.proses}{proses_}</b>")

    command, text = client.extract_type_and_msg(message)

    if command not in ["group", "private", "all", "db"] or not text:
        return await proses.edit(
            f"{em.gagal}<code>{message.text.split()[0]}</code> <b>[group, private, all atau db]</b>"
        )
    task_id = task.start_task()
    prefix = client.get_prefix(client.me.id)
    await proses.edit(
        f"{em.proses}<i>Task broadcast sedang berjalan #<code>{task_id}</code>. "
        f"Ketik <code>{prefix[0]}cancel {task_id}</code> untuk membatalkan broadcast!</i>"
    )
    chats = await client.get_chat_id(command)
    blacklist = await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST")
    done, failed = 0, 0
    error = f"{em.gagal}**Error failed broadcast:**\n"
    try:
        if command == "db":
            return await broadcast_db(
                client,
                message,
                em,
                prefix,
                done,
                failed,
                blacklist,
                task,
                task_id,
                proses,
            )
        for chat_id in chats:
            if not task.is_active(task_id):
                return await proses.edit(f"{em.gagal}Broadcast dibatalkan.")
            if chat_id in blacklist or chat_id in BLACKLIST_GCAST or chat_id in DEVS:
                continue
            try:
                await (
                    text.copy(chat_id)
                    if message.reply_to_message
                    else client.send_message(chat_id, text)
                )
                done += 1
            except ChannelPrivate:
                error += f"ChannelPrivate or channel private {chat_id}\n"
                continue

            except SlowmodeWait:
                error += f"SlowmodeWait or gc di timer {chat_id}\n"
                failed += 1

            except ChatWriteForbidden:
                error += f"ChatWriteForbidden or lu dimute {chat_id}\n"
                failed += 1

            except Forbidden:
                error += f"Forbidden or antispam grup aktif {chat_id}\n"
                failed += 1

            except ChatSendPlainForbidden:
                error += f"ChatSendPlainForbidden or ga bisa kirim teks {chat_id}\n"
                failed += 1

            except UserBannedInChannel:
                error += f"UserBannedInChannel or lu limit {chat_id}\n"
                failed += 1

            except PeerIdInvalid:
                error += f"PeerIdInvalid or lu bukan pengguna grup ini {chat_id}\n"
                continue

            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await (
                        text.copy(chat_id)
                        if message.reply_to_message
                        else client.send_message(chat_id, text)
                    )
                except Exception:
                    failed += 1
                except SlowmodeWait:
                    failed += 1
                    error += f"Grup timer {chat_id}\n"

            except Exception as err:
                failed += 1
                error += f"{str(err)}\n"
    finally:
        task.end_task(task_id)
        await proses.delete()
    if error:
        error_dir = "storage/cache"
        if not os.path.exists(error_dir):
            os.makedirs(error_dir)
        with open(f"{error_dir}/{client.me.id}_errors.txt", "w") as error_file:
            error_file.write(error)
        return await message.reply(
            f"""
<blockquote><b> {em.warn}{sukses_}</b>
<b>{em.sukses}sᴜᴋsᴇs : {done}</b>
<b>{em.gagal}ɢᴀɢᴀʟ : {failed}</b>
<b>{em.msg}ᴛʏᴘᴇ : {command}</b>
<b>{em.robot}ᴛᴀsᴋ ɪᴅ : `{task_id}`</b>
<b>{em.profil}{owner_}</b>

<b>Ketik <code>{prefix[0]}bc-error</code> untuk melihat broadcast yang gagal.</b></blockquote>"""
        )
    else:
        return await message.reply(
            f"""
<blockquote><b> {em.warn}{sukses_}</b>
<b>{em.sukses}sᴜᴋsᴇs : {done}</b>
<b>{em.gagal}ɢᴀɢᴀʟ : {failed}</b>
<b>{em.msg}ᴛʏᴘᴇ : {command}</b>
<b>{em.robot}ᴛᴀsᴋ ɪᴅ : `{task_id}`</b>
<b>{em.profil}{owner_}</b></blockquote>"""
        )


@CMD.UBOT("gcast")
@CMD.DEV_CMD("mgcast")
@CMD.FAKEDEV("mgcast")
async def gcast_cmd(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    proses = await message.reply(f"<b>{em.proses}{proses_}</b>")

    text = client.get_message(message)

    if not text:
        return await proses.edit(
            f"{em.gagal}<code>{message.text.split()[0]}</code> <b>teks atau reply teks</b>"
        )
    task_id = task.start_task()
    prefix = client.get_prefix(client.me.id)
    await proses.edit(
        f"{em.proses}<i>Task {message.command[0]} sedang berjalan #<code>{task_id}</code>. "
        f"Ketik <code>{prefix[0]}cancel {task_id}</code> untuk membatalkan {message.command[0]}!</i>"
    )
    chats = await client.get_chat_id("group")
    blacklist = await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST")
    done, failed = 0, 0
    error = f"{em.gagal}**Error failed broadcast:**\n"
    try:

        for chat_id in chats:
            if not task.is_active(task_id):
                return await proses.edit(f"{em.gagal}{message.command[0]} dibatalkan.")
            if chat_id in blacklist or chat_id in BLACKLIST_GCAST or chat_id in DEVS:
                continue
            try:
                await (
                    text.copy(chat_id)
                    if message.reply_to_message
                    else client.send_message(chat_id, text)
                )
                done += 1
            except ChannelPrivate:
                error += f"ChannelPrivate or channel private {chat_id}\n"
                continue

            except SlowmodeWait:
                error += f"SlowmodeWait or gc di timer {chat_id}\n"
                failed += 1

            except ChatWriteForbidden:
                error += f"ChatWriteForbidden or lu dimute {chat_id}\n"
                failed += 1

            except Forbidden:
                error += f"Forbidden or antispam grup aktif {chat_id}\n"
                failed += 1

            except ChatSendPlainForbidden:
                error += f"ChatSendPlainForbidden or ga bisa kirim teks {chat_id}\n"
                failed += 1

            except UserBannedInChannel:
                error += f"UserBannedInChannel or lu limit {chat_id}\n"
                failed += 1

            except PeerIdInvalid:
                error += f"PeerIdInvalid or lu bukan pengguna grup ini {chat_id}\n"
                continue

            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await (
                        text.copy(chat_id)
                        if message.reply_to_message
                        else client.send_message(chat_id, text)
                    )
                except Exception:
                    failed += 1
                except SlowmodeWait:
                    failed += 1
                    error += f"Grup timer {chat_id}\n"

            except Exception as err:
                failed += 1
                error += f"{str(err)}\n"
    finally:
        task.end_task(task_id)
        await proses.delete()
    if error:
        error_dir = "storage/cache"
        if not os.path.exists(error_dir):
            os.makedirs(error_dir)
        with open(f"{error_dir}/{client.me.id}_errors.txt", "w") as error_file:
            error_file.write(error)
        return await message.reply(
            f"""
<blockquote><b> {em.warn}{sukses_}</b>
<b>{em.sukses}sᴜᴋsᴇs : {done}</b>
<b>{em.gagal}ɢᴀɢᴀʟ : {failed}</b>
<b>{em.msg}ᴛʏᴘᴇ : {message.command[0]}</b>
<b>{em.robot}ᴛᴀsᴋ ɪᴅ : `{task_id}`</b>
<b>{em.profil}{owner_}</b>

<b>Ketik <code>{prefix[0]}bc-error</code> untuk melihat broadcast yang gagal.</b></blockquote>"""
        )
    else:
        return await message.reply(
            f"""
<blockquote><b> {em.warn}{sukses_}</b>
<b>{em.sukses}sᴜᴋsᴇs : {done}</b>
<b>{em.gagal}ɢᴀɢᴀʟ : {failed}</b>
<b>{em.msg}ᴛʏᴘᴇ : {message.command[0]}</b>
<b>{em.robot}ᴛᴀsᴋ ɪᴅ : `{task_id}`</b>
<b>{em.profil}{owner_}</b></blockquote>"""
        )


@CMD.UBOT("ucast")
@CMD.DEV_CMD("mucast")
@CMD.FAKEDEV("mucast")
async def broadcast(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    proses = await message.reply(f"<b>{em.proses}{proses_}</b>")

    text = client.get_message(message)

    if not text:
        return await proses.edit(
            f"{em.gagal}<code>{message.text.split()[0]}</code> <b>teks atau reply teks</b>"
        )
    task_id = task.start_task()
    prefix = client.get_prefix(client.me.id)
    await proses.edit(
        f"{em.proses}<i>Task {message.command[0]} sedang berjalan #<code>{task_id}</code>. "
        f"Ketik <code>{prefix[0]}cancel {task_id}</code> untuk membatalkan {message.command[0]}!</i>"
    )
    chats = await client.get_chat_id("private")
    blacklist = await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST")
    done, failed = 0, 0
    error = f"{em.gagal}**Error failed broadcast:**\n"
    try:
        for chat_id in chats:
            if not task.is_active(task_id):
                return await proses.edit(f"{em.gagal}{message.command[0]} dibatalkan.")
            if chat_id in blacklist or chat_id in BLACKLIST_GCAST or chat_id in DEVS:
                continue
            try:
                await (
                    text.copy(chat_id)
                    if message.reply_to_message
                    else client.send_message(chat_id, text)
                )
                done += 1
            except ChannelPrivate:
                error += f"ChannelPrivate or channel private {chat_id}\n"
                continue

            except SlowmodeWait:
                error += f"SlowmodeWait or gc di timer {chat_id}\n"
                failed += 1

            except ChatWriteForbidden:
                error += f"ChatWriteForbidden or lu dimute {chat_id}\n"
                failed += 1

            except Forbidden:
                error += f"Forbidden or antispam grup aktif {chat_id}\n"
                failed += 1

            except ChatSendPlainForbidden:
                error += f"ChatSendPlainForbidden or ga bisa kirim teks {chat_id}\n"
                failed += 1

            except UserBannedInChannel:
                error += f"UserBannedInChannel or lu limit {chat_id}\n"
                failed += 1

            except PeerIdInvalid:
                error += f"PeerIdInvalid or lu bukan pengguna grup ini {chat_id}\n"
                continue

            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await (
                        text.copy(chat_id)
                        if message.reply_to_message
                        else client.send_message(chat_id, text)
                    )
                except Exception:
                    failed += 1
                except SlowmodeWait:
                    failed += 1
                    error += f"Grup timer {chat_id}\n"

            except Exception as err:
                failed += 1
                error += f"{str(err)}\n"
    finally:
        task.end_task(task_id)
        await proses.delete()
    if error:
        error_dir = "storage/cache"
        if not os.path.exists(error_dir):
            os.makedirs(error_dir)
        with open(f"{error_dir}/{client.me.id}_errors.txt", "w") as error_file:
            error_file.write(error)
        return await message.reply(
            f"""
<blockquote><b> {em.warn}{sukses_}</b>
<b>{em.sukses}sᴜᴋsᴇs : {done}</b>
<b>{em.gagal}ɢᴀɢᴀʟ : {failed}</b>
<b>{em.msg}ᴛʏᴘᴇ : {message.command[0]}</b>
<b>{em.robot}ᴛᴀsᴋ ɪᴅ : `{task_id}`</b>
<b>{em.profil}{owner_}</b>

<b>Ketik <code>{prefix[0]}bc-error</code> untuk melihat broadcast yang gagal.</b></blockquote>"""
        )
    else:
        return await message.reply(
            f"""
<blockquote><b> {em.warn}{sukses_}</b>
<b>{em.sukses}sᴜᴋsᴇs : {done}</b>
<b>{em.gagal}ɢᴀɢᴀʟ : {failed}</b>
<b>{em.msg}ᴛʏᴘᴇ : {message.command[0]}</b>
<b>{em.robot}ᴛᴀsᴋ ɪᴅ : `{task_id}`</b>
<b>{em.profil}{owner_}</b></blockquote>"""
        )


@CMD.UBOT("bc-error")
@CMD.DEV_CMD("mbc-error")
@CMD.FAKEDEV("mbc-error")
async def _(client, message):
    oy = await message.reply("<b>Membaca error logs...</b>")
    try:
        error_file = f"storage/cache/{client.me.id}_errors.txt"
        try:
            with open(error_file, "r") as f:
                content = f.read().strip()

            if not content:
                await oy.edit("<b>No errors found in log file.</b>")
                return
            if len(content) > 4000:
                content = content[-4000:]
                content = f"... (truncated)\n\n{content}"

            message_text = f"<b>📋 Error Logs:</b>\n\n<code>{content}</code>"

            return await oy.edit(message_text)

        except FileNotFoundError:
            return await oy.edit("<b>Error log file not found!</b>")

    except Exception:
        try:
            error_file = f"storage/cache/{client.me.id}_error.txt"
            with open(error_file, "r") as f:
                content = f.read().strip()

            if not content:
                await oy.edit("<b>No errors found in fallback log file.</b>")
                return

            if len(content) > 4000:
                content = content[-4000:]
                content = f"... (truncated)\n\n{content}"

            message_text = (
                f"<b>📋 Error Logs (from fallback):</b>\n\n<code>{content}</code>"
            )

            await client.send_message("me", message_text)
            return await oy.edit("<b>Cek saved message</b>")

        except Exception as e:
            return await oy.edit(f"<b>Failed to read error logs: {str(e)}</b>")


async def broadcast_db(
    client, message, em, prefix, done, failed, blacklist, task, task_id, proses
):
    command, text = client.extract_type_and_msg(message)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    chatsdb = await dB.get_list_from_var(client.me.id, "BROADCASTDB")
    if not chatsdb:
        return await proses.edit(
            f"{em.gagal}**Anda tidak punya broadcastdb !! Silakan ketik `{prefix[0]} add-bcdb 'di grup atau user.**"
        )
    try:
        for chat_id in chatsdb:
            if not task.is_active(task_id):
                return await proses.edit(f"{em.gagal}**Broadcast dibatalkan.**")
            if chat_id in blacklist or chat_id in BLACKLIST_GCAST or chat_id in DEVS:
                continue
            try:
                await (
                    text.copy(chat_id)
                    if message.reply_to_message
                    else client.send_message(chat_id, text)
                )
                done += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await (
                    text.copy(chat_id)
                    if message.reply_to_message
                    else client.send_message(chat_id, text)
                )
            except Exception:
                failed += 1
                continue
    finally:
        task.end_task(task_id)
        await proses.delete()

    return await message.reply(
        f"""
<blockquote><b> {em.warn}{sukses_}</b>
<b>{em.sukses}sᴜᴋsᴇs : {done}</b>
<b>{em.gagal}ɢᴀɢᴀʟ : {failed}</b>
<b>{em.msg}ᴛʏᴘᴇ : {command}</b>
<b>{em.profil}ᴛᴀsᴋ ɪᴅ : {task_id}</b></blockquote>

<blockquote><b>{em.profil}{owner_}</b></blockquote>"""
    )


@CMD.UBOT("cancel")
@CMD.DEV_CMD("mcancel")
@CMD.FAKEDEV("mcancel")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    prefix = client.get_prefix(client.me.id)
    if len(message.command) != 2:
        return await message.reply(
            f"{em.gagal}**Harap berikan Task ID untuk membatalkan.\nKetik `{prefix[0]}task` untuk melihat list task yang sedang berjalan.**"
        )

    task_id = message.command[1]

    if not task.is_active(task_id):
        return await message.reply(
            f"{em.gagal}**No active task found with ID: #`{task_id}`**"
        )
    task.end_task(task_id)
    return await message.reply(f"{em.sukses}**Ended task: #`{task_id}`**")


@CMD.UBOT("addbl")
@CMD.DEV_CMD("maddbl")
@CMD.FAKEDEV("maddbl")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    pp = await message.reply(f"{em.proses}**{proses_}**")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    blacklist = await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST")
    try:
        chat_id = int(chat_id)
    except ValueError:
        return await pp.edit(f"{em.gagal}**chat_id must be in the form of numbers!**")
    chat_type = message.chat.type
    if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        name = message.chat.title
    elif chat_type == ChatType.PRIVATE:
        name = f"{message.chat.first_name} {message.chat.last_name or ''}"
    if chat_id in blacklist:
        return await pp.edit(f"{em.gagal}**`{name}` sudah ada di dalam blacklist-Gcast!**")
    await dB.add_to_var(client.me.id, "BLACKLIST_GCAST", chat_id)
    return await pp.edit(
        f"{em.sukses}<b>Berhasil menambahkan `{name}` ke dalam blacklists</b>"
    )


@CMD.UBOT("delbl")
@CMD.DEV_CMD("mdelbl")
@CMD.FAKEDEV("mdelbl")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    proses_ = await em.get_costum_text()
    pp = await message.reply(f"{em.proses}**{proses_[4]}**")
    blacklist = await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST")
    chat_type = message.chat.type
    if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        name = message.chat.title
    elif chat_type == ChatType.PRIVATE:
        name = f"{message.chat.first_name} {message.chat.last_name or ''}"
    try:
        if len(message.command) < 2:
            chat_id = message.chat.id

            if chat_id not in blacklist:
                return await pp.edit(f"{em.gagal}**`{name}` tidak ada di blacklists!**")
            await dB.remove_from_var(client.me.id, "BLACKLIST_GCAST", chat_id)
            return await pp.edit(
                f"{em.sukses}**Berhasil menghapus `{name}` `dari daftar blacklist-gcast!**"
            )
        else:
            if message.command[1] == "all":
                for A in blacklist:
                    await dB.remove_from_var(client.me.id, "BLACKLIST_GCAST", A)
                return await pp.edit(
                    f"{em.sukses}<b>Berhasil menghapus semua daftar blacklist-gcast!</b>"
                )
            else:
                chat_id = message.command[1]
                try:
                    chat_id = int(chat_id)
                except ValueError:
                    return await pp.edit(
                        f"{em.gagal}**Please give a valid chat_id.Error `{chat_id}`!**"
                    )

                if chat_id not in blacklist:
                    return await pp.edit(
                        f"{em.gagal}`{name}` **Tidak ada di Blacklist-Gcast!**"
                    )
                await dB.remove_from_var(client.me.id, "BLACKLIST_GCAST", chat_id)
                return await pp.edit(
                    f"{em.sukses}**Berhasil menghapus `{name}` dari daftar blacklist-gcast!**"
                )
    except Exception as er:
        return await pp.edit(f"{em.gagal}ERRORR: `{str(er)}`!!")


@CMD.UBOT("listbl")
@CMD.DEV_CMD("mlistbl")
@CMD.FAKEDEV("mlistbl")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    blacklist = await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST")
    pp = await message.reply(f"{em.proses}**{proses_}**")
    if blacklist == []:
        return await pp.edit(f"{em.gagal}**Blacklist-Gcast Data Anda masih kosong!**")
    msg = f"{em.msg}Total Blacklist-Gcast: {len(blacklist)}\n\n"
    for num, x in enumerate(blacklist, 1):
        try:
            chat = await client.get_chat(x)
            name = chat.title or f"{chat.first_name} {chat.last_name or ''}"
            msg += f"{num}. {name}|`{chat.id}`\n"
        except Exception:
            msg += f"{num}. `{x}`\n"
    if len(msg) > 4096:
        link = await Tools.paste(msg)
        await pp.edit(f"{em.proses}**Pesan Anda terlalu panjang, mengupload ke pastebin...**")
        await asyncio.sleep(1)
        return await message.reply_text(
            f"{em.sukses}**<a href='{link}'>Klik Disini </a> untuk melihat daftar blacklist-gcast Anda.**",
            disable_web_page_preview=True,
        )
    else:
        await pp.delete()
        return await message.reply_text(msg)


@CMD.UBOT("add-bcdb")
@CMD.DEV_CMD("madd-bcdb")
@CMD.FAKEDEV("madd-bcdb")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    pp = await message.reply(f"{em.proses}**{proses_}**")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    blacklist = await dB.get_list_from_var(client.me.id, "BROADCASTDB")
    chat_type = message.chat.type
    if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        name = message.chat.title
    elif chat_type == ChatType.PRIVATE:
        name = f"{message.chat.first_name}{message.chat.last_name or ''}"
    try:
        chat_id = int(chat_id)
    except ValueError:
        return await pp.edit(f"{em.gagal}**Chat_id must be a number!**")

    if chat_id in blacklist:
        return await pp.edit(f"{em.gagal}`{name}` **Already on Broadcast-DB!**")
    await dB.add_to_var(client.me.id, "BROADCASTDB", chat_id)
    return await pp.edit(
        f"{em.sukses}**Successfully added `{name}` into broadcast-db**"
    )


@CMD.UBOT("del-bcdb")
@CMD.DEV_CMD("mdel-bcdb")
@CMD.FAKEDEV("mdel-bcdb")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    pp = await message.reply(f"{em.proses}**{proses_}**")
    blacklist = await dB.get_list_from_var(client.me.id, "BROADCASTDB")
    chat_type = message.chat.type
    if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        name = message.chat.title
    elif chat_type == ChatType.PRIVATE:
        name = f"{message.chat.first_name}{message.chat.last_name or ''}"
    try:
        if len(message.command) < 2:
            chat_id = message.chat.id

            if chat_id not in blacklist:
                return await pp.edit(f"{em.gagal}`{name}` **is not in broadcast-db!**")
            await dB.remove_from_var(client.me.id, "BROADCASTDB", chat_id)
            return await pp.edit(
                f"{em.sukses}**Successfully delete `{name} 'from the broadcast list-db!**"
            )
        else:
            if message.command[1] == "all":
                for A in blacklist:
                    await dB.remove_from_var(client.me.id, "BROADCASTDB", A)
                return await pp.edit(
                    f"{em.sukses}Successfully delete all broadcast lists-DB!"
                )
            else:
                chat_id = message.command[1]
                try:
                    chat_id = int(chat_id)
                except ValueError:
                    return await pp.edit(
                        f"{em.gagal}**Please give a valid chat_id.Error `{chat_id}`!**"
                    )

                if chat_id not in blacklist:
                    return await pp.edit(f"{em.gagal}`{name}` **not in broadcast-db!**")
                await dB.remove_from_var(client.me.id, "BROADCASTDB", chat_id)
                return await pp.edit(
                    f"{em.sukses}**Successfully delete `{name}` from the broadcast list-db!**"
                )
    except Exception as er:
        return await pp.edit(f"{em.gagal}ERRORR: `{str(er)}`!!")


@CMD.UBOT("list-bcdb")
@CMD.DEV_CMD("mlist-bcdb")
@CMD.FAKEDEV("mlist-bcdb")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    blacklist = await dB.get_list_from_var(client.me.id, "BROADCASTDB")
    pp = await message.reply(f"{em.proses}**{proses_}**")
    if blacklist == []:
        return await pp.edit(f"{em.gagal}**Your broadcast-DB data is still empty!**")
    msg = f"{em.msg}**Total Broadcast-DB: {len(blacklist)}**\n\n"
    for num, x in enumerate(blacklist, 1):
        try:
            chat = await client.get_chat(x)
            name = chat.title or f"{chat.first_name} {chat.last_name or ''}"
            msg += f"**{num}. {name}|`{chat.id}`**\n"
        except Exception:
            msg += f"**{num}. `{x}`**\n"
    if len(msg) > 4096:
        link = await Tools.paste(msg)
        await pp.edit(f"{em.proses}**Message is too long, uploading to pastebin ...**")
        await asyncio.sleep(1)
        return await message.reply_text(
            f"{em.sukses}**<a href='{link}'>Click here </a> to see your broadcast list.**",
            disable_web_page_preview=True,
        )
    else:
        await pp.delete()
        return await message.reply_text(msg)


@CMD.UBOT("send")
@CMD.DEV_CMD("msend")
@CMD.FAKEDEV("msend")
async def _(client, message):
    em = Emoji(client)
    await em.get()
    if message.reply_to_message:
        chat_id = (
            message.chat.id if len(message.command) < 2 else message.text.split()[1]
        )
        try:
            if message.reply_to_message.reply_markup:
                state.set(client.me.id, "inline_send", id(message))
                query = f"inline_send {client.me.id}"
                inline = await ButtonUtils.send_inline_bot_result(
                    message,
                    chat_id,
                    bot.me.username,
                    query,
                )
                if inline:
                    return await message.delete()
        except Exception as er:
            return await message.reply(f"{em.gagal}ERROR: {str(er)}")
        else:
            try:
                await message.reply_to_message.copy(chat_id)
                await message.delete()
                return
            except Exception as er:
                return await message.reply(f"{em.gagal}ERROR: {str(er)}")
    else:
        if len(message.command) < 3:
            return
        chat_id, chat_text = message.text.split(None, 2)[1:]
        try:
            if "/" in chat_id:
                to_chat, msg_id = chat_id.split("/")
                await client.send_message(
                    to_chat, chat_text, reply_to_message_id=int(msg_id)
                )
                await message.delete()
                return
            else:
                await client.send_message(chat_id, chat_text)
                await message.delete()
                return
        except Exception as er:
            return await message.reply(f"{em.gagal}ERROR: {str(er)}")
