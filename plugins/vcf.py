import csv
import os

from pyrogram import Client, filters
from pyrogram.types import Message
from Haji.helpers import CMD

__MODULES__ = "Vcf"
__HELP__ = """
<blockquote>⪼ **--Command help Vcf--**</blockquote>

**ᐉ Keterangan: Mengubah file .csv atau .txt menjadi file .vcf**
ᐈ Perintah: `{0}vcfconvert` (reply file .csv atau .txt) 

    Dengan format:
    <i>Nama Kontak,Nomor HP</i>

<blockquote>**Contoh isi file:**</blockquote>
`John Doe,081234567890`
`Jane Smith,+6281234567891`

<b>   {1}</b>
"""


@CMD.UBOT("vcfconvert")
async def vcf_converter(client: Client, message: Message):
    reply = message.reply_to_message

    if not reply or not reply.document:
        return await message.reply("❗ Balas file `.csv` atau `.txt` yang berisi daftar kontak.")

    # Unduh file csv/txt
    file_path = await client.download_media(reply)
    output_path = file_path.rsplit(".", 1)[0] + ".vcf"
    count = 0

    try:
        with open(file_path, "r", encoding="utf-8") as csv_file, open(output_path, "w", encoding="utf-8") as vcf_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) < 2:
                    continue
                name, number = row[0].strip(), row[1].strip()
                vcf_file.write("BEGIN:VCARD\n")
                vcf_file.write("VERSION:3.0\n")
                vcf_file.write(f"FN:{name}\n")
                vcf_file.write(f"TEL;TYPE=CELL:{number}\n")
                vcf_file.write("END:VCARD\n\n")
                count += 1

        await message.reply_document(
            document=output_path,
            caption=f"✅ Berhasil dikonversi {count} kontak ke file VCF."
        )

    except Exception as e:
        await message.reply(f"❌ Terjadi kesalahan saat konversi:\n<code>{e}</code>")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(output_path):
            os.remove(output_path)
