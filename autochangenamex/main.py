import traceback
from datetime import datetime, timezone

from pagermaid.dependence import scheduler
from pagermaid.services import bot
from pagermaid.utils import logs


@scheduler.scheduled_job("cron", second=0, id="autochangename")
async def change_name_auto():
    try:
        local_time = datetime.now().strftime("%H:%M:%S")
        hour, minu = local_time.split(":")[:2]
        _last_name = f"{hour}:{minu}"
        await bot.update_profile(last_name=_last_name)
        me = await bot.get_me()
        if me.last_name != _last_name:
            raise Exception("修改 last_name 失败")
    except Exception as e:
        trac = "\n".join(traceback.format_exception(e))
        await logs.info(f"更新失败! \n{trac}")