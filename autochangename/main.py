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


@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        time_cur = (
            datetime.utcnow()
            .replace(tzinfo=timezone.utc)
            .astimezone(timezone(timedelta(hours=9)))
            .strftime("%-I:%M:%S %p:%a")
        )
        hour, minu, seco, p, abbwn = time_cur.split(":")
        period = "午前" if "AM" in p else "午後"
        shift = 1 if int(minu) > 30 else 0
        hsym = time_emoji_symb[(int(hour) % 12) * 2 + shift]
        _first_name = f"ミドリ♪ {period}{hour}:{minu} UTC+9 {hsym}"
        await bot.update_profile(first_name=_first_name)
        me = await bot.get_me()
        if me.first_name != _first_name:
            raise Exception("修改 first_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"更新失败! \n{trac}")