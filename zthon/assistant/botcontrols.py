import asyncio
from datetime import datetime

from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError

from zthon import zedub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id, time_formatter
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list, get_all_bl_users
from ..sql_helper.bot_starters import del_starter_from_db, get_all_starters
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import (
    ban_user_from_bot,
    get_user_and_reason,
    progress_str,
    unban_user_from_bot,
)

LOGS = logging.getLogger(__name__)

plugin_category = "البوت"
botusername = Config.TG_BOT_USERNAME
cmhd = Config.COMMAND_HAND_LER


@zedub.bot_cmd(pattern="^/help$", from_users=Config.OWNER_ID)
async def bot_help(event):
    await event.reply(
        f"""**- اوامـر البـوت المسـاعـد 🤖♥️**:
**ملاحظة : **__تعمـل هذه الأوامـر فقـط بخـاص البـوت__ {botusername}

• **الامـر : ** /uinfo <بالـرد ع رسـالة الشخـص>
• **الوصـف : **__لقد لاحظت أن الملصقات / الرموز التعبيرية المُعاد توجيهها لا تحتوي على علامة إعادة توجيه حتى تتمكن من تحديد المستخدم الذي أرسل تلك الرسائل بواسطة الامـر.__
• **ملاحظـه : **__يعمل لجميع الرسائل المعاد توجيهها. حتى بالنسبة للمستخدمين الذين يسمح لهم بإعادة توجيه الرسالة ، لا أحد.__

• **الامـر : ** /ban <السبب> او /ban <المعرف/الايدي> <السبب>
• **الوصـف : **__الرد على رسالة المستخدم مع ذكر السبب حتى يتم إعلامه لأنك حظرت من البـوت ولن يتم إرسال رسائله إليك بعد ذلك.__
• **ملاحظـه : **__السبب لا بد منه. بدون سبب لن يعمل. __

• **الامـر : ** /unban <السبب (اختياري)> او /unban <المعـرف/الايـدي>
• **الوصـف : **__الرد على رسالة المستخدم أو باضافـة اسم المستخدم / معرف المستخدم للامـر لإلغاء الحظر من البوت.__
• **ملاحظـه : **__لعـرض قائمـه المحظـورين في البـوت__ `{cmhd}المحظورين`.

• **الامـر : ** /broadcast
• **الوصـف : **__قم بالرد على رسالة ليتم اذاعتها لكل مستخدم مشتـرك بالبـوت الخاص بك. للحصول على قائمـة المستخدمين استخدام__ `{cmhd}المشتركين`.
• **ملاحـظه : **__إذا قام المستخدم بحذف / حظر البـوت ، فسيتم إزالته من قاعدة البيانات الخاصة بك وسيتم مسحه من قائمة المشتـركـين.__
"""
    )


@zedub.bot_cmd(pattern="^/broadcast$", from_users=Config.OWNER_ID)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("**- بالـرد ع رسـالة للاذاعـة**")
    start_ = datetime.now()
    br_cast = await replied.reply("**جـاري الاذاعـه ...**")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply("**- لايـوجد مستخدمين بعـد بـ البـوت الخـاص بك**")
    users = get_all_starters()
    if users is None:
        return await event.reply("**- حدثت أخطـاء أثنـاء جلب قائمـة المستخـدمين.**")
    for user in users:
        try:
            await event.client.send_message(
                int(user.user_id), "**- تم الاذاعـه لجميـع مشتركيـن البـوت .. بنجـاح 🔊✓**"
            )
            await event.client.send_message(int(user.user_id), replied)
            await asyncio.sleep(0.8)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**خطـأ بالإذاعة**\n`{e}`"
                )

        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        "**🔊 جـاري الاذاعـه لمستخدمين البـوت ...**\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• ✔️ **تم بنجـاح** :  `{count}`\n"
                        + f"• ✖️ **خطـأ باذاعـة** :  `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
    end_ = datetime.now()
    b_info = f"**🔊  تمت الاذاعـه بنجـاح لـ ➜**  <b>{count} شخـص.</b>"
    if blocked_users:
        b_info += f"\n <b>- المحظـوريـن 🚫 : {len(blocked_users)} مشتـرك </b> تم حظـرهم من البـوت المسـاعد مؤخـراً .. لذلك تم استبعـادهم 🚯"
    b_info += (
        f"\n⏳  <code>- جـارِ : {time_formatter((end_ - start_).seconds)}</code>."
    )
    await br_cast.edit(b_info, parse_mode="html")


