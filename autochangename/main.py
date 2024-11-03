""" Module to automate message deletion. """

import traceback
from datetime import datetime, timedelta, timezone

from pagermaid.dependence import scheduler
from pagermaid.services import bot
from pagermaid.utils import pip_install, logs

pip_install("emoji")

from emoji import emojize

auto_change_name_init = False
dizzy = emojize(":dizzy:", language="alias")
cake = emojize(":cake:", language="alias")
all_time_emoji_name = [
    "clock12",
    "clock1230",
    "clock1",
    "clock130",
    "clock2",
    "clock230",
    "clock3",
    "clock330",
    "clock4",
    "clock430",
    "clock5",
    "clock530",
    "clock6",
    "clock630",
    "clock7",
    "clock730",
    "clock8",
    "clock830",
    "clock9",
    "clock930",
    "clock10",
    "clock1030",
    "clock11",
    "clock1130",
]
time_emoji_symb = [emojize(f":{s}:", language="alias") for s in all_time_emoji_name]

def get_status_emoji(hour):
    if 0 <= hour < 6:
        return "💤"
    elif 6 <= hour < 7:
        return "🍳"
    elif 7 <= hour < 8:
        return "🪞"
    elif 8 <= hour < 9:
        return "🚌"
    elif 9 <= hour < 11:
        return "🐟"
    elif 11 <= hour < 12:
        return "🍚"
    elif 12 <= hour < 13:
        return "💅"
    elif 13 <= hour < 14:
        return "🥱"
    elif 14 <= hour < 15:
        return "🧹"
    elif 15 <= hour < 16:
        return "🛍️"
    elif 16 <= hour < 17:
        return "🍘"
    elif 17 <= hour < 19:
        return "🥗"
    elif 19 <= hour < 20:
        return "♨️"
    elif 20 <= hour < 21:
        return "🍼"
    elif 21 <= hour < 22:
        return "🛁"
    else:
        return "🌙"

def get_time_period(hour):
    if 0 <= hour < 3:
        return "未明"
    elif 3 <= hour < 6:
        return "明け方"
    elif 6 <= hour < 9:
        return "朝"
    elif 9 <= hour < 11:
        return "昼前"
    elif 11 <= hour < 13:
        return "昼頃"
    elif 13 <= hour < 15:
        return "昼過ぎ"
    elif 15 <= hour < 18:
        return "夕方"
    elif 18 <= hour < 21:
        return "夜初め"
    else:
        return "夜遅く"

@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        dt = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=9)))
        hour = dt.strftime("%-I")
        minu = dt.strftime("%M")
        period = get_time_period(dt.hour)
        emoji = get_status_emoji(dt.hour)
        shift = 1 if int(minu) > 30 else 0
        hsym = time_emoji_symb[(dt.hour % 12) * 2 + shift]
        _first_name = f"ミドリ♪ {emoji} {period}{hour}:{minu} {hsym}"
        await bot.update_profile(first_name=_first_name)
        me = await bot.get_me()
        if me.first_name != _first_name:
            raise Exception("修改 first_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"更新失败! \n{trac}")