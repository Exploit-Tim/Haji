import openrouteservice
from geopy.geocoders import Nominatim
from pyrogram.types import Message
from Haji import haji
from geopy.distance import geodesic
from Haji.helpers import CMD

__MODULES__ = "Jarak"

__HELP__ = """
<blockquote>⪼ **--Command help Jarak--**</blockquote>

**ᐉ Keterangan: Hitung jarak dan estimasi waktu tempuh antar lokasi**
ᐈ Perintah: `{0}jarak` [kota1]-[kota2] [kendaraan]

<blockquote>**📍 Contoh:**</blockquote>
ᐈ Perintah: `{0}jarak Jakarta-Bandung mobil`
ᐈ Perintah: `{0}jarak Solo-Jogja jalan`

<blockquote>**🚗 Jenis Kendaraan yang Didukung:**</blockquote>
    - `mobil`
    - `motor`
    - `truk`
    - `sepeda`
    - `jalan`

<b>   {1}</b>
"""

# Ganti dengan API Key OpenRouteService milik Paduka
ORS_API_KEY = "5b3ce3597851110001cf62487dd357ed4176459c91200d240a5aa4b4"

client = openrouteservice.Client(key=ORS_API_KEY)
geolocator = Nominatim(user_agent="jarakbot", timeout=10)

def is_self_userbot(message: Message) -> bool:
    return message.from_user and message.from_user.is_self


# Mapping jenis kendaraan + emoji
VEHICLE_MAP = {
    "mobil": ("driving-car", "🚗"),
    "motor": ("driving-car", "🛵"),
    "truk": ("driving-hgv", "🚚"),
    "sepeda": ("cycling-regular", "🚴"),
    "jalan": ("foot-walking", "🚶"),
    "kursi": ("wheelchair", "♿"),
}


@CMD.UBOT("jarak")
async def jarak_handler(_, message: Message):
    if not is_self_userbot(message):
        return

    if len(message.command) < 2:
        return await message.reply("❗ Contoh penggunaan:\n`.jarak Jakarta-Bandung mobil`")

    try:
        # Ambil argumen dari perintah
        text = message.text.split(None, 1)[1]
        *lokasi_bagian, kendaraan_input = text.rsplit(" ", 1)

        if kendaraan_input.lower() not in VEHICLE_MAP:
            return await message.reply(
                "❗ Jenis kendaraan tidak dikenali.\nGunakan salah satu dari:\n" +
                ", ".join(VEHICLE_MAP.keys())
            )

        asal_tujuan = " ".join(lokasi_bagian)
        if "-" not in asal_tujuan:
            return await message.reply("❗ Format salah. Contoh:\n`.jarak Jakarta-Bandung motor`")

        asal, tujuan = map(str.strip, asal_tujuan.split("-", 1))
        kendaraan, emoji = VEHICLE_MAP[kendaraan_input.lower()]

        # Ambil koordinat lokasi
        asal_loc = geolocator.geocode(asal)
        tujuan_loc = geolocator.geocode(tujuan)

        if not asal_loc or not tujuan_loc:
            return await message.reply("⚠️ Lokasi tidak ditemukan.")

        koordinat_asal = (asal_loc.longitude, asal_loc.latitude)
        koordinat_tujuan = (tujuan_loc.longitude, tujuan_loc.latitude)

        # Hitung jarak dan durasi via OpenRouteService
        route = client.directions(
            coordinates=[koordinat_asal, koordinat_tujuan],
            profile=kendaraan,
            format='json'
        )

        jarak = route['routes'][0]['summary']['distance'] / 1000
        durasi = route['routes'][0]['summary']['duration'] / 3600

        await message.reply(
            f"📍 Dari: {asal.title()}\n"
            f"📍 Ke: {tujuan.title()}\n"
            f"📏 Jarak: {jarak:.2f} km\n"
            f"🕒 Estimasi ({emoji} {kendaraan_input.title()}): ±{durasi:.1f} jam"
        )

    except Exception as e:
        await message.reply(f"🚫 Terjadi kesalahan:\n`{e}`")
