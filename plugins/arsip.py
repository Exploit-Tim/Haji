from pyrogram import Client, filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import Message
from Haji.helpers import CMD

__MODULES__ = "Arsip"
__HELP__ = """
<blockquote>⪼ **--Command help Arsip--**</blockquote>

<blockquote>**Perintah Arsip**</blockquote>
**ᐉ Keterangan: Arsipkan semua chat**
ᐈ Perintah: `{0}arsip all`
**ᐉ Keterangan: Arsipkan semua grup**
ᐈ Perintah: `{0}arsip group`
**ᐉ Keterangan: Arsipkan semua channel**
ᐈ Perintah: `{0}arsip channel`
**ᐉ Keterangan: Arsipkan semua chat pribadi**
ᐈ Perintah: `{0}arsip user`
**ᐉ Keterangan: Arsipkan semua chat dengan bot**
ᐈ Perintah: `{0}arsip bot`
**ᐉ Keterangan: Arsipkan 10 chat terakhir**
ᐈ Perintah: `{0}arsip 10`

<blockquote>**Perintah Unarsip**</blockquote>
**ᐉ Keterangan: Unarsip semua chat**
ᐈ Perintah: `{0}unarsip all`
**ᐉ Keterangan: Unarsip grup saja**
ᐈ Perintah: `{0}unarsip group`
**ᐉ Keterangan: Unarsip channel saja**
ᐈ Perintah: `{0}unarsip channel`
**ᐉ Keterangan: Unarsip chat pribadi**
ᐈ Perintah: `{0}unarsip user`
**ᐉ Keterangan: Unarsip bot**
ᐈ Perintah: `{0}unarsip bot`
**ᐉ Keterangan: Unarsip 5 chat terakhir**
ᐈ Perintah: `{0}unarsip 5`

<blockquote>**Perintah Cek**</blockquote>
**ᐉ Keterangan: Cek semua chat aktif**
ᐈ Perintah: `{0}cekchat`

<b>   {1}</b>
"""

def filter_targets(dialogs, query):
    targets = []
    for dialog in dialogs:
        chat = dialog.chat

        if query == "all":
            targets.append(chat.id)
        elif query == "group" and chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
            targets.append(chat.id)
        elif query == "channel" and chat.type == ChatType.CHANNEL:
            targets.append(chat.id)
        elif query == "bot" and getattr(chat, "is_bot", False):
            targets.append(chat.id)
        elif query == "user" and chat.type == ChatType.PRIVATE and not getattr(chat, "is_bot", False):
            targets.append(chat.id)
    return targets

@CMD.UBOT("arsip")
async def archive_chat(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❗ Gunakan `.arsip [all|group|channel|bot|user|angka]`")

    query = message.command[1].lower()
    reply = await message.reply("🔄 Mengambil daftar chat...")

    dialogs = [dialog async for dialog in client.get_dialogs()]
    targets = filter_targets(dialogs, query)

    if query.isdigit():
        jumlah = int(query)
        targets = [dialog.chat.id for dialog in dialogs[:jumlah]]

    if not targets:
        return await reply.edit("🚫 Tidak ada chat yang cocok ditemukan.")

    for cid in targets:
        try:
            await client.archive_chats(cid)
        except Exception:
            continue

    await reply.edit(f"✅ Berhasil mengarsipkan {len(targets)} chat.")

@CMD.UBOT("unarsip")
async def unarchive_chat(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❗ Gunakan `.unarsip [all|group|channel|bot|user|angka]`")

    query = message.command[1].lower()
    reply = await message.reply("🔄 Mengambil daftar chat...")

    dialogs = [dialog async for dialog in client.get_dialogs()]
    targets = filter_targets(dialogs, query)

    if query.isdigit():
        jumlah = int(query)
        targets = [dialog.chat.id for dialog in dialogs[:jumlah]]

    if not targets:
        return await reply.edit("🚫 Tidak ada chat yang cocok ditemukan.")

    for cid in targets:
        try:
            await client.unarchive_chats(cid)
        except Exception:
            continue

    await reply.edit(f"✅ Berhasil meng-unarsipkan {len(targets)} chat.")

@CMD.UBOT("cekchat")
async def cek_chat(client: Client, message: Message):
    reply = await message.reply("📥 Mengambil semua chat...")
    dialogs = [dialog async for dialog in client.get_dialogs()]
    teks = ""

    for dialog in dialogs:
        chat = dialog.chat
        nama = chat.title or getattr(chat, "first_name", "Tanpa Nama")
        tipe = chat.type.value
        teks += f"🔹 <b>{nama}</b>\n🧾 <code>{chat.id}</code> | <i>{tipe}</i>\n\n"

    if not teks:
        return await reply.edit("🚫 Tidak ada chat ditemukan.")
 

    await reply.edit(teks[:4096], parse_mode=ParseMode.HTML)
