from datetime import datetime, timedelta, timezone
from pagermaid.dependence import scheduler
from pagermaid.services import bot

@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        time_cur = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(
            timezone(timedelta(hours=8))
        ).strftime("%I:%M %p")
        hour, minu_p = time_cur.split(":")
        minu, p = minu_p.split()
        _last_name = f"{hour}:{minu} {p}"
        await bot.update_profile(last_name=_last_name)
        me = await bot.get_me()
        if me.last_name != _last_name:
            raise Exception("修改 last_name 失败")
    except Exception:
        pass