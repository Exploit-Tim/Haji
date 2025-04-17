import asyncio
import random

from pyrogram.errors import ChatIdInvalid
from pyrogram.raw import functions
from pyrogram.raw.functions.phone import DiscardGroupCall
from pyrogram.raw.types import InputGroupCall
from pytgcalls.exceptions import (AlreadyJoinedError, NoActiveGroupCall,
                                  NotInCallError)

from Haji.helpers import CMD, Emoji

__MODULES__ = "Vctools"
__HELP__ = """
<blockquote>⪼ **--Command help VcTools--**</blockquote>

<blockquote>**Start end vc group**</blockquote>
**ᐉ Keterangan: Mulai obrolan suara grup/channel**
ᐈ Perintah: `{0}startvc` 
**ᐉ Keterangan: Mengakhiri obrolan suara grup/channel**
ᐈ Perintah: `{0}stopvc`
        
<blockquote>**Join leave vc group**</blockquote>
**ᐉ Keterangan: Join OS grup/channel**
ᐈ Perintah: `{0}jvc` (chatid)
**ᐉ Keterangan: Turun OS grup/channel**
ᐈ Perintah: `{0}lvc` (chatid)

<blockquote>**Get listeners vc group**</blockquote>
**ᐉ Keterangan: Periksa listeners dari obrolan suara**
ᐈ Perintah: `{0}listeners`
        
<blockquote>**Change vc title**</blockquote>
**ᐉ Keterangan: Edit judul obrolan suara grup**
ᐈ Perintah: `{0}vctitle` (title)

<b>   {1}</b>
"""


@CMD.UBOT("startvc")
@CMD.DEV_CMD("mstartvc")
@CMD.FAKEDEV("mstartvc")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    args = message.command[1:]

    chat_id = None
    title = None

    if len(args) == 0:
        chat_id = message.chat.id
    elif len(args) == 1:
        if args[0].startswith("@"):
            try:
                chat_id = (await client.get_chat(args[0])).id
            except Exception:
                return await message.reply(f"{emo.gagal}<b>Cannot find the group.</b>")
        elif args[0].startswith("-100"):
            chat_id = int(args[0])
        else:
            chat_id = message.chat.id
            title = args[0]
    elif len(args) == 2:
        if args[0].startswith("@"):
            chat_id = (await client.get_chat(args[0])).id
            title = args[1]
        elif args[0].startswith("-100"):
            chat_id = int(args[0])
            title = args[1]
        else:
            try:
                chat_id = int(args[0])
            except ValueError:
                return await message.reply(
                    f"{emo.gagal}<b>The first argument is not valid. Please use a valid group ID or username.</b>"
                )
            title = args[1]
    elif (
        len(args) == 2
        and not args[0].startswith("@")
        and not args[0].startswith("-100")
    ):
        chat_id = message.chat.id
        title = args[0]

    if chat_id is None:
        chat_id = message.chat.id

    pros = await message.reply(f"{emo.proses}<b>Starting Voice Chat ..</b>")

    try:
        chat = await client.get_chat(chat_id)
        chat_title = chat.title
        if title is None:
            title = chat.title
    except Exception:
        chat_title = chat_id
        if title is None:
            title = chat_id

    group_call = await client.get_call(client, chat_id)
    if group_call:
        title = group_call.title if group_call.title else chat_title
        return await pros.edit(
            f"{emo.gagal}<b>Voice chat already exists:\n{emo.profil}Group: <code>{chat_title}</code>\n{emo.warn}Title: <code>{title}</code></b>"
        )

    txt = f"<b>{emo.sukses}Starting Voice Chat:\n{emo.profil}Group: <code>{chat_title}</code>\n{emo.warn}Title: <code>{title}</code></b>"
    try:
        await client.invoke(
            functions.phone.CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=random.randint(10000, 999999999),
                title=title,
            )
        )
        return await pros.edit(f"{txt}")
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            return await pros.edit(f"{emo.gagal}<b>You are not an admin!</b>")
        return await pros.edit(f"{emo.gagal}<b>Error:</b>\n\n<code>{str(e)}</code>")


