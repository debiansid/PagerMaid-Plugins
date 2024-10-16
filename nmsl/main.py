from asyncio import sleep
from pyrogram.errors import ChatAdminRequired, FloodWait
from pagermaid.dependence import add_delete_message_job
from pagermaid.listener import listener
from pagermaid.services import bot
from pagermaid.enums import Message
from pagermaid.utils import lang


async def ban_user(chat_id: int, user_id: int):
    await bot.ban_chat_member(chat_id, user_id)
    await bot.delete_user_history(chat_id, user_id)


@listener(
    command="sb",
    description=lang("sb_des"),
    need_admin=True,
    groups_only=True,
)
async def super_ban(message: Message):
    chat = message.chat
    reply = message.reply_to_message

    if not reply or not reply.from_user:
        await message.edit(lang("arg_error"))  # 必须回复目标消息
        return add_delete_message_job(message, 10)

    uid = reply.from_user.id
    user_mention = reply.from_user.mention
    chat_title = chat.title

    try:
        await ban_user(chat.id, uid)
        text = f'用户 {user_mention} (`{uid}`) 已在群组 {chat_title} (`{chat.id}`) 被封禁。'
        await message.edit(text)
    except ChatAdminRequired:
        await message.edit(lang("sb_no_per"))
    except FloodWait as e:
        await sleep(e.value)
        await ban_user(chat.id, uid)
        text = f'用户 {user_mention} (`{uid}`) 已在群组 {chat_title} (`{chat.id}`) 被封禁。'
        await message.edit(text)
    except Exception as e:
        await message.edit(f"出现错误：{e}")
    finally:
        add_delete_message_job(message, 10)
