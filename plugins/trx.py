import json
import os
from datetime import datetime
from pyrogram.types import Message
from Haji.helpers import CMD
from Haji import haji

__MODULES__ = "Trx"
__HELP__ = """
<blockquote>⪼ **--Command help Transaksi--**</blockquote>

**ᐉ Keterangan: Simpan ID channel transaksi**
ᐈ Perintah: `{0}setch` (id_channel)

**ᐉ Keterangan: Tampilkan format transaksi**
ᐈ Perintah: `{0}trx` barang,nominal,payment
	
**ᐉ Keterangan: Kirim transaksi ke channel**
ᐈ Perintah: `{0}trxdone` barang,nominal,payment

<blockquote>**Contoh:**</blockquote>
`setch -10098283792` mengatur pesan ke channel
`{0}trxdone Ubot,25000,Qris` mengirim pesan otomatis ke channel
`{0}trx Teleprem,55000,Dana`

<b>   {1}</b>
"""

CONFIG_FILE = "trx_config.json"

# Fungsi: hanya userbot sendiri
def is_self_userbot(message: Message) -> bool:
    return message.from_user and message.from_user.is_self

# Load config
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

# Save config
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# Format teks transaksi
def generate_transaksi_text(barang, nominal, payment):
    tanggal = datetime.now().strftime("%d-%m-%Y")
    jam = datetime.now().strftime("%H:%M")
    return f"""「 𝗧𝗥𝗔𝗡𝗦𝗔𝗞𝗦𝗜 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 」

<b>📦 Barang : {barang}</b>
<b>💸 Nominal : Rp. {nominal}</b>
<b>📆 Tanggal : {tanggal}</b>
<b>⏰ Jam : {jam}</b>
<b>💬 Payment : {payment}</b>

𝗧𝗲𝗿𝗶𝗺𝗮𝗸𝗮𝘀𝗶𝗵 𝗧𝗲𝗹𝗮𝗵 𝗢𝗿𝗱𝗲𝗿"""

# Handler: setch
@CMD.UBOT("setch")
async def set_channel(_, message: Message):
    if not is_self_userbot(message):
        return

    if len(message.command) < 2:
        return await message.reply("❗ Masukkan ID channel.\nContoh: `.setch -1001234567890`")

    channel_id = message.command[1]
    if not channel_id.startswith("-100"):
        return await message.reply("🚫 ID channel harus diawali dengan -100.")

    config = load_config()
    config["channel_id"] = channel_id
    save_config(config)
    await message.reply(f"✅ Channel <code>{channel_id}</code> berhasil disimpan.")

# Handler: trx (tampilkan transaksi)
@CMD.UBOT("trx")
async def show_transaksi(_, message: Message):
    if not is_self_userbot(message):
        return

    if len(message.command) < 2:
        return await message.reply("❗ Format salah. Contoh: `.trx barang,500,dana`")

    try:
        data = message.text.split(None, 1)[1]
        barang, nominal, payment = [x.strip() for x in data.split(",")]
        text = generate_transaksi_text(barang, nominal, payment)
        await message.reply(text)
    except Exception:
        await message.reply("🚫 Format salah. Gunakan seperti ini:\n`.trx barang,500,dana`")

# Handler: trxdone (kirim ke channel)
@CMD.UBOT("trxdone")
async def done_transaksi(_, message: Message):
    if not is_self_userbot(message):
        return

    if len(message.command) < 2:
        return await message.reply("❗ Format salah. Contoh: `.trxdone barang,500,dana`")

    try:
        data = message.text.split(None, 1)[1]
        barang, nominal, payment = [x.strip() for x in data.split(",")]
        text = generate_transaksi_text(barang, nominal, payment)

        config = load_config()
        channel_id = config.get("channel_id")
        if not channel_id:
            return await message.reply("🚫 Belum ada channel tujuan. Set dulu pakai `.setch <id_channel>`")

        await _.send_message(int(channel_id), text)
        await message.reply("✅ Transaksi berhasil dikirim ke channel.")
    except Exception as e:
        await message.reply(f"🚫 Gagal mengirim transaksi:\n<code>{e}</code>")