@CMD.UBOT("stopvc")
@CMD.DEV_CMD("mstopvc")
@CMD.FAKEDEV("mstopvc")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    args = message.command[1:]

    chat_id = None

    if len(args) == 0:
        chat_id = message.chat.id
    elif len(args) == 1:
        if args[0].startswith("@"):
            try:
                chat_id = (await client.get_chat(args[0])).id
            except Exception:
                return await message.reply(f"{emo.gagal}<b>Cannot find the chat.</b>")
        elif args[0].startswith("-100"):
            chat_id = int(args[0])
        else:
            chat_id = message.chat.id
    elif (
        len(args) == 1
        and not args[0].startswith("@")
        and not args[0].startswith("-100")
    ):
        chat_id = message.chat.id

    if chat_id is None:
        chat_id = message.chat.id

    pros = await message.reply(f"{emo.proses}<b>Stopping Voice Chat ..</b>")

    try:
        chat = await client.get_chat(chat_id)
        title = chat.title
    except Exception:
        title = chat_id

    group_call = await client.get_call(client, chat_id)

    if not group_call:
        return await pros.edit(
            f"{emo.gagal}<b>No Voice Chat:\n{emo.profil}Group: <code>{title}</code></b>"
        )

    try:
        call = InputGroupCall(id=group_call.id, access_hash=group_call.access_hash)
        await client.invoke(DiscardGroupCall(call=call))
        return await pros.edit(
            f"{emo.sukses}<b>Stopped Voice Chat:\n{emo.profil}Group: <code>{title}</code>.</b>"
        )
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            return await pros.edit(f"{emo.gagal}<b>You are not an admin!</b>")
        return await pros.edit(
            f"{emo.gagal}<b>Failed to stop Voice Chat:\n{emo.profil}Group: <code>{title}</code>\n\n<code>{str(e)}</code></b>"
        )


@CMD.UBOT("joinvc|jvc")
@CMD.DEV_CMD("mjoinvc|mjvc")
@CMD.FAKEDEV("mjoinvc|mjvc")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    args = message.chat.id if len(message.command) < 2 else message.text.split()[1]
    pros = await message.reply(f"{emo.proses}<b>Joining Voice Chat ..</b>")

    try:
        chat = await client.get_chat(args)
    except ChatIdInvalid:
        return await pros.edit(
            f"{emo.gagal}<b>Cannot find the Group, please give username or chatid</b>"
        )
    title = chat.title
    chat_id = chat.id

    group_call = await client.get_call(client, chat_id)
    if not group_call:
        await message.reply(
            f"{emo.gagal}<b>Cannot find Voice Chat in <code>{title}</code></b>"
        )
        return await pros.delete()
    try:
        await client.group_call.play(chat.id)
        await asyncio.sleep(1)
        await client.group_call.mute_stream(chat.id)
        await message.reply(
            f"{emo.sukses}<b>Successfully joined Voice Chat:\n{emo.profil}Group: <code>{title}</code>.</b>"
        )
    except NoActiveGroupCall:
        await message.reply(
            f"{emo.gagal}<b>No active Voice Chat in <code>{title}</code></b>"
        )
    except AlreadyJoinedError:
        await message.reply(
            f"{emo.gagal}<b>Your account is already in the Voice Chat.</b>"
        )
    except Exception as e:
        await message.reply(
            f"{emo.gagal}<b>Failed to join Voice Chat:\n{emo.profil}Group: <code>{title}</code>\nError:\n<code>{e}</b>"
        )

    return await pros.delete()


