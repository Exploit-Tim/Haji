from config import BOT_NAME

from ..database import dB


class Emoji:
    DEFAULT_VARS = {
        "emo_ping": "🏓",
        "emo_msg": "✉️",
        "emo_proses": "⏳",
        "emo_sukses": "✅",
        "emo_gagal": "❌",
        "emo_profil": "👤",
        "emo_owner": "⭐",
        "emo_warn": "⚠️",
        "emo_block": "⛔",
        "emo_uptime": "⏰",
        "emo_robot": "⚙️",
        "emo_klip": "📎",
        "emo_net": "🌐",
        "emo_up": "⬆️",
        "emo_down": "⬇️",
        "emo_speed": "⚡️",
        "emo_haji": "👑",
    }

    CUSTOM_EMOJI_IDS = {
        "emo_ping": 5258330865674494479,
        "emo_msg": 5260535596941582167,
        "emo_proses": 5427181942934088912,
        "emo_sukses": 5260416304224936047,
        "emo_gagal": 5260342697075416641,
        "emo_profil": 5258011929993026890,
        "emo_owner": 5258185631355378853,
        "emo_warn": 5260249440450520061,
        "emo_block": 5258362429389152256,
        "emo_uptime": 5258089153505009279,
        "emo_robot": 5258093637450866522,
        "emo_klip": 5260730055880876557,
        "emo_net": 5260348422266822411,
        "emo_up": 5260379144167890225,
        "emo_down": 5258514780469075716,
        "emo_speed": 5258152182150077732,
        "emo_haji": 6332511094166264136,
    }

    def __init__(self, client):
        self.client = client
        self.me = client.me
        self.is_premium = client.me.is_premium
        self.user_id = client.me.id
        self.mention = f"[{client.me.first_name} {client.me.last_name or ''}](tg://user?id={client.me.id})"
        self.full_name = (
            f"{self.me.first_name} {self.me.last_name if self.me.last_name else ''}"
        )

    async def set_emotes(self, new_client, is_premium):
        emotes = {
            "uptime": "⏰",
            "warn": "⚠️",
            "block": "❌",
            "ping": "🏸",
            "msg": "✉️",
            "proses": "⏳",
            "gagal": "❎",
            "sukses": "✅",
            "profil": "👤",
            "owner": "⭐️",
            "robot": "⚙️",
            "klip": "📎",
            "net": "🌐",
            "up": "⬆️",
            "down": "⬇️",
            "speed": "⚡️",
            "haji": "👑",
        }

        emote_ids = {
            "uptime": "<emoji id=5359698274318037766>⏰</emoji>",
            "warn": "<emoji id=6008233706039284019>⚠️</emoji>",
            "block": "<emoji id=5215642288071387368>❌</emoji>",
            "ping": "<emoji id=5467537163589538076>🏸</emoji>",
            "msg": "<emoji id=5913236481220022288>✉️</emoji>",
            "proses": "<emoji id=6010111371251815589>⏳</emoji>",
            "gagal": "<emoji id=5940804914220372462>❎</emoji>",
            "sukses": "<emoji id=5940635490645449104>✅</emoji>",
            "profil": "<emoji id=5373012449597335010>👤</emoji>",
            "owner": "<emoji id=6084447187742233001>⭐️</emoji>",
            "robot": "<emoji id=5350396951407895212>⚙️</emoji>",
            "klip": "<emoji id=5972261808747057065>📎</emoji>",
            "net": "<emoji id=5224450179368767019>🌐</emoji>",
            "up": "<emoji id=5445355530111437729>⬆️</emoji>",
            "down": "<emoji id=5443127283898405358>⬇️</emoji>",
            "speed": "<emoji id=5456140674028019486>⚡️</emoji>",
            "haji": "<emoji id=6332511094166264136>👑</emoji>",
        }

        emote_dict = emote_ids if is_premium else emotes

        for key, emote in emote_dict.items():
            await dB.set_var(new_client.me.id, f"emo_{key}", emote)

    async def get(self):
        me = self.client.me
        self.me = me
        self.user_id = me.id
        self.mention = f"[{me.first_name} {me.last_name or ''}](tg://user?id={me.id})"
        self.full_name = f"{me.first_name} {me.last_name or ''}"
        self.is_premium = me.is_premium
        await self.load_emoji()

    async def get_costum_text(self):
        me = self.client.me.id
        pong_ = await dB.get_var(me, "text_ping") or "ᴘɪɴɢ"
        uptime_ = await dB.get_var(me, "text_uptime") or "ᴜᴘᴛɪᴍᴇ"
        mmg = f"<a href=tg://user?id={self.client.me.id}>{self.client.me.first_name} {self.client.me.last_name or ''}</a>"
        owner_ = await dB.get_var(me, "text_owner") or f"ᴏᴡɴᴇʀ: {mmg}"
        ubot_ = await dB.get_var(me, "text_ubot") or f"{BOT_NAME}"
        proses_ = await dB.get_var(me, "text_gcast") or "ᴍᴇᴍᴘʀᴏsᴇs"
        sukses_ = await dB.get_var(me, "text_sukses") or "ɢɪᴋᴇs sᴜᴋsᴇs ᴘᴀᴋ"
        return pong_, uptime_, owner_, ubot_, proses_, sukses_

    async def load_emoji(self):
        for key in self.DEFAULT_VARS:
            var = await dB.get_var(self.user_id, key)

            if self.is_premium:
                default = self.CUSTOM_EMOJI_IDS.get(key)
                if isinstance(var, int):
                    setattr(self, key, var)
                else:
                    await dB.set_var(self.user_id, key, default)
                    setattr(self, key, default)
            else:
                default = self.DEFAULT_VARS.get(key)
                if isinstance(var, str):
                    setattr(self, key, var)
                else:
                    await dB.set_var(self.user_id, key, default)
                    setattr(self, key, default)

    async def set_emoji(self, var_name, new_value):
        if var_name not in self.CUSTOM_EMOJI_IDS and var_name not in self.DEFAULT_VARS:
            raise ValueError(f"Variabel '{var_name}' tidak valid.")
        await dB.set_var(self.user_id, var_name, new_value)
        setattr(
            self,
            var_name,
            str(new_value) if not isinstance(new_value, int) else new_value,
        )

    async def reset_emoji(self):
        if self.is_premium:
            for key, default in self.CUSTOM_EMOJI_IDS.items():
                await dB.set_var(self.user_id, key, default)
                setattr(self, key, default)
        else:
            for key, default in self.DEFAULT_VARS.items():
                await dB.set_var(self.user_id, key, default)
                setattr(self, key, default)
        return f"Emoji sudah di reset ke default untuk: {self.mention}."

    def _format_emoji(self, var, fallback_emoji):
        # Tampilkan emoji hanya jika pengguna premium
        if not self.is_premium:
            return ""  # Non-premium tidak mendapatkan emoji
        if isinstance(var, int):
            return f"<emoji id={var}>{fallback_emoji}</emoji> "
        return var

    @property
    def ping(self):
        return self._format_emoji(self.emo_ping, "🏓")

    @property
    def msg(self):
        return self._format_emoji(self.emo_msg, "✉️")

    @property
    def proses(self):
        return self._format_emoji(self.emo_proses, "⏳")

    @property
    def sukses(self):
        return self._format_emoji(self.emo_sukses, "✅")

    @property
    def gagal(self):
        return self._format_emoji(self.emo_gagal, "❌")

    @property
    def profil(self):
        return self._format_emoji(self.emo_profil, "👤")

    @property
    def owner(self):
        return self._format_emoji(self.emo_owner, "⭐")

    @property
    def warn(self):
        return self._format_emoji(self.emo_warn, "⚠️")

    @property
    def block(self):
        return self._format_emoji(self.emo_block, "⛔")

    @property
    def uptime(self):
        return self._format_emoji(self.emo_uptime, "⏰")

    @property
    def robot(self):
        return self._format_emoji(self.emo_robot, "⚙️")

    @property
    def klip(self):
        return self._format_emoji(self.emo_klip, "📎")

    @property
    def net(self):
        return self._format_emoji(self.emo_net, "🌐")

    @property
    def up(self):
        return self._format_emoji(self.emo_up, "⬆️")

    @property
    def down(self):
        return self._format_emoji(self.emo_down, "⬇️")

    @property
    def speed(self):
        return self._format_emoji(self.emo_speed, "⚡️")

    @property
    def haji(self):
        return self._format_emoji(self.emo_haji, "👑")

