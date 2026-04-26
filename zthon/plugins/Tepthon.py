import json

import math

import os

import random

import re

import time

from pathlib import Path

from uuid import uuid4



from telethon import Button, types

from telethon.errors import QueryIdInvalidError

from telethon.events import CallbackQuery, InlineQuery

from zthon import zedub



from ..Config import Config

from ..helpers.functions import rand_key

from ..helpers.functions.utube import (

    download_button,

    get_yt_video_id,

    get_ytthumb,

    youtube_inline_search_formatted,

    ytsearch_data,

)

from ..sql_helper.globals import gvarstatus

from ..core.logger import logging



LOGS = logging.getLogger(__name__)



BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")

MEDIA_PATH_REGEX = re.compile(r"(:?\<\bmedia:(:?(?:.*?)+)\>)")

tr = Config.COMMAND_HAND_LER





def get_thumb(name):

    url = f"https://github.com/TgCatUB/CatUserbot-Resources/blob/master/Resources/Inline/{name}?raw=true"

    return types.InputWebDocument(url=url, size=0, mime_type="image/png", attributes=[])





def ibuild_keyboard(buttons):

    keyb = []

    for btn in buttons:

        if btn[2] and keyb:

            keyb[-1].append(Button.url(btn[0], btn[1]))

        else:

            keyb.append([Button.url(btn[0], btn[1])])

    return keyb







@zedub.tgbot.on(InlineQuery)

async def inline_handler(event):  # sourcery no-metrics

    builder = event.builder

    result = None

    query = event.text

    string = query.lower()

    query.split(" ", 2)

    str_y = query.split(" ", 1)

    string.split()

    query_user_id = event.query.user_id

    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:

        if str_y[0].lower() == "ytdl" and len(str_y) == 2:

            link = get_yt_video_id(str_y[1].strip())

            found_ = True

            if link is None:

                outdata = await youtube_inline_search_formatted(str_y[1].strip(), 15)

                if not outdata:

                    found_ = False

                else:

                    key_ = rand_key()

                    ytsearch_data.store_(key_, outdata)

                    buttons = [

                        Button.inline(

                            f"1 / {len(outdata)}",

                            data=f"ytdl_next_{key_}_1",

                        ),

                        Button.inline(

                            "القائمـة 📜",

                            data=f"ytdl_listall_{key_}_1",

                        ),

                        Button.inline(

                            "⬇️  تحميـل",

                            data=f'ytdl_download_{outdata[1]["video_id"]}_0',

                        ),

                    ]

                    caption = outdata[1]["message"]

                    photo = await get_ytthumb(outdata[1]["video_id"])

            else:

                caption, buttons = await download_button(link, body=True)

                photo = await get_ytthumb(link)

            if found_:

                markup = event.client.build_reply_markup(buttons)

                photo = types.InputWebDocument(

                    url=photo, size=0, mime_type="image/jpeg", attributes=[]

                )

                text, msg_entities = await event.client._parse_message_text(

                    caption, "html"

                )

                result = types.InputBotInlineResult(

                    id=str(uuid4()),

                    type="photo",

                    title=link,

                    description="⬇️ اضغـط للتحميـل",

                    thumb=photo,

                    content=photo,

                    send_message=types.InputBotInlineMessageMediaAuto(

                        reply_markup=markup, message=text, entities=msg_entities

                    ),

                )

            else:

                result = builder.article(

                    title="Not Found",

                    text=f"No Results found for `{str_y[1]}`",

                    description="INVALID",

                )

            try:

                await event.answer([result] if result else None)

            except QueryIdInvalidError:

                await event.answer(

                    [

                        builder.article(

                            title="Not Found",

                            text=f"No Results found for `{str_y[1]}`",

                            description="INVALID",

                        )

                    ]

                )

        elif string == "pmpermit":

            buttons = [

                Button.inline(text="عـرض الخيـارات", data="show_pmpermit_options"),

            ]

            PM_PIC = gvarstatus("pmpermit_pic")

            if PM_PIC:

                CAT = [x for x in PM_PIC.split()]

                PIC = list(CAT)

                CAT_IMG = random.choice(PIC)

            else:

                CAT_IMG = None

            query = gvarstatus("pmpermit_text")

            if CAT_IMG and CAT_IMG.endswith((".jpg", ".jpeg", ".png")):

                result = builder.photo(

                    CAT_IMG,

                    # title="Alive zed",

                    text=query,

                    buttons=buttons,

                )

            elif CAT_IMG:

                result = builder.document(

                    CAT_IMG,

                    title="Alive cat",

                    text=query,

                    buttons=buttons,

                )

            else:

                result = builder.article(

                    title="Alive cat",

                    text=query,

                    buttons=buttons,

                )

            await event.answer([result] if result else None)

    else:

        buttons = [

            (

                Button.url("قنـاة السـورس", "https://t.me/SI0lZ"),

                Button.url(

                    "مطـور السـورس",

                    "https://t.me/Sl0IZ",

                ),

            )

        ]

        markup = event.client.build_reply_markup(buttons)

        photo = types.InputWebDocument(

            url=ZEDLOGO, size=0, mime_type="image/jpeg", attributes=[]

        )

        text, msg_entities = await event.client._parse_message_text(

            "𝗗𝗲𝗽𝗹𝗼𝘆 𝘆𝗼𝘂𝗿 𝗼𝘄𝗻 [Smart Guard](https://t.me/SI0lZ) | الحارس الذكي.", "md"

        )

        result = types.InputBotInlineResult(

            id=str(uuid4()),

            type="photo",

            title="[Smart Guard](https://t.me/SI0lZ) | الحارس الذكي 𓅛",

            description="روابـط التنصـيب",

            url="https://t.me/SI0lZ/2",

            thumb=photo,

            content=photo,

            send_message=types.InputBotInlineMessageMediaAuto(

                reply_markup=markup, message=text, entities=msg_entities

            ),

        )

        await event.answer([result] if result else None)