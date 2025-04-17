import random
from datetime import datetime
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.enums import ParseMode
from Haji.helpers import CMD
from Haji import haji

__MODULES__ = "Fun"
__HELP__ = """
<blockquote>⪼ **--Command help Fun--**</blockquote>

**ᐉ Keterangan: Fake global ban target**
ᐈ Perintah: `{0}gben` [username/reply]
**ᐉ Keterangan: Fake global mute target**
ᐈ Perintah: `{0}gmut` [username/reply]
**ᐉ Keterangan: Fake global kick target**
ᐈ Perintah: `{0}gkik` [username/reply]
**ᐉ Keterangan: Fake transfer saldo ke target**
ᐈ Perintah: `{0}ftf` [username/reply] [jumlah]

<blockquote>Contoh:</blockquote>
`{0}gben` @target
`{0}ftf` @target 10000

<b>   {1}</b>
"""

# Cek hanya untuk userbot
def is_self_userbot(message: Message) -> bool:
    return message.from_user and message.from_user.is_self

# Ambil target dari reply atau command
def get_target(message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        return f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    elif len(message.command) >= 2:
        return message.command[1]
    else:
        return None

# Format waktu
def get_time():
    return datetime.now().strftime("%Y-%m-%d")

# Format rupiah
def format_rupiah(amount: str):
    try:
        return f"{int(amount):,}".replace(",", ".")
    except ValueError:
        return amount

# Random statistik grup
def get_stats():
    berhasil = random.randint(1000, 5000)
    gagal = max(1, int(berhasil * 0.0016))  # ~0.16%
    return berhasil, gagal

@CMD.UBOT("gben")
async def fake_gban(_, m: Message):
    if not is_self_userbot(m): return
    target = get_target(m)
    if not target:
        return await m.reply("❗ Masukkan username atau balas pesan target.")
    berhasil, gagal = get_stats()
    await m.reply(
        f"🚫 <b>Global Ban Issued</b>\n\n👤 Target: {target}\n"
        f"📊 Berhasil: {berhasil} Grup\n❌ Gagal: {gagal} Grup\n🕐 Tanggal: {get_time()}",
        parse_mode=ParseMode.HTML
    )

@CMD.UBOT("gmut")
async def fake_gmute(_, m: Message):
    if not is_self_userbot(m): return
    target = get_target(m)
    if not target:
        return await m.reply("❗ Masukkan username atau balas pesan target.")
    berhasil, gagal = get_stats()
    await m.reply(
        f"🔇 <b>Global Mute Issued</b>\n\n👤 Target: {target}\n"
        f"📊 Berhasil: {berhasil} Grup\n❌ Gagal: {gagal} Grup\n🕐 Tanggal: {get_time()}",
        parse_mode=ParseMode.HTML
    )

@CMD.UBOT("gkik")
async def fake_gkick(_, m: Message):
    if not is_self_userbot(m): return
    target = get_target(m)
    if not target:
        return await m.reply("❗ Masukkan username atau balas pesan target.")
    berhasil, gagal = get_stats()
    await m.reply(
        f"🥾 <b>Global Kick Issued</b>\n\n👤 Target: {target}\n"
        f"📊 Berhasil: {berhasil} Grup\n❌ Gagal: {gagal} Grup\n🕐 Tanggal: {get_time()}",
        parse_mode=ParseMode.HTML
    )

@CMD.UBOT("ftf")
async def fake_transfer(_, m: Message):
    if not is_self_userbot(m): return
    target = get_target(m)
    if not target or len(m.command) < 3 and not m.reply_to_message:
        return await m.reply("❗ Format salah!\nGunakan: `.ftransfer @username 10000` atau reply lalu ketik `.ftransfer 10000`")
    amount = m.command[-1]
    amount_rp = format_rupiah(amount)
    await m.reply(
        f"💸 <b>Transfer Berhasil!</b>\n\n👤 Penerima: {target}\n"
        f"💰 Jumlah: Rp{amount_rp}\n🕐 Tanggal: {get_time()}\n📌 Status: Transfer telah dikirim ✨",
        parse_mode=ParseMode.HTML
    )