@CMD.UBOT("leavevc|lvc")
@CMD.DEV_CMD("mleavevc|mlvc")
@CMD.FAKEDEV("mleavevc|mlvc")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    args = message.chat.id if len(message.command) < 2 else message.text.split()[1]
    pros = await message.reply(f"{emo.proses}<b>Joining Voice Chat ..</b>")

    try:
        chat = await client.get_chat(args)
    except ChatIdInvalid:
        return await pros.edit(
            f"{emo.gagal}<b>Cannot find the Group, please give username or chatid</b>"
        )
    title = chat.title
    chat_id = chat.id

    try:
        await client.group_call.leave_call(chat_id)
        return await pros.edit(
            f"{emo.sukses}<b>Successfully left Voice Chat:\n{emo.profil}Group: <code>{title}</code></b>"
        )
    except NotInCallError:
        return await pros.edit(
            f"{emo.gagal}<b>Your account is not in the Voice Chat <code>{title}</code></b>"
        )
    except Exception as e:
        return await pros.edit(
            f"{emo.gagal}<b>Failed to leave Voice Chat:\n{emo.profil}Group: <code>{title}</code>\n{emo.block}Error: <code>{e}</code>"
        )


@CMD.UBOT("listeners")
@CMD.DEV_CMD("mlisteners")
@CMD.FAKEDEV("mlisteners")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    pros = await message.reply(
        f"{emo.proses}<b>Fetching Voice Chat listeners data ..</b>"
    )

    chat = message.command[1] if len(message.command) > 1 else message.chat.id
    try:
        if isinstance(chat, int):
            chat_id = chat
        else:
            chat_info = await client.get_chat(chat)
            chat_id = chat_info.id
        try:
            info = await client.get_chat(chat_id)
            title = info.title if info.title else f"{chat_id}"
        except Exception:
            title = f"{chat_id}"
        group_call = await client.get_call(client, info.id)
        if not group_call:
            return await pros.edit(
                f"{emo.gagal}<b>Cannot find Voice Chat in <code>{title}</code></b>"
            )
        try:
            call_title = group_call.title
            client.group_call.cache_peer(chat_id)
            participants = await client.group_call.get_participants(chat_id)
            mentions = []
            for participant in participants:
                user_id = participant.user_id
                try:
                    user = await client.get_users(user_id)
                    mention = user.mention
                    volume = participant.volume
                    status = "🔇 Muted" if participant.muted else "🔊 Speaking"
                    mentions.append(
                        f"<b>{mention} | status: <code>{status}</code> | volume: <code>{volume}</code></b>"
                    )
                except Exception:
                    mentions.append(f"{user_id} status Unknown")

            total_participants = len(participants)
            if total_participants == 0:
                return await pros.edit(
                    f"{emo.gagal}<b>No one is in the Voice Chat.</b>"
                )

            mentions_text = "\n".join(
                [
                    (f"┣ {mention}" if i < total_participants - 1 else f"┖ {mention}")
                    for i, mention in enumerate(mentions)
                ]
            )

            text = f"""
{emo.sukses}<b>Voice Chat Listeners:
{emo.owner}Chat: <code>{title}</code>.
{emo.profil}Total: <code>{total_participants}</code> people.
{emo.warn}Title: <code>{call_title}</code>

❒ Participants:
{mentions_text}</b>
"""
            return await pros.edit(f"{text}")

        except Exception as e:

            await pros.edit(f"{emo.gagal}<b>Error:</b>\n<code>{e}</code>")
    except Exception as e:
        await pros.edit(f"{emo.gagal}<b>Error:</b>\n<code>{e}</code>")


