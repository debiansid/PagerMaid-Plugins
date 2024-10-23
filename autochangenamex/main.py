import traceback
from datetime import datetime, timedelta, timezone

from pagermaid.enums import Message
from pagermaid.listener import listener
from pagermaid.dependence import scheduler
from pagermaid.services import bot, sqlite
from pagermaid.utils import pip_install, logs

pip_install("emoji")

from emoji import emojize

dizzy = emojize(":dizzy:", language="alias")
cake = emojize(":cake:", language="alias")
all_time_emoji_name = [
    "clock12", "clock1230", "clock1", "clock130", "clock2", "clock230",
    "clock3", "clock330", "clock4", "clock430", "clock5", "clock530",
    "clock6", "clock630", "clock7", "clock730", "clock8", "clock830",
    "clock9", "clock930", "clock10", "clock1030", "clock11", "clock1130"
]
time_emoji_symb = [emojize(f":{s}:", language="alias") for s in all_time_emoji_name]


def get_timezone_settings():
    return sqlite.get("autochangenamex.timezone", 9), sqlite.get("autochangenamex.name_type", "last_name")


def set_timezone_settings(timezone_offset: int, name_type: str) -> None:
    sqlite.update({
        "autochangenamex.timezone": timezone_offset,
        "autochangenamex.name_type": name_type
    })


@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        user_timezone_offset, name_type = get_timezone_settings()
        time_cur = (
            datetime.utcnow()
            .replace(tzinfo=timezone.utc)
            .astimezone(timezone(timedelta(hours=user_timezone_offset)))
            .strftime("%H:%M:%S:%p:%a")
        )
        hour, minu, seco, abbwn = time_cur.split(":")
        shift = 1 if int(minu) > 30 else 0
        hsym = time_emoji_symb[(int(hour) % 12) * 2 + shift]
        _name = f"{hour}:{minu} UTC+{user_timezone_offset} {hsym}"

        if name_type == "first_name":
            await bot.update_profile(first_name=_name)
        elif name_type == "last_name":
            await bot.update_profile(last_name=_name)

        me = await bot.get_me()
        if (name_type == "first_name" and me.first_name != _name) or \
           (name_type == "last_name" and me.last_name != _name):
            raise Exception(f"修改 {name_type} 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"更新失败! \n{trac}")


@listener(
    command="autochangenamex",
    description="设置自动修改名字的时区和修改目标 (first_name 或 last_name)。",
    parameters="<时区> <firstname|lastname>"
)
async def set_timezone_and_name(message: Message):
    try:
        if not message.parameter:
            timezone_offset, name_type = get_timezone_settings()
            return await message.edit(f"当前时区设置为 UTC{timezone_offset:+d}，自动修改 {name_type}。")

        args = message.parameter.split()
        if len(args) != 2:
            return await message.edit("格式错误！正确格式：autochangenamex <时区> <firstname|lastname>")

        tz_offset = int(args[0])
        if not (-12 <= tz_offset <= 14):
            return await message.edit("无效的时区值，请输入介于 -12 和 +14 之间的整数。")

        if args[1] not in ["firstname", "lastname"]:
            return await message.edit("无效的参数，请输入 'firstname' 或 'lastname'。")

        set_timezone_settings(tz_offset, args[1])

        await message.edit(f"时区已设置为 UTC{tz_offset:+d}，将自动修改 {args[1]}。")

    except ValueError:
        await message.edit("请输入有效的整数时区值。")
    except Exception as e:
        await message.edit(f"发生错误：{str(e)}")
