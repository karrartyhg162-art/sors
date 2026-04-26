#𝙕𝙚𝙙𝙏𝙝𝙤𝙣 ®
#الملـف حقـوق وكتابـة زلـزال الهيبـه ⤶ @zzzzl1l خاص بسـورس ⤶ 𝙕𝙚𝙙𝙏𝙝𝙤𝙣

import asyncio
import os
from secrets import choice
import random
from urllib.parse import quote_plus
from collections import deque
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import InputMessagesFilterVideo, InputMessagesFilterVoice, InputMessagesFilterPhotos

from zthon import zedub

from zthon.core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from . import ALIVE_NAME, mention
from ..helpers import get_user_from_event
from ..helpers.utils import _format

from . import reply_id


@zedub.zed_cmd(pattern="حالات$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل حـالات واتـس ...**")
    try:
        ZTHONR = [
            zlzzl
            async for zlzzl in event.client.iter_messages(
                "@RSHDO5", filter=InputMessagesFilterVideo
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(ZTHONR),
            caption=f"**🎆┊حـالات واتـس قصيـرة 🧸♥️**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عـذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="ستوري انمي$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الستـوري ...**")
    try:
        ZTHONR = [
            zlzzl
            async for zlzzl in event.client.iter_messages(
                "@AA_Zll", filter=InputMessagesFilterVideo
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(ZTHONR),
            caption=f"**🎆┊ستـوريات آنمـي قصيـرة 🖤🧧**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عـذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="رقيه$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الرقيـه ...**")
    try:
        zedgan = [
            zlzzl77
            async for zlzzl77 in event.client.iter_messages(
                "@Rqy_1", filter=InputMessagesFilterVoice
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedgan),
            caption=f"**◞مقاطـع رقيـه شرعيـة ➧🕋🌸◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="رمادي$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الافتـار ...**")
    try:
        zedph = [
            zelzal
            async for zelzal in event.client.iter_messages(
                "@shababbbbR", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**◞افتـارات شبـاب ࢪمـاديه ➧🎆🖤◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="رماديه$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الافتـار ...**")
    try:
        zedph = [
            zelzal
            async for zelzal in event.client.iter_messages(
                "@banatttR", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**◞افتـارات بنـات ࢪمـاديه ➧🎆🤎◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="بيست$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮ - جـارِ تحميـل الآفتـار ...🧚🏻‍♀🧚🏻‍♀╰**")
    try:
        zedph = [
            zelzal
            async for zelzal in event.client.iter_messages(
                "@Tatkkkkkim", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**◞افتـارات بيست تطقيـم بنـات ➧🎆🧚🏻‍♀🧚🏻‍♀◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="حب$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮ - جـارِ تحميـل الآفتـار ...♥️╰**")
    try:
        zedph = [
            zelzal
            async for zelzal in event.client.iter_messages(
                "@tatkkkkkimh", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**◞افتـارات حـب تمبلـرࢪ ➧🎆♥️◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="رياكشن$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الرياكشـن ...**")
    try:
        ZTHONR = [
            zlzzl
            async for zlzzl in event.client.iter_messages(
                "@reagshn", filter=InputMessagesFilterVideo
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(ZTHONR),
            caption=f"** 🎬┊رياكشـن تحشيـش ➧🎃😹◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="ادت$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل مقطـع ادت ...**")
    try:
        ZTHONR = [
            asupan
            async for asupan in event.client.iter_messages(
                "@snje1", filter=InputMessagesFilterVideo
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(ZTHONR),
            caption=f"**🎬┊مقاطـع ايـدت منوعـه ➧ 🖤🎭◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="$ملغي أيضًا")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الاغنيـه ...𓅫╰**")
    try:
        zedgan = [
            desah
            async for desah in event.client.iter_messages(
                "@TEAMSUL", filter=InputMessagesFilterVoice
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedgan),
            caption=f"**✦┊تم اختياࢪ الاغنيـه لك 💞🎶**ٴ▁ ▂ ▉ ▄ ▅ ▆ ▇ ▅ ▆ ▇ █ ▉ ▂ ▁\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")
        

@zedub.zed_cmd(pattern="شعر$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الشعـر ...**")
    try:
        zedgan = [
            zlzzl77
            async for zlzzl77 in event.client.iter_messages(
                "@L1BBBL", filter=InputMessagesFilterVoice
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedgan),
            caption=f"**✦┊تم اختيـار مقطـع الشعـر هـذا لك**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="ميمز$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الميمـز ...**")
    try:
        zedgan = [
            zlzzl77
            async for zlzzl77 in event.client.iter_messages(
                "@MemzWaTaN", filter=InputMessagesFilterVoice
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedgan),
            caption=f"**✦┊تم اختيـار مقطـع الميمـز هـذا لك**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="ري اكشن$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل الرياكشـن ...**")
    try:
        zedre = [
            zlzz7
            async for zlzz7 in event.client.iter_messages(
                "@gafffg", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedre),
            caption=f"**🎆┊رياكشـن تحشيـش ➧🎃😹◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="معلومه$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ جـارِ تحميـل صـورة ومعلومـة ...**")
    try:
        zedph = [
            zilzal
            async for zilzal in event.client.iter_messages(
                "@A_l3l", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**🎆┊صـورة ومعلومـة ➧ 🛤💡◟**\n\n[➧??𝙤𝙪𝙧𝙘𝙚 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="تويت$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ كـت تـويت بالصـور ...**")
    try:
        zedre = [
            zlzz7
            async for zlzz7 in event.client.iter_messages(
                "@twit_selva", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedre),
            caption=f"**✦┊كـت تـويت بالصـور ➧⁉️🌉◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عـذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="خيرني$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮•⎚ لـو خيـروك بالصـور ...**")
    try:
        zedph = [
            zelzal
            async for zelzal in event.client.iter_messages(
                "@SourceSaidi", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**✦┊لـو خيـروك  ➧⁉️🌉◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عـذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="ولد انمي$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮ - جـارِ تحميـل الآفتـار ...𓅫╰**")
    try:
        zedph = [
            zelzal
            async for zelzal in event.client.iter_messages(
                "@dnndxn", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**◞افتـارات آنمي شبـاب ➧🎆🙋🏻‍♂◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عـذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="بنت انمي$")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮ - جـارِ تحميـل الآفتـار ...𓅫╰**")
    try:
        zedph = [
            zelzal
            async for zelzal in event.client.iter_messages(
                "@shhdhn", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**◞افتـارات آنمي بنـات ➧🎆🧚🏻‍♀◟**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عـذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


@zedub.zed_cmd(pattern="$صورة تمبلر")
async def _(event):
    zzevent = await edit_or_reply(event, "**╮ - جـارِ العثـور علـى صـور تمبلـر انتظـر ..**")
    try:
        zedph = [
            zelzal
            async for zelzal in event.client.iter_messages(
                "@N1NNNN", filter=InputMessagesFilterPhotos
            )
        ]
        aing = await event.client.get_me()
        await event.client.send_file(
            event.chat_id,
            file=random.choice(zedph),
            caption=f"**◞صور تمبلـر ✨**\n\n[➧𝙎𝙊𝙐𝙍𝘾𝙀 Smart Guard](https://t.me/SI0lZ)",
        )
        await zzevent.delete()
    except Exception:
        await zzevent.edit("**╮•⎚ عـذرًا .. لـم استطـع ايجـاد المطلـوب ☹️💔**")