emotikon = [
    "😀",
    "😃",
    "😄",
    "😁",
    "😆",
    "😅",
    "😂",
    "🤣",
    "😊",
    "😇",
    "🙂",
    "🙃",
    "😉",
    "😌",
    "😍",
    "🥰",
    "😘",
    "😗",
    "😙",
    "😚",
    "😋",
    "😛",
    "😜",
    "🤪",
    "😝",
    "🤑",
    "🤗",
    "🤭",
    "🤫",
    "🤔",
    "😐",
    "😑",
    "😶",
    "😏",
    "😒",
    "🙄",
    "😬",
    "🤥",
    "😌",
    "😔",
    "😪",
    "🤤",
    "😴",
    "😷",
    "🤒",
    "🤕",
    "🤢",
    "🤮",
    "🤧",
    "🥵",
    "🥶",
    "😵",
    "🤯",
    "🤠",
    "🥳",
    "😎",
    "🤓",
    "🧐",
    "😕",
    "😟",
    "🙁",
    "☹️",
    "😮",
    "😯",
    "😲",
    "😳",
    "🥺",
    "😦",
    "😧",
    "😨",
    "😰",
    "😥",
    "😢",
    "😭",
    "😱",
    "😖",
    "😣",
    "😞",
    "😓",
    "😩",
    "😫",
    "🥱",
    "😤",
    "😡",
    "😠",
    "🤬",
    "😈",
    "👿",
    "💀",
    "☠️",
    "💩",
    "🤡",
    "👹",
    "👺",
    "👻",
    "👽",
    "👾",
    "🤖",
    "❤️",
    "🧡",
    "💛",
    "💚",
    "💙",
    "💜",
    "🤎",
    "🖤",
    "🤍",
    "💔",
    "🎉",
    "🎊",
    "🎈",
    "🎁",
    "🧸",
    "🎯",
    "🏆",
    "🏀",
    "🏈",
    "⚾",
    "🎾",
    "🎱",
    "🏓",
    "🏸",
    "🏒",
    "🏏",
]
