from config import LOG_SELLER, SUDO_OWNERS
from Haji.database import state
from Haji.helpers import CMD, FILTERS, ButtonUtils, Message, Tools
from Haji.logger import logger


@CMD.BOT("start", FILTERS.PRIVATE)
@CMD.DB_BROADCAST
async def start_home(client, message):
    try:
        user = message.from_user
        if user.id in SUDO_OWNERS:
            buttons = ButtonUtils.start_menu(is_admin=True)
        else:
            buttons = ButtonUtils.start_menu(is_admin=False)
            sender_id = message.from_user.id
            sender_mention = message.from_user.mention
            sender_name = message.from_user.first_name
            await client.send_message(
                LOG_SELLER,
                f"<b>ᴜꜱᴇʀ : {sender_mention}\nɪᴅ : `{sender_id}`\nɴᴀᴍᴀ : {sender_name}\nᴛᴇʟᴀʜ ᴍᴇᴍᴜʟᴀɪ ʙᴏᴛ ᴀɴᴅᴀ.</b>",
            )
        text = Message.welcome_message(client, message)
        return await message.reply_text(
            text, reply_markup=buttons, disable_web_page_preview=True
        )
    except Exception as er:
        logger.error(f"{str(er)}")


@CMD.BOT("button")
async def _(client, message):
    link = message.text.split(None, 1)[1]
    tujuan, _id = Tools.extract_ids_from_link(link)
    txt = state.get(message.from_user.id, "edit_reply_markup")
    teks, button = ButtonUtils.parse_msg_buttons(txt)
    if button:
        button = ButtonUtils.create_inline_keyboard(button)
    return await client.edit_message_reply_markup(
        chat_id=tujuan, message_id=_id, reply_markup=button
    )


@CMD.BOT("id")
async def _(client, message):
    if len(message.command) < 2:
        return
    query = message.text.split()[1]
    try:
        reply = message.reply_to_message
        media = Tools.get_file_id(reply)
        data = {"file_id": media["file_id"], "type": media["message_type"]}
        state.set(message.from_user.id, query, data)
        return
    except Exception as er:
        logger.error(f"{str(er)}")
