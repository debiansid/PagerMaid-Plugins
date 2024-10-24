from datetime import datetime

from pagermaid.dependence import scheduler
from pagermaid.services import bot


@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        local_time = datetime.now().strftime("%H:%M:%S")
        hour, minu = local_time.split(":")[:2]
        _last_name = f"{hour}:{minu}"
        await bot.update_profile(last_name=_last_name)
        me = await bot.get_me()
        if me.last_name != _last_name:
            pass
    except Exception:
        pass