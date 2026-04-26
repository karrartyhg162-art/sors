import os
from asyncio.exceptions import CancelledError
from time import sleep

from zthon import zedub

from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP, mention

LOGS = logging.getLogger(__name__)
plugin_category = "الادوات"


@zedub.zed_cmd(
    pattern="اعادة تشغيل$",
    command=("اعادة تشغيل", plugin_category),
    info={
        "header": "لـ إعـادة تشغيـل البـوت",
        "الاستخـدام": "{tr}اعادة تشغيل",
    },
    disable_errors=True,
)
async def _(event):
    "لـ إعـادة تشغيـل البـوت"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#إعــادة_التشغيــل\n\n" "**⪼ بـوت الحارس الذكي في وضـع اعـادة التشغيـل انتظـر**\n\n" "**⪼ اذ لـم يستجـب البـوت بعـد خمـس دقائـق .. قـم بالذهـاب الـى حسـاب هيـروكو واعـادة التشغيـل اليـدوي**")
    sandy = await edit_or_reply(
        event,
        f"**•⎆┊أهـلًا عـزيـزي** - {mention}\n\n"
        f"**•⎆┊يتـم الان اعـادة تشغيـل بـوت الحارس الذكي قـد يستغـرق الامـر 1-2 دقيقـة ▬▭ ...**",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS.error(e)
    try:
        await zedub.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS.error(e)


@zedub.zed_cmd(
    pattern="ايقاف البوت$",
    command=("ايقاف البوت", plugin_category),
    info={
        "header": "لـ إطفـاء البـوت",
        "الوصـف": "لـ إطفـاء الداينـو الخاص بتنصيبك بهيروكـو .. لا تستطيع اعادة التشغيل مرة اخرى عبر حسابك عليك الذهاب لحساب هيروكو واتباع الشرح التالي https://t.me/SI0lZ",
        "الاستخـدام": "{tr}ايقاف البوت",
    },
)
async def _(event):
    "لـ إطفـاء البـوت"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#ايقــاف البــوت\n\n" "**- بـوت الحارس الذكي فـي وضــع الايقــاف**")
    await edit_or_reply(event, "**✾╎جــارِ إيقـاف تشغيـل بـوت الحارس الذكي الآن 📟 ...**\n\n**✾╎شغِّـلنـي يـدويًـا لاحقًــا**\n**✾╎باتبـاع الشـرح** https://t.me/SI0lZ")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        os._exit(143)


@zedub.zed_cmd(
    pattern="نوم( [0-9]+)?$",
    command=("نوم", plugin_category),
    info={
        "header": "البـوت الخـاص بك سيتوقف موقتـاً .. حسب الثوانـي المدخلـه",
        "الاستخـدام": "{tr}نوم <عـدد الثـواني>",
        "مثــال": "{tr}نوم 60",
    },
)
async def _(event):
    "لـ إيقـاف البـوت مؤقـتـًا"
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "**- عـذراً .. قم بادخـال عـدد الثواني للامـر**\n**- مثــال :**\n`.نوم 60`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"**- لقـد تم وضـع البـوت في وضـع النـوم لمـدة {counter} ثـانيـه✓**"
        )

    event = await edit_or_reply(event, f"**- تم وضـع البـوت في وضـع النـوم لمـدة {counter} ثـانيـه✓**")
    sleep(counter)
    await event.edit("**✾╎لقـد عـدت 🏃...**\n**✾╎انا الآن في وضـع التشغيـل ☑️**")


@zedub.zed_cmd(
    pattern="الاشعارات (تفعيل|تعطيل)$",
    command=("notify", plugin_category),
    info={
        "header": "To update the your chat after restart or reload .",
        "الوصـف": "Will send the ping cmd as reply to the previous last msg of (restart/reload/update cmds).",
        "الاستخـدام": [
            "{tr}الاشعارات <تفعيل/تعطيل>",
        ],
    },
)
async def set_pmlog(event):
    "To update the your chat after restart or reload ."
    input_str = event.pattern_match.group(1)
    if input_str == "تعطيل":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "__Notify already disabled__")
        delgvar("restartupdate")
        return await edit_or_reply(event, "__Notify is disable successfully.__")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "__Notify is enable successfully.__")
    await edit_delete(event, "__Notify already enabled.__")
