from asyncio import sleep

from telethon import events
from telethon.utils import get_display_name

from zthon import zedub

from ..core.managers import edit_or_reply
from ..sql_helper import pmpermit_sql as pmpermit_sql
from ..sql_helper.welcomesql import (
    addwelcome_setting,
    getcurrent_welcome_settings,
    rmwelcome_setting,
)
from . import BOTLOG_CHATID

plugin_category = "الترفيه"


@zedub.on(events.ChatAction)
async def _(event):  # sourcery no-metrics
    cws = getcurrent_welcome_settings(event.chat_id)
    if (
        cws
        and (event.user_joined or event.user_added)
        and not (await event.get_user()).bot
    ):
        a_user = await event.get_user()
        chat = await event.get_chat()
        me = await event.client.get_me()
        title = get_display_name(await event.get_chat()) or "لهـذه الدردشـه"
        participants = await event.client.get_participants(chat)
        count = len(participants)
        mention = "<a href='tg://user?id={}'>{}</a>".format(
            a_user.id, a_user.first_name
        )
        my_mention = "<a href='tg://user?id={}'>{}</a>".format(me.id, me.first_name)
        first = a_user.first_name
        last = a_user.last_name
        fullname = f"{first} {last}" if last else first
        username = f"@{a_user.username}" if a_user.username else mention
        userid = a_user.id
        my_first = me.first_name
        my_last = me.last_name
        my_fullname = f"{my_first} {my_last}" if my_last else my_first
        my_username = f"@{me.username}" if me.username else my_mention
        file_media = None
        current_saved_welcome_message = None
        if cws:
            if cws.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
                )
                file_media = msg_o.media
                current_saved_welcome_message = msg_o.message
                link_preview = True
            elif cws.reply:
                current_saved_welcome_message = cws.reply
                link_preview = False
        if not pmpermit_sql.is_approved(userid):
            pmpermit_sql.approve(userid, "Due to private welcome")
        await sleep(1)
        current_message = await event.client.send_message(
            userid,
            current_saved_welcome_message.format(
                mention=mention,
                title=title,
                count=count,
                first=first,
                last=last,
                fullname=fullname,
                username=username,
                userid=userid,
                my_first=my_first,
                my_last=my_last,
                my_fullname=my_fullname,
                my_username=my_username,
                my_mention=my_mention,
            ),
            file=file_media,
            parse_mode="html",
            link_preview=link_preview,
        )


@zedub.zed_cmd(
    pattern=r"رحب(?:\s|$)([\s\S]*)",
    command=("رحب", plugin_category),
    info={
        "header": "To welcome user(sends welcome message to here private messages).",
        "description": "Saves the message as a welcome note in the chat. And will send welcome message to every new user who ever joins newly in group.",
        "option": {
            "{mention}": "To mention the user",
            "{title}": "To get chat name in message",
            "{count}": "To get group members",
            "{first}": "To use user first name",
            "{last}": "To use user last name",
            "{fullname}": "To use user full name",
            "{userid}": "To use userid",
            "{username}": "To use user username",
            "{my_first}": "To use my first name",
            "{my_fullname}": "To use my full name",
            "{my_last}": "To use my last name",
            "{my_mention}": "To mention myself",
            "{my_username}": "To use my username.",
        },
        "usage": [
            "{tr}savepwel <welcome message>",
            "reply {tr}savepwel to text message or supported media with text as media caption",
        ],
        "examples": "{tr}savepwel Hi {mention}, Welcome to {title} chat",
    },
)
async def save_welcome(event):
    "To set private welcome message."
    msg = await event.get_reply_message()
    string = "".join(event.text.split(maxsplit=1)[1:])
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#ترحـيب الخاص\
                \n**- ايـدي الدردشـة :** {event.chat_id}\
                \nThe following message is saved as the welcome note for the {get_display_name(await event.get_chat())}, Dont delete this message !!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "**⪼ الميديا المعطاه تم حفظها كترحيب خاص لـ BOTLOG_CHATID  ء𓆰**",
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "**⪼ تـرحيب الخـاص {}  بنجـاح .. في هذه الدردشـه 𓆰**"
    if addwelcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تم حفظـه"))
    rmwelcome_setting(event.chat_id)
    if addwelcome_setting(event.chat_id, 0, string, msg_id) is True:
        return await edit_or_reply(event, success.format("تم تحديثـه"))
    await edit_or_reply("**- خطأ .. لا يسمح بوضع ترحيب خـاص بهذه الدردشـه**")


@zedub.zed_cmd(
    pattern="حذف رحب$",
    command=("حذف رحب", plugin_category),
    info={
        "header": "To turn off private welcome message.",
        "description": "Deletes the private welcome note for the current chat.",
        "usage": "{tr}clearpwel",
    },
)
async def del_welcome(event):
    "To turn off private welcome message"
    if rmwelcome_setting(event.chat_id) is True:
        await edit_or_reply(event, "**⪼ تم حذف تـرحيب الخـاص في هذه الدردشـه 𓆰**")
    else:
        await edit_or_reply(event, "**⪼ انت لا تمتلك تـرحيب الخـاص لــ هذه الدردشـه 𓆰**")


@zedub.zed_cmd(
    pattern="قائمه رحب$",
    command=("قائمه رحب", plugin_category),
    info={
        "header": "To check current private welcome message in group.",
        "usage": "{tr}listpwel",
    },
)
async def show_welcome(event):
    "To show current private welcome message in group"
    cws = getcurrent_welcome_settings(event.chat_id)
    if not cws:
        await edit_or_reply(event, "**⪼ لا يوجد ترحـيب خاص بهـذه الدردشـه 𓆰**")
        return
    if cws.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(cws.f_mesg_id)
        )
        await edit_or_reply(
            event, "**⪼ انا ارحب بالاعضاء الجدد في هذه الدردشه بالخاص باستخدام هذا الترحيب 𓆰**"
        )
        await event.reply(msg_o.message, file=msg_o.media)
    elif cws.reply:
        await edit_or_reply(
            event, "**⪼ انا ارحب بالاعضاء الجدد في هذه الدردشه بالخاص باستخدام هذا الترحيب 𓆰**"
        )
        await event.reply(cws.reply, link_preview=False)
