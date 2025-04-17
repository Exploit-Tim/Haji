import asyncio

from pyrogram.errors import FloodWait, SlowmodeWait

from config import BLACKLIST_GCAST
from Haji.database import dB
from Haji.helpers import CMD, Emoji, task

__MODULES__ = "Spam"
__HELP__ = """
<blockquote>⪼ **--Command help Spam--**</blockquote>

<blockquote>**Spam message with delay**</blockquote>
**ᐉ Keterangan: Kirim spam dengan delay**
ᐈ Perintah: `{0}dspam` (reply message) (jumlah) (delay)
        
<blockquote>**Spam message without delay**</blockquote>
**ᐉ Keterangan: Kirim spam tanpa delay**
ᐈ Perintah: `{0}spam` (reply message) (jumlah)

<blockquote>**Spam broadcast** </blockquote>
**ᐉ Keterangan: Kirim siaran spam dengan hitungan**
ᐈ Perintah: `{0}spamg` (count) (text/reply message)

<blockquote>**Stop spam** </blockquote>
**ᐉ Keterangan: Batalkan task spam**
ᐈ Perintah: `{0}cancel` (taskid)

<b>   {1}</b>
"""


@CMD.UBOT("spam|dspam")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    command = message.command[0]
    reply = message.reply_to_message
    proses = await message.reply(
        f"{emo.proses}<b>{'Delay ' if command == 'dspam' else ''}Spam process is running ..</b>"
    )
    task_id = task.start_task()
    prefix = client.get_prefix(client.me.id)
    try:
        if len(message.command) < 2:
            return await proses.edit(
                f"{emo.gagal}<b>Usage `{prefix[0]}{command}`[amount] {'[delay] ' if command == 'dspam' else ''}[text/reply text].</b>"
            )
        jumlah = int(message.command[1])
        count_delay = (
            int(message.command[2])
            if command == "dspam" and len(message.command) > 2
            else 0
        )
    except Exception as error:
        return await proses.edit(f"{emo.gagal}<b>Error:</b>\n<code>{str(error)}</code>")
    await proses.edit(
        f"{emo.proses}<i>{'Delay ' if command == 'dspam' else ''}Spam task running #<code>{task_id}</code>. "
        f"Type <code>{prefix[0]}cancel {task_id}</code> to cancel {'delay ' if command == 'dspam' else ''}spam!</i>"
    )
    if reply:
        text = reply.text
    else:
        if len(message.command) < (3 if command == "dspam" else 2):
            return await proses.edit(
                f"{emo.gagal}<b>Usage `{prefix[0]}{command}`[amount] {'[delay] ' if command == 'dspam' else ''}[text/reply text].</b>"
            )
        text = message.text.split(None, 3 if command == "dspam" else 2)[-1]
    for i in range(jumlah):
        if not task.is_active(task_id):
            return await proses.edit(
                f"{emo.gagal}{'Delay ' if command == 'dspam' else ''}Spam cancelled."
            )
        else:
            try:
                await (reply.copy(message.chat.id) if reply else message.reply(text))
                await asyncio.sleep(count_delay if command == "dspam" else 0.1)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await (reply.copy(message.chat.id) if reply else message.reply(text))
            except SlowmodeWait as e:
                await asyncio.sleep(e.value)
                await (reply.copy(message.chat.id) if reply else message.reply(text))

            except Exception as error:
                return await proses.edit(str(error))
    task.end_task(task_id)
    await proses.delete()
    return await message.delete()


@CMD.UBOT("spamg")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    proses = await message.reply(f"{emo.proses}<b>Spam broadcast process ..</b>")
    if len(message.command) < 2 or not message.command[1].isdigit():
        return await proses.edit(
            f"{emo.gagal}<b>Please use command: `{message.text.split()[0]} 5` (text or reply text)</b>"
        )

    jumlah = int(message.command[1])
    send = client.get_message(message)
    if not send:
        return await proses.edit(
            f"{emo.gagal}<b>Provide me with text or reply to a message ..</b>"
        )
    task_id = task.start_task()
    prefix = client.get_prefix(client.me.id)
    await proses.edit(
        f"{emo.proses}<i>Spam broadcast task running #<code>{task_id}</code>. "
        f"Type <code>{prefix[0]}cancel {task_id}</code> to cancel Spam broadcast!</i>"
    )
    chats = await client.get_chat_id("group")
    blacklist = await dB.get_list_from_var(client.me.id, "BLACKLIST_GCAST")
    done = 0
    failed = 0
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_GCAST:
            continue
        if not task.is_active(task_id):
            return await proses.edit(f"{emo.gagal}Spam broadcast cancelled.")
        else:
            try:
                for i in range(jumlah):
                    (
                        await send.copy(chat_id)
                        if message.reply_to_message
                        else await client.send_message(chat_id, send)
                    )
                done += 1
            except FloodWait as e:
                wait = int(e.value)
                if wait > 200:
                    failed += 1
                    continue
                await asyncio.sleep(wait)
                try:
                    for i in range(jumlah):
                        (
                            await send.copy(chat_id)
                            if message.reply_to_message
                            else await client.send_message(chat_id, send)
                        )
                    done += 1
                except Exception:
                    failed += 1
                    continue
            except Exception:
                failed += 1
                continue
    task.end_task(task_id)

    await message.reply(
        f"""
{emo.profil}<b>Spam Broadcast Report:
{emo.sukses} Success: <code>{done}</code> Groups
{emo.gagal} Failed: <code>{failed}</code> Groups
</b>"""
    )
    return await proses.delete()
