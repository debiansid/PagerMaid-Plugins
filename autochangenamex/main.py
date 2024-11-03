from datetime import datetime, timedelta, timezone
from pagermaid.dependence import scheduler
from pagermaid.services import bot

@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        time_cur = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(
            timezone(timedelta(hours=9))
        ).strftime("%H:%M")
        hour, minu = time_cur.split(":")
        _first_name = f"{hour}:{minu}"
        await bot.update_profile(first_name=_first_name)
        me = await bot.get_me()
        if me.first_name != _first_name:
            raise Exception("修改 first_name 失败")
    except Exception:
        pass