@zedub.zed_cmd(
    pattern="المشتركين$",
    command=("المشتركين", plugin_category),
    info={
        "header": "لـ جلب قائمـة بالاعضـاء المشتـركيـن في البـوت السـاعد الخـاص بك",
        "الاسـتخـدام": "{tr}المشتركين",
    },
)
async def ban_starters(event):
    "لـ جلب قائمـة بالاعضـاء المشتـركيـن في البـوت السـاعد الخـاص بك"
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edit_delete(event, "**- لايــوجد مشتـركين بالبـوت بعـد**")
    msg = "**- قـائمـة مشتـركيـن البـوت المسـاعـد الخـاص بـك :\n\n**"
    for user in ulist:
        msg += f"**• المستخـدم :**  {_format.mentionuser(user.first_name , user.user_id)}\n**• الايـدي :** `{user.user_id}`\n**• المعـرف :** @{user.username}\n**• البيـانات : **__{user.date}__\n\n"
    await edit_or_reply(event, msg)


@zedub.bot_cmd(pattern=r"^/ban\\s+([\\s\\S]*)", from_users=Config.OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "**- لـم استطـع العثـور علـى الشخـص**", reply_to=reply_to
        )
    if not reason:
        return await event.client.send_message(
            event.chat_id, "**- لحظـر الشخـص اولا عليـك بذكـر السبب مـع الامـر**", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**- خطـأ :**\n`{e}`")
    if user_id == Config.OWNER_ID:
        return await event.reply("**- لايمكننـي حظـرك سيـدي ؟!**")
    if check := check_is_black_list(user.id):
        return await event.client.send_message(
            event.chat_id,
            f"#بالفعـل_محظـور\
            \nالشخـص بالفعـل موجود في قائمـة الحظـر.\
            \n**سبب الحظـر:** `{check.reason}`\
            \n**الوقت:** `{check.date}`.",
        )
    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@zedub.bot_cmd(pattern=r"^/unban(?:\\s|$)([\\s\\S]*)", from_users=Config.OWNER_ID)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "**- لـم استطـع العثـور علـى الشخـص**", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**- خطـأ :**\n`{e}`")
    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"#ليـس_محظـور\
            \n👤 {_format.mentionuser(user.first_name , user.id)} doesn't exist in my Banned Users list.",
        )
    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@zedub.zed_cmd(
    pattern="المحظورين$",
    command=("المحظورين", plugin_category),
    info={
        "header": "لـ جلب قائمـة بالمستخـدمين المحظـورين من بـوتك المسـاعـد",
        "الاسـتخـدام": "{tr}المحظورين",
    },
)
async def ban_starters(event):
    "لـ جلب قائمـة بالمستخـدمين المحظـورين من بـوتك المسـاعـد"
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edit_delete(event, "**- لـم تقـم بحظـر احـد بعـد**")
    msg = "**- قـائمـة محظـورين البـوت المسـاعـد الخـاص بـك :\n\n**"
    for user in ulist:
        msg += f"**• المستخـدم :**  {_format.mentionuser(user.first_name , user.chat_id)}\n**• الايـدي :** `{user.chat_id}`\n**• المعـرف :** @{user.username}\n**• البيـانات : **__{user.date}__\n**• السبب :** __{user.reason}__\n\n"
    await edit_or_reply(event, msg)


@zedub.zed_cmd(
    pattern="عدم التكرار (تفعيل|تعطيل)$",
    command=("bot_antif", plugin_category),
    info={
        "header": "لـ تفعيل / تعطيل مكافح التكرار لمستخدمين البوت الخاص بك",
        "الوصـف": "if it was turned on then after 10 messages or 10 edits of same messages in less time then your bot auto loacks them.",
        "الاسـتخـدام": [
            "{tr}عدم التكرار تفعيل",
            "{tr}عدم التكرار تعطيل",
        ],
    },
)
async def ban_antiflood(event):
    "لـ تفعيل / تعطيل مكافح التكرار لمستخدمين البوت الخاص بك"
    input_str = event.pattern_match.group(1)
    if input_str == "تفعيل":
        if gvarstatus("bot_antif") is not None:
            return await edit_delete(event, "**- وضـع عـدم التكـرار مفعـل مسبقـاً**")
        addgvar("bot_antif", True)
        await edit_delete(event, "**- تـم تفعيـل وضـع عـدم التكـرار . . بنجـاح ✓**")
    elif input_str == "تعطيل":
        if gvarstatus("bot_antif") is None:
            return await edit_delete(event, "**- وضـع عـدم التكـرار معطـل مسبقـاً**")
        delgvar("bot_antif")
        await edit_delete(event, "**- تـم تعطيـل وضـع عـدم التكـرار . . بنجـاح ✓**")
