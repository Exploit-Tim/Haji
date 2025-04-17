import requests
import os
from config import API_BOTCHAX
from Haji.helpers import CMD, Emoji

__MODULES__ = "Xnxx"
__HELP__ = 
"""<blockquote>⪼ **--Command help XNXX--**</blockquote>

**Generate Video Using XNXX API**
**ᐉ Keterangan: Anda dapat mencari dan mengunduh video dari XNXX**
ᐈ Perintah: `{0}xnxx` (text)

   {1}
"""

@CMD.UBOT("xnxx")
async def _(client, message):
    try:
        em = Emoji(client)
        await em.get()

        query = message.text.split()[1:]
        if not query:
            await message.reply(f"**{em.gagal} Gunakan Format: `.xnxx [ Query ]`\n➡️ Contoh: `.xnxx Japanese`**")
            return

        search_query = " ".join(query[:4])

        status_msg = await message.reply(f"**{em.proses} Mencari Video 18+: **{search_query}...__**")

        api_url = f"https://api.botcahx.eu.org/api/search/xnxx?query={search_query}&apikey={API_BOTCHAX}"

        response = requests.get(api_url)
        response.raise_for_status()
        api = response.json()

        results = api.get('result', [])
        if not results:
            await status_msg.edit(f"**{em.gagal} Tidak Ditemukan Hasil Untuk: `{search_query}`**")
            return

        data = results[0]

        capt = f"""
📑 Hasil Pencarian: {search_query}
◦ 📍 Title : {data.get('title', 'N/A')}
◦ 👁 Views : {data.get('views', 'N/A')}
◦ 🎥 Quality : {data.get('quality', 'N/A')}
◦ ⌛️ Duration : {data.get('duration', 'N/A')}
◦ **[🔗 Link ]({data.get('link', 'N/A')})
"""

        await status_msg.edit(f"**{em.proses} Mengunduh Video: **{data.get('title', 'N/A')}...__**")

        dl_url = f"https://api.botcahx.eu.org/api/download/xnxxdl?url={data['link']}&apikey={API_BOTCHAX}"
        dl_response = requests.get(dl_url)
        dl_response.raise_for_status()
        dl_data = dl_response.json()
        video_url = dl_data.get('result', {}).get('url')

        if not video_url:
            await status_msg.edit(f"**{em.gagal} Gagal mendapatkan URL video.**")
            return

        video_path = "video.mp4"

        await status_msg.edit(f"**{em.proses} Sedang Mengunduh Video, Harap Tunggu...**")
        with requests.get(video_url, stream=True) as vid_res:
            vid_res.raise_for_status()
            with open(video_path, "wb") as f:
                for chunk in vid_res.iter_content(chunk_size=8192):
                    f.write(chunk)

        await status_msg.edit(f"**{em.proses} Mengunggah Video Ke Telegram...**")

        await client.send_video(message.chat.id, video_path, caption=capt)
        os.remove(video_path)

        await status_msg.delete()

    except requests.exceptions.RequestException as e:
        await message.reply(f"**{em.gagal} Terjadi Kesalahan Saat Mengakses API: {str(e)}**")