@CMD.UBOT("vctitle")
@CMD.DEV_CMD("mvctitle")
@CMD.FAKEDEV("mvctitle")
async def _(client, message):
    emo = Emoji(client)
    await emo.get()
    chat_id = message.chat.id
    pros = await message.reply(f"{emo.proses}<b>Setting Voice Chat Title ..</b>")
    if len(message.command) < 2:
        return await pros.edit(
            f"{emo.gagal}<b>Provide text/reply to text to set as Voice Chat Title.</b>"
        )
    title = message.text.split(maxsplit=1)[1]
    try:
        chat = await client.get_chat(chat_id)
    except Exception:
        return await pros.edit(
            f"{emo.gagal}<b>Cannot find the group <code>{chat_id}</code></b>"
        )
    chat_title = chat.title
    try:
        group_call = await client.get_call(client, chat_id)
        if not group_call:
            return await pros.edit(
                f"{emo.gagal}<b>No Voice Chat:\n{emo.profil}Group: <code>{chat_title}</code></b>"
            )

        await client.invoke(
            functions.phone.EditGroupCallTitle(
                call=InputGroupCall(
                    id=group_call.id, access_hash=group_call.access_hash
                ),
                title=title,
            )
        )
        return await pros.edit(
            f"{emo.sukses}<b>Successfully changed Voice Chat Title:\n{emo.profil}Group: <code>{chat_title}</code>.\n{emo.warn}Title: <code>{title}</code>.</b>"
        )
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            return await pros.edit(f"{emo.gagal}<b>You are not an admin!</b>")
        return await pros.edit(
            f"{emo.profil}Group: <code>{message.chat.title}</code>{emo.gagal}Error:\n <code>{str(e)}</code></b>"
        )


@CMD.UBOT("joinos")
@CMD.DEV_CMD("mjoinos")
@CMD.FAKEDEV("mjoinos")
@CMD.FAKE_NLX
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_}**")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    sk = 0
    gl = 0
    if "/+" in str(chat_id):
        gid = await client.get_chat(str(chat_id))
        chat_id = int(gid.id)
    elif "t.me/" in str(chat_id) or "@" in str(chat_id):
        chat_id = chat_id.replace("https://t.me/", "")
        gid = await client.get_chat(str(chat_id))
        chat_id = int(gid.id)
    else:
        chat_id = int(chat_id)
    try:
        for X in client._ubot:
            try:
                await X.group_call.play(chat_id)
                await X.group_call.mute_stream(chat_id)
                sk += 1
            except:
                gl += 1
                continue
        await proses.delete()
        return await message.reply(
            "<b>{} Berhasil Naik Os:\nChat ID: `{}`\nSukses `{}`\nGagal `{}`\nDari Total Userbot: {}</b>".format(
                em.sukses, chat_id, sk, gl, len(client._ubot)
            )
        )
    except Exception as e:
        await proses.delete()
        return await message.reply(f"{em.gagal}**ERROR:** {str(e)}")


@CMD.UBOT("turunos")
@CMD.DEV_CMD("mturunos")
@CMD.FAKEDEV("mturunos")
@CMD.FAKE_NLX
async def _(client, message):
    em = Emoji(client)
    await em.get()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = await em.get_costum_text()
    proses = await message.reply(f"{em.proses}**{proses_}**")
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    sk = 0
    gl = 0
    if "/+" in str(chat_id):
        gid = await client.get_chat(str(chat_id))
        chat_id = int(gid.id)
    elif "t.me/" in str(chat_id) or "@" in str(chat_id):
        chat_id = chat_id.replace("https://t.me/", "")
        gid = await client.get_chat(str(chat_id))
        chat_id = int(gid.id)
    else:
        chat_id = int(chat_id)
    try:
        for X in client._ubot:
            try:
                await X.group_call.leave_call(chat_id)
                sk += 1
            except:
                gl += 1
                continue
        await proses.delete()
        return await message.reply(
            "<b>{} Berhasil Turun Os:\nChat ID: `{}`\nSukses `{}`\nGagal `{}`\nDari Total Userbot: {}</b>".format(
                em.sukses, chat_id, sk, gl, len(client._ubot)
            )
        )
    except Exception as e:
        await proses.delete()
        return await message.reply(f"{em.gagal}**ERROR:** {str(e)}")
