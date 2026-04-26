# Zed-Thon

# Copyright (C) 2022 Zed-Thon . All Rights Reserved

#

# This file is a part of < https://github.com/Zed-Thon/ZelZal/ >

# PLease read the GNU Affero General Public License in

# <https://www.github.com/Zed-Thon/ZelZal/blob/zthon/LICENSE/>.

#يبووووووووووووووووووو

#هههههههههههههههههههههههههههههههههههههه

import os

import re

import telethon

from telethon.events import CallbackQuery, InlineQuery

from telethon import Button, events, functions

from telethon.tl import functions, types

from telethon.errors.rpcerrorlist import UserNotParticipantError

from telethon.tl.functions.channels import EditBannedRequest, GetFullChannelRequest, GetParticipantRequest

from telethon.tl.functions.messages import ExportChatInviteRequest

from telethon.tl.functions.users import GetFullUserRequest

from telethon.tl.types import ChatBannedRights



from ..sql_helper.fsub_sql import *

from zthon import zedub

from . import BOTLOG, BOTLOG_CHATID, admin_groups, get_user_from_event



# =========================================================== #

#                                                  الملـــف كتـــابـــة  - T.me/ZThon                                    #

# =========================================================== #

Warn = "تخمـط بـدون ذكـر المصـدر - راح توثقهـا فضيحـه ع نفسـك"

# =========================================================== #

#                                                       زلـــزال الهيبـــه - T.me/zzzzl1l                                  #

# =========================================================== #

#                                              تـاريـخ كتابـة الملـف - 30 اكتوبر/2022                                  #

#                                                   الملف كان مدفوع وتم تنزيله مجاني                                   #

#                                                  الدليل https://t.me/ZThon/260                                 #

# =========================================================== #



zilzal = zedub.uid

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

ANTI_DDDD_ZEDTHON_MODE = ChatBannedRights(

    until_date=None, view_messages=None, send_messages=True, send_media=True, send_stickers=True, send_gifs=True

)



async def is_admin(event, user):

    try:

        sed = await event.client.get_permissions(event.chat_id, user)

        if sed.is_admin:

            is_mod = True

        else:

            is_mod = False

    except:

        is_mod = False

    return is_mod





async def check_him(channel, user):

    try:

        result = await bot(

            functions.channels.GetParticipantRequest(channel, user)

        )

        return True

    except telethon.errors.rpcerrorlist.UserNotParticipantError:

        return False





async def rights(event):

    result = await bot(

        functions.channels.GetParticipantRequest(

            channel=event.chat_id,

            user_id=zilzal,

        )

    )

    p = result.participant

    return isinstance(p, types.ChannelParticipantCreator) or (

        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.ban_users

    )





@zedub.zed_cmd(pattern="(ضع اشتراك الكروب|وضع اشتراك الكروب) ?(.*)")

async def fs(event):

    permissions = await bot.get_permissions(event.chat_id, event.sender_id)

    if not permissions.is_admin:

        return await event.reply(

            "**⌔╎عـذرًا .. عـزيـزي\n**⌔╎لا أمـلك صلاحيات المشـرف هنـا**"

        )

    if not await is_admin(event, zilzal):

        return await event.reply("**⌔╎عـذرًا .. عـزيـزي\n**⌔╎لا أمـلك صلاحيات المشـرف هنـا**")

    if event.is_private:

        await edit_or_reply(event, "**✾╎عـذرًا .. هـذا الامـر خـاص بالمجمـوعـات فقـط**")

        return

    ahmed = event.pattern_match.group(1)

    if not ahmed:

        return await edit_delete(event, "**✾╎استخـدم الامـر هكـذا**\n**✾╎.اشتراك الكروب + معـرف القنـاة**")

    args = event.pattern_match.group(2)

    channel = args.replace("@", "")

    if args == "تفعيل" or args == "تشغيل":

        return await event.reply("**⌔╎عـذرًا .. يرجى التحقق من معـرف القنـاة**")

    if args in ("off", "تعطيل", "ايقاف"):

        rm_fsub(event.chat_id)

        await event.reply("**✾╎تـم إيقـاف الاشتـراك الإجبـاري هنـا .. بنجـاح ✓**")

    else:

        try:

            ch_full = await bot(GetFullChannelRequest(channel=channel))

        except Exception as e:

            await event.reply(f"{e}")

            return await event.reply("**⌔╎عـذرًا .. معـرف القنـاة غيـر موجـود**")

        rip = await check_him(channel, zilzal)

        if rip is False:

            return await event.reply(

                f"**⌔╎عـذرًا .. عـزيـزي**\n**⌔╎لـ تمكين الاشتـراك الإجبـاري**\n**⌔╎يجب أن تـكون مشرفًا في** [القنـاة](https://t.me/{args}).",

                link_preview=False,

            )

        add_fsub(event.chat_id, str(channel))

        await event.reply(f"**✾╎تم تفعيل الاشتراك الاجباري .. بنجاح ☑️**\n**✾╎قناة الاشتراك ~** @{channel}.")





@zedub.on(events.NewMessage(pattern=None))

async def f(event):

    chat_id = event.chat_id

    chat_db = is_fsub(event.chat_id)

    event.sender_id

    user = await event.get_sender()

    zed_dev = (5658302963, 9256472505)

    zelzal = event.sender_id

    if isinstance(user, telethon.types.User) and user.bot:

        return

    if zelzal in zed_dev:

        return

    if not await is_admin(event, zilzal):

        return

    if not chat_db:

        return

    if chat_db:

        try:

            channel = chat_db.channel

            chat_id = event.chat_id

            chat_db = is_fsub(event.chat_id)

            channel = chat_db.channel

            user = await event.get_sender()

            grp = f"t.me/{channel}"

            rip = await check_him(channel, event.sender_id)

            if rip is False:

                await bot.send_message(

                    event.chat_id, f"[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗣𝗢𝗪𝗘𝗥𝗧𝗛𝗢𝗡 - الاشتࢪاك الإجباࢪي](t.me/Power_Thon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎**مࢪحـبًا عـزيـزي 👋** [{user.first_name}](tg://user?id={user.id}) \n⌔╎**لـ إلغـاء كتمـك 🔊**\n⌔╎**يُࢪجـى الإشتـࢪاك بالقنـاة @{channel} **", link_preview=False

                )

                await event.delete()

        except:

            if not await rights(event):

                await bot.send_message(

                    event.chat_id,

                    "**⌔╎عـذرًا .. عـزيـزي\n**⌔╎لا أمـلك صلاحيات المشـرف هنـا**",

                )





@zedub.zed_cmd(pattern="تعطيل اشتراك الكروب$")

async def removef(event):

    if is_fsub(event.chat_id):

        rm_fsub(event.chat_id)

        await edit_or_reply(event, "**✾╎تـم إيقـاف الاشتـراك الإجبـاري هنـا .. بنجـاح ✓**")

    else:

        return await edit_delete(event, "**✾╎عـذرًا .. الاشتـراك الإجبـاري غيـر مفعـل هنـا**")

    #شـكرًا زلـزال الهـيـبـة .