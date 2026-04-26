# Zed-Thon
# Copyright (C) 2022 Zed-Thon . All Rights Reserved
#
# This file is a part of < https://github.com/Zed-Thon/ZelZal/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Zed-Thon/ZelZal/blob/master/LICENSE/>.

""" وصـف الملـف : اوامـر اضـافة الفـارات باللغـة العربيـة كـاملة ولا حـرف انكلـش🤘 تخمـط اذكـر المصـدر يولـد
اضـافة فـارات صـورة ( الحمايـة - الفحـص - الوقتـي ) بـ امـر واحـد فقـط
حقـوق للتـاريخ : @Zthon
@zzzzl1l - كتـابـة الملـف :  زلــزال الهيبــه"""
#زلـزال_الهيبـه يولـد هههههههههههههههههههههههههه
import asyncio
import math
import os

import heroku3
import requests
import urllib3
import random
import string
from datetime import datetime

from PIL import Image
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_display_name
from urlextract import URLExtract

from zthon import zedub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
from . import BOTLOG_CHATID, mention


plugin_category = "الادوات"
LOGS = logging.getLogger(__name__)

extractor = URLExtract()
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


ZelzalVP_cmd = (
    "𓆩 [Smart Guard 𝗖𝗼𝗻𝗳𝗶𝗴 𝗩𝗮𝗿𝘀 - اوامـر الفـارات](t.me/SI0lZ) 𓆪\n\n"
    "**❈╎قائـمه اوامر تغييـر فـارات الصـور بأمـر واحـد فقـط - لـ أول مـرة ع سـورس تليثـون يوزر بـوت 🦾 :** \n\n"
    "⪼ `.اضف صورة الحماية` بالـرد ع صـورة او ميديـا\n\n"
    "⪼ `.اضف صورة الفحص` بالـرد ع صـورة او ميديـا\n\n"
    "⪼ `.اضف صورة الوقتي` بالـرد ع صـورة او ميديـا\n\n"
    "⪼ `.اضف صورة الاوامر` بالـرد ع صـورة او ميديـا\n\n"
    "⪼ `.اضف صورة السورس` بالـرد ع صـورة او ميديـا\n\n"
    "⪼ `.اضف صورة الكتم` بالـرد ع صـورة او ميديـا\n\n"
    "⪼ `.اضف صورة البوت` بالـرد ع صـورة او ميديـا لـ اضـافة صـورة ستـارت للبـوت\n\n"
    "⪼ `.اوامر الفارات` لعـرض بقيـة اوامـر الفـارات\n\n\n"
    "**❈╎قائـمه اوامر تغييـر كليشـة الايـدي :** \n\n"
    "⪼ `.اضف ايموجي الايدي` بالـرد ع الرمـز او الايموجـي\n\n"
    "⪼ `.اضف عنوان الايدي` بالـرد ع نـص العنـوان\n\n"
    "⪼ `.اضف خط الايدي` بالـرد ع الخـط او المستقيـم\n\n\n"
    "**❈╎قائـمه اوامر تغييـر بقيـة الفـارات بأمـر واحـد فقـط :** \n\n"
    "⪼ `.اضف كليشة الحماية` بالـرد ع الكليشـة\n\n"
    "⪼ `.اضف كليشة الفحص` بالـرد ع الكليشـة\n\n"
    "⪼ `.اضف كليشة الحظر` بالـرد ع الكليشـة\n\n"
    "⪼ `.اضف كليشة البوت` بالـرد ع الكليشـة لـ اضـافة كليشـة ستـارت\n\n"
    "⪼ `.اضف رمز الوقتي` بالـرد ع رمـز\n\n"
    "⪼ `.اضف زخرفة الوقتي` بالـرد ع ارقـام الزغـرفه\n\n"
    "⪼ `.اضف البايو الوقتي` بالـرد ع البـايـو\n\n"
    "⪼ `.اضف اسم المستخدم` بالـرد ع اسـم\n\n"
    "⪼ `.اضف كروب الرسائل` بالـرد ع ايدي الكـروب\n\n"
    "⪼ `.اضف كروب السجل` بالـرد ع ايدي الكـروب\n\n"
    "⪼ `.اضف ايديي` بالـرد ع ايدي حسـابك\n\n"
    "⪼ `.اضف نقطة الاوامر` بالـرد ع الـرمز الجديـد\n\n"
    "⪼ `.اضف نوم الترحيب` بالـرد ع رقـم الساعة لبداية نوم الترحيب المؤقت\n\n"
    "⪼ `.اضف رسائل الحماية` بالـرد ع رقـم لعدد رسائل تحذيـرات حماية الخاص\n\n\n"
    "⪼ `.جلب` + اسـم الفـار\n\n"
    "⪼ `.حذف` + اسـم الفـار\n\n"
    "⪼ `.رفع مطور` بالـرد ع الشخـص لرفعـه مطـور تحكـم كامـل بالاوامـر\n\n"
    "⪼ `.حذف المطورين`\n\n"
    "**❈╎قائـمه اوامر تغييـر المنطقـة الزمنيـة للوقـت 🌐:** \n\n"
    "⪼ `.وقت العراق` \n\n"
    "⪼ `.وقت مصر` \n\n"
    "⪼ `.وقت الامارات` \n\n"
    "⪼ `.وقت ايران` \n\n"
    "⪼ `.وقت الجزائر` \n\n"
    "⪼ `.وقت المغرب` \n\n"
    "⪼ `.وقت تركيا` \n\n"
    "🛃 سيتـم اضـافة المزيـد من الدول قريبـاً\n\n"
    "\n𓆩 [ 𝙑𝙖𝙧𝙨 - قنـاة الفـارات](t.me/Power_Thone1) 𓆪"
)


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern=r"اضف (.*)")
async def variable(event):
    input_str = event.pattern_match.group(1)
    if input_str.startswith("نشر"):
        return
    reply = await event.get_reply_message()
    if not reply:
        return await edit_or_reply(event, "**❈╎عـذࢪاً .. يجب الرد على النص أو الصورة أولاً!**")
    vinfo = getattr(reply, "text", "")
    zed = await edit_or_reply(event, "**❈╎جـاري اضـافة الفـار الـى بـوتك ...**")
    # All Rights Reserved for "Zed-Thon" "زلـزال الهيبـه"
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        variable = "ALIVE_TEMPLATE"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_TEMPLATE") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎الكليشـة الجـديده** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم إضـافـة {} بنجـاح ☑️**\n**❈╎الكليشـة المضـافه** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.فحص` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("ALIVE_TEMPLATE", vinfo)
    elif input_str == "كليشة الحماية" or input_str == "كليشه الحمايه" or input_str == "كليشه الحماية" or input_str == "كليشة الحمايه":
        variable = "pmpermit_txt"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_txt") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎الكليشـة الجـديده** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم إضـافـة {} بنجـاح ☑️**\n**❈╎الكليشـة المضـافه** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.الحمايه تفعيل` **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("pmpermit_txt", vinfo)
    elif input_str == "كليشة البوت" or input_str == "كليشه البوت":
        variable = "START_TEXT"
        await asyncio.sleep(1.5)
        if gvarstatus("START_TEXT") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎الكليشـة الجـديده** \n {} \n\n**❈╎الآن قـم بـ الذهـاب لبوتك المسـاعد من حساب آخر ↶** ودز ستارت **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم إضـافـة {} بنجـاح ☑️**\n**❈╎الكليشـة المضـافه** \n {} \n\n**❈╎الآن قـم بـ الذهـاب لبوتك المسـاعد من حساب آخر ↶** ودز ستارت **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("START_TEXT", vinfo)
    elif input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        variable = "pmblock"
        await asyncio.sleep(1.5)
        if gvarstatus("pmblock") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎الكليشـة الجـديده** \n {} \n\n**❈╎الآن قـم بـ الذهـاب لبوتك المسـاعد من حساب آخر ↶** ودز ستارت **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم إضـافـة {} بنجـاح ☑️**\n**❈╎الكليشـة المضـافه** \n {} \n\n**❈╎الآن قـم بـ الذهـاب لبوتك المسـاعد من حساب آخر ↶** ودز ستارت **لـ التحقـق مـن الكليشـة . .**".format(input_str, vinfo))
        addgvar("pmblock", vinfo)
    elif input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = "CUSTOM_ALIVE_EMZED"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_EMZED") is None:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎الـرمـز الجـديـد** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.الاسم تلقائي` **لـ التحقـق مـن الـرمز . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم إضـافـة {} بنجـاح ☑️**\n**❈╎الـرمـز المضـاف** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.الاسم تلقائي` **لـ التحقـق مـن الـرمز . .**".format(input_str, vinfo))
    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه" or input_str == "البايو تلقائي":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_BIO") is None:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎البـايـو الجـديـد** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.البايو تلقائي` **لـ التحقـق مـن البايـو . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم اضـافه {} بنجـاح ☑️**\n**❈╎البـايـو المضـاف** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.البايو تلقائي` **لـ التحقـق مـن البايـو . .**".format(input_str, vinfo))
    elif input_str == "التحقق" or input_str == "كود التحقق" or input_str == "التحقق بخطوتين" or input_str == "تحقق":
        variable = "TG_2STEP_VERIFICATION_CODE"
        await asyncio.sleep(1.5)
        if gvarstatus("TG_2STEP_VERIFICATION_CODE") is None:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم إضافـة {} بنجـاح ☑️**\n**❈╎كـود التحـقق بخطـوتيـن** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.تحويل ملكية` **ثم معـرف الشخـص داخـل الكـروب او القنـاة . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم إضافـة {} بنجـاح ☑️**\n**❈╎كـود التحـقق بخطـوتيـن** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.تحويل ملكية` **ثم معـرف الشخـص داخـل الكـروب او القنـاة . .**".format(input_str, vinfo))
    elif input_str == "كاشف الاباحي" or input_str == "كشف الاباحي":
        variable = "DEEP_API"
        await asyncio.sleep(1.5)
        if gvarstatus("DEEP_API") is None:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم تغييـر توكـن {} بنجـاح ☑️**\n**❈╎التوكـن الجـديـد** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.قفل الاباحي` **لـ تفعيـل كاشـف الاباحي . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم إضافـة توكـن {} بنجـاح ☑️**\n**❈╎التوكـن المضـاف** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.قفل الاباحي` **لـ تفعيـل كاشـف الاباحي . .**".format(input_str, vinfo))
    elif input_str == "ايموجي الايدي" or input_str == "ايموجي ايدي" or input_str == "رمز الايدي" or input_str == "رمز ايدي" or input_str == "الرمز ايدي":
        variable = "CUSTOM_ALIVE_EMOJI"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_EMOJI") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.ايدي`".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.ايدي`".format(input_str, vinfo))
        addgvar("CUSTOM_ALIVE_EMOJI", vinfo)
    elif input_str == "عنوان الايدي" or input_str == "عنوان ايدي":
        variable = "CUSTOM_ALIVE_TEXT"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_TEXT") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.ايدي`".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.ايدي`".format(input_str, vinfo))
        addgvar("CUSTOM_ALIVE_TEXT", vinfo)
    elif input_str == "خط الايدي" or input_str == "خط ايدي" or input_str == "خطوط الايدي" or input_str == "خط ايدي":
        variable = "CUSTOM_ALIVE_FONT"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_FONT") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.ايدي`".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.ايدي`".format(input_str, vinfo))
        addgvar("CUSTOM_ALIVE_FONT", vinfo)
    elif input_str == "اشتراك الخاص" or input_str == "اشتراك خاص":
        variable = "Custom_Pm_Channel"
        await asyncio.sleep(1.5)
        if gvarstatus("Custom_Pm_Channel") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.اشتراك خاص`".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.اشتراك خاص`".format(input_str, vinfo))
        delgvar("Custom_Pm_Channel")
        addgvar("Custom_Pm_Channel", vinfo)
        if BOTLOG_CHATID:
                await event.client.send_message(
                BOTLOG_CHATID,
                f"#قنـاة_الاشتـراك_الاجبـاري_للخـاص\
                        \n**- القنـاة {input_str} تم اضافتهـا في قاعده البيانات ..بنجـاح ✓**",
            )
    elif input_str == "اشتراك كروب" or input_str == "اشتراك الكروب":
        variable = "Custom_G_Channel"
        await asyncio.sleep(1.5)
        if gvarstatus("Custom_G_Channel") is None:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.اشتراك كروب`".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n\n**❈╎المتغيـر : ↶**\n `{}`\n**❈╎ارسـل الآن** `.اشتراك كروب`".format(input_str, vinfo))
        delgvar("Custom_G_Channel")
        addgvar("Custom_G_Channel", vinfo)
        if BOTLOG_CHATID:
                await event.client.send_message(
                BOTLOG_CHATID,
                f"#قنـاة_الاشتـراك_الاجبـاري_للكـروب\
                        \n**- القنـاة {input_str} تم اضافتهـا في قاعده البيانات ..بنجـاح ✓**",
            )
    elif input_str == "زاجل" or input_str == "قائمة زاجل" or input_str == "قائمه زاجل" or input_str == "يوزرات":
        variable = "ZAGL_Zed"
        await asyncio.sleep(1.5)
        if gvarstatus("ZAGL_Zed") is None:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️**\n**❈╎اليـوزرات المضـافة** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.زاجل` **بالـرد ع نـص او ميديـا بنـص . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️**\n**❈╎اليـوزرات المضـافة** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.زاجل` **بالـرد ع نـص او ميديـا بنـص . .**".format(input_str, vinfo))
    elif input_str == "بوت التجميع" or input_str == "بوت النقاط" or input_str == "النجميع" or input_str == "النقاط":
        variable = "Z_Point"
        await asyncio.sleep(1.5)
        if gvarstatus("Z_Point") is None:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎البـوت المضـاف** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.تجميع` **لـ البـدء بتجميـع النقـاط من البـوت الجـديـد . .**".format(input_str, vinfo))
        else:
            addgvar(variable, vinfo)
            await zed.edit("**❈╎تم اضـافه {} بنجـاح ☑️**\n**❈╎البـوت المضـاف** \n {} \n\n**❈╎الآن قـم بـ ارسـال الامـر ↶** `.تجميع` **لـ البـدء بتجميـع النقـاط من البـوت الجـديـد . .**".format(input_str, vinfo))
    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "ALIVE_NAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo

    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص" or input_str == "عدد التحذيرات":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "✾╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "MAX_FLOOD_IN_PMS"
        await asyncio.sleep(1.5)
        if vinfo.isdigit():
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            return await zed.edit("**❈╎خطـأ .. قم بالـرد ع رقـم فقـط ؟!**")
        heroku_var[variable] = vinfo

    elif input_str == "كود تيرمكس" or input_str == "كود السيشن" or input_str == "كود سيشن":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "STRING_SESSION"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo

    elif input_str == "كروب الرسائل" or input_str == "كروب التخزين" or input_str == "كروب الخاص":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "السجل" or input_str == "كروب السجل":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "السجل 2" or input_str == "كروب السجل 2":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PRIVATE_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "قناة السجل" or input_str == "قناة السجلات":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PRIVATE_CHANNEL_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "قناة الملفات" or input_str == "قناة الاضافات":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "PLUGIN_CHANNEL"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "ايديي" or input_str == "ايدي الحساب":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "OWNER_ID"
        await asyncio.sleep(1.5)
        if vinfo.isdigit():
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            return await zed.edit("**❈╎خطـأ .. قم بالـرد ع رقـم فقـط ؟!**")
        heroku_var[variable] = vinfo
    elif input_str == "نقطة الاوامر" or input_str == "نقطه الاوامر":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "COMMAND_HAND_LER"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "التوكن" or input_str == "توكن البوت":
        variable = "TG_BOT_TOKEN"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "TG_BOT_USERNAME"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "الريبو" or input_str == "السورس":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "UPSTREAM_REPO"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "توكن المكافح" or input_str == "كود المكافح" or input_str == "مكافح التخريب" or input_str == "مكافح التفليش":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")

        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "SPAMWATCH_API"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "توكن الذكاء" or input_str == "مفتاح الذكاء" or input_str == "الذكاء":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "OPENAI_API_KEY"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            await zed.edit("**❈╎تم اضافـة {} بنجـاح ☑️** \n**❈╎المضاف اليه :**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        heroku_var[variable] = vinfo
    elif input_str == "ايقاف الترحيب" or input_str == "نوم الترحيب":
        variable = "TIME_STOP"
        await asyncio.sleep(1.5)
        if vinfo.isdigit():
            await zed.edit("**❈╎تم تغييـر {} بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, vinfo))
        else:
            return await zed.edit("**❈╎خطـأ .. قم بالـرد ع رقـم فقـط ؟!**")
        addgvar("TIME_STOP", vinfo)
        if BOTLOG_CHATID:
                await event.client.send_message(
                BOTLOG_CHATID,
                f"#فتـرة_الايقـاف_المـؤقت_للترحيب\
                        \n**- تم اضافة الفتـرة من الساعة {vinfo} الى الساعة 6 صباحـاً .. بنجـاح ✓**",
            )
    else:
        if input_str:
            return await zed.edit("**❈╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))

        return await edit_or_reply(event, "**❈╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))



# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern=r"حذف(?:\s|$)([\s\S]*)")
async def variable(event):
    input_str = event.text[5:]
    if input_str.startswith("نشر"):
        return
    if Config.HEROKU_API_KEY is None:
        return await ed(
            event,
            "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await ed(
            event,
            "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.",
        )
    input_str = event.text[5:]
    heroku_var = app.config()
    zed = await edit_or_reply(event, "**❈╎جـاري حـذف الفـار مـن بـوتك 🚮...**")
    # All Rights Reserved for "Zed-Thon" "زلـزال الهيبـه"
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        variable = gvarstatus("ALIVE_TEMPLATE")
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_TEMPLATE") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, variable))
        delgvar("ALIVE_TEMPLATE")
        
    elif input_str == "كليشة الحماية" or input_str == "كليشه الحمايه" or input_str == "كليشه الحماية" or input_str == "كليشة الحمايه":
        variable = gvarstatus("pmpermit_txt")
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_txt") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, variable))
        delgvar("pmpermit_txt")

    elif input_str == "كليشة البوت" or input_str == "كليشه البوت":
        variable = gvarstatus("START_TEXT")
        await asyncio.sleep(1.5)
        if gvarstatus("START_TEXT") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, variable))
        delgvar("START_TEXT")

    elif input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        variable = gvarstatus("pmblock")
        await asyncio.sleep(1.5)
        if gvarstatus("pmblock") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, variable))
        delgvar("pmblock")

    elif input_str == "صورة الفحص" or input_str == "صوره الفحص":
        variable = "ALIVE_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_PIC") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("ALIVE_PIC")

    elif input_str == "صورة الاوامر" or input_str == "صوره الاوامر":
        variable = "CMD_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("CMD_PIC") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("CMD_PIC")

    elif input_str == "صورة السورس" or input_str == "صوره السورس":
        variable = "ALIVE_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("ALIVE_PIC") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("ALIVE_PIC")

    elif input_str == "صورة الكتم" or input_str == "صوره الكتم":
        variable = "KTM_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("KTM_PIC") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("KTM_PIC")

    elif input_str == "صورة البوت" or input_str == "صوره البوت":
        variable = "BOT_START_PIC"
        await asyncio.sleep(1.5)
        if gvarstatus("BOT_START_PIC") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
        delgvar("BOT_START_PIC")

    elif input_str == "صورة الحماية" or input_str == "صوره الحمايه" or input_str == "صورة الحمايه" or input_str == "صوره الحماية":
        variable = "pmpermit_pic"
        await asyncio.sleep(1.5)
        if gvarstatus("pmpermit_pic") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        delgvar("pmpermit_pic")
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))

    elif input_str == "صورة الوقتي" or input_str == "صوره الوقتي":
        variable = gvarstatus("DIGITAL_PIC")
        await asyncio.sleep(1.5)
        if gvarstatus("DIGITAL_PIC") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, variable))
        delgvar("DIGITAL_PIC")

    elif input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = "CUSTOM_ALIVE_EMZED"
        await asyncio.sleep(1.5)
        if gvarstatus("CUSTOM_ALIVE_EMZED") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        delgvar("CUSTOM_ALIVE_EMZED")
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
    elif input_str == "زخرفه الوقتي" or input_str == "زخرفة الوقتي":
        variable = "ZI_FN"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]
    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص" or input_str == "عدد التحذيرات":
        variable = "MAX_FLOOD_IN_PMS"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]
    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه الوقتيه":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1.5)
        if gvarstatus("DEFAULT_BIO") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        delgvar("DEFAULT_BIO")
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))
    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        variable = "ALIVE_NAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]
    elif input_str == "كروب الرسائل" or input_str == "كروب التخزين" or input_str == "كروب الخاص":
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "السجل" or input_str == "كروب السجل":
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "السجل 2" or input_str == "كروب السجل 2":
        variable = "PRIVATE_GROUP_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "قناة السجل" or input_str == "قناة السجلات":
        variable = "PRIVATE_CHANNEL_BOT_API_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "قناة الملفات" or input_str == "قناة الاضافات":
        variable = "PLUGIN_CHANNEL"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "التحقق" or input_str == "كود التحقق":
        variable = "TG_2STEP_VERIFICATION_CODE"
        await asyncio.sleep(1.5)
        if gvarstatus("TG_2STEP_VERIFICATION_CODE") is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        delgvar("TG_2STEP_VERIFICATION_CODE")
        await zed.edit("**❈╎تم حـذف فـار {} . . بنجـاح ☑️**".format(input_str))

    elif input_str == "ايديي" or input_str == "ايدي الحساب":
        variable = "OWNER_ID"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "نقطة الاوامر" or input_str == "نقطه الاوامر":
        variable = "COMMAND_HAND_LER"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "التوكن" or input_str == "توكن البوت":
        variable = "TG_BOT_TOKEN"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        variable = "TG_BOT_USERNAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "الريبو" or input_str == "السورس":
        variable = "UPSTREAM_REPO"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]

    elif input_str == "اسمي التلقائي" or input_str == "الاسم التلقاائي":
        variable = "AUTONAME"
        await asyncio.sleep(1.5)
        if variable not in heroku_var:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str, heroku_var[variable]))
        del heroku_var[variable]
    elif input_str == "ايموجي الايدي" or input_str == "ايموجي ايدي" or input_str == "رمز الايدي" or input_str == "رمز ايدي" or input_str == "الرمز ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_EMOJI")
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("CUSTOM_ALIVE_EMOJI")
    elif input_str == "عنوان الايدي" or input_str == "عنوان ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_TEXT")
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("CUSTOM_ALIVE_TEXT")
    elif input_str == "خط الايدي" or input_str == "خط ايدي" or input_str == "خطوط الايدي" or input_str == "خط ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_FONT")
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("CUSTOM_ALIVE_FONT")
    elif input_str == "كاشف الاباحي" or input_str == "كشف الاباحي":
        variable = gvarstatus("DEEP_API")
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("DEEP_API")
    elif input_str == "ايقاف الترحيب" or input_str == "نوم الترحيب":
        variable = "TIME_STOP"
        await asyncio.sleep(1.5)
        if variable is None:
        	return await zed.edit("**❈╎عـذࢪاً عـزيـزي .. انت لـم تقـم بإضـافـة فـار {} اصـلاً...**".format(input_str))
        await zed.edit("**❈╎تم حـذف {} بنجـاح ☑️**\n**❈╎المتغيـر المحـذوف : ↶**\n `{}`".format(input_str, variable))
        delgvar("TIME_STOP")
    elif input_str == "الترحيب":
        return
    else:
        if input_str:
            return await zed.edit("**❈╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))
        return await edit_or_reply(event, "**❈╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern=r"جلب(?:\s|$)([\s\S]*)")
async def custom_zed(event):
    input_str = event.text[5:]
    zed = await edit_or_reply(event, "**❈╎جــاري جلـب معلـومـات الفــار 🛂. . .**")
    if (input_str == "كليشة الحماية" or input_str == "كليشة الحمايه" or input_str == "كليشه الحماية" or input_str == "كليشه الحمايه"):
        variable = gvarstatus("pmpermit_txt")
        if variable is None:
            await zed.edit("**❈╎فـار كليشـة الحمايـة غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الكليشـة استخـدم الامـر : ↶**\n `.اضف كليشة الحماية` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))
            
    elif input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        variable = gvarstatus("ALIVE_TEMPLATE")
        if variable is None:
            await zed.edit("**❈╎فـار كليشـة الفحص غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الكليشـة استخـدم الامـر : ↶**\n `.اضف كليشة الفحص` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "كليشة البوت" or input_str == "كليشه البوت":
        variable = gvarstatus("START_TEXT")
        if variable is None:
            await zed.edit("**❈╎فـار كليشـة البـوت غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الكليشـة استخـدم الامـر : ↶**\n `.اضف كليشة البوت` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        variable = gvarstatus("pmblock")
        if variable is None:
            await zed.edit("**❈╎فـار كليشـة الحظـر غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الكليشـة استخـدم الامـر : ↶**\n `.اضف كليشة الحظر` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "رمز الوقتي" or input_str == "رمز الاسم الوقتي":
        variable = gvarstatus("CUSTOM_ALIVE_EMZED")
        if variable is None:
            await zed.edit("**❈╎فـار رمـز الوقتـي غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف رمز الوقتي` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "التحقق" or input_str == "كود التحقق":
        variable = gvarstatus("TG_2STEP_VERIFICATION_CODE")
        if variable is None:
            await zed.edit("**❈╎فـار التحقق بخطوتين غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف التحقق`  **بالـرد ع كـود التحـقق**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "كاشف الاباحي" or input_str == "كشف الاباحي":
        variable = gvarstatus("DEEP_API")
        if variable is None:
            await zed.edit("**❈╎فـار كشـف الاباحي غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الكـود استخـدم الامـر : ↶**\n `.اضف كاشف الاباحي` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "البايو" or input_str == "البايو الوقتي" or input_str == "النبذه" or input_str == "البايو تلقائي":
        variable = gvarstatus("DEFAULT_BIO")
        if variable is None:
            await zed.edit("**❈╎فـار البايـو الوقتـي غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع نـص استخـدم الامـر : ↶**\n `.اضف البايو` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "اسم المستخدم" or input_str == "الاسم":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "ALIVE_NAME"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار اسـم المستخـدم غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الاسم استخـدم الامـر : ↶**\n `.اضف اسم المستخدم` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "كود تيرمكس" or input_str == "كود السيشن" or input_str == "كود سيشن":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "STRING_SESSION"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار اسـم المستخـدم غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الاسم استخـدم الامـر : ↶**\n `.اضف اسم المستخدم` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "ايديي" or input_str == "ايدي الحساب":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "OWNER_ID"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار ايـدي الحسـاب غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الايـدي فقـط استخـدم الامـر : ↶**\n `.اضف ايدي الحساب` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "نقطة الاوامر" or input_str == "نقطه الاوامر":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "COMMAND_HAND_LER"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار نقطـة الاوامـر غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الرمـز فقـط استخـدم الامـر : ↶**\n `.اضف نقطة الاوامر` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "التوكن" or input_str == "توكن البوت":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "TG_BOT_TOKEN"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار توكـن البـوت غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع التوكـن فقـط استخـدم الامـر : ↶**\n `.اضف التوكن` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "معرف البوت" or input_str == "معرف بوت":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "TG_BOT_USERNAME"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار معرف البوت غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع المعرف استخـدم الامـر : ↶**\n `.اضف معرف البوت` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "الريبو" or input_str == "السورس":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "UPSTREAM_REPO"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار الريبـو غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع رابط السورس الرسمي استخـدم الامـر : ↶**\n `.اضف الريبو` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "اسمي التلقائي" or input_str == "الاسم التلقاائي":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "AUTONAME"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار الاسـم التلقائي غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الاسم استخـدم الامـر : ↶**\n `.اضف اسمي التلقائي` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "صورة الحماية" or input_str == "صوره الحمايه" or input_str == "صورة الحمايه" or input_str == "صوره الحماية":
        variable = gvarstatus("pmpermit_pic")
        if variable is None:
            await zed.edit("**❈╎فـار صـورة الحمايـة غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الحماية` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "صورة الوقتي" or input_str == "صوره الوقتي":
        variable = gvarstatus("DIGITAL_PIC")
        if variable is None:
            await zed.edit("**❈╎فـار صـورة الوقتـي غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الوقتي` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "صورة الفحص" or input_str == "صوره الفحص":
        variable = gvarstatus("ALIVE_PIC")
        if variable is None:
            await zed.edit("**❈╎فـار صـورة الفحص غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الفحص` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "صورة البوت" or input_str == "صوره البوت":
        variable = gvarstatus("BOT_START_PIC")
        if variable is None:
            await zed.edit("**❈╎فـار صـورة ستـارت البـوت غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة البوت` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "صورة الاوامر" or input_str == "صوره الاوامر":
        variable = gvarstatus("CMD_PIC")
        if variable is None:
            await zed.edit("**❈╎فـار صـورة الاوامـر غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة الاوامر` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "صورة السورس" or input_str == "صوره السورس":
        variable = gvarstatus("ALIVE_PIC")
        if variable is None:
            await zed.edit("**❈╎فـار صـورة السـورس غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع صـورة فقـط استخـدم الامـر : ↶**\n `.اضف صورة السورس` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))
    elif input_str == "زخرفة الوقتي" or input_str == "زخرفه الوقتي":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "ZI_FN"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار زخرفـة الاسـم الوقتي غيـر موجـود ❌**\n**❈╎لـ اضـافته فقـط استخـدم الامـر : ↶**\n `.الوقتي 1` الـى `.الوقتي 14` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "رسائل الحماية" or input_str == "رسائل الحمايه" or input_str == "رسائل الخاص" or input_str == "رسائل حماية الخاص" or input_str == "عدد التحذيرات":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = Config.MAX_FLOOD_IN_PMS
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار رسـائل الحمايـة غيـر موجـود ❌**\n**❈╎لـ اضـافته فقـط استخـدم الامـر : ↶**\n `.اضف رسائل الحماية` بالـرد ع عـدد فقـط \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "زخرفة الوقتية" or input_str == "زخرفه الوقتيه" or input_str == "زخرفة الوقتيه" or input_str == "زخرفه الوقتية":
        variable = gvarstatus("DEFAULT_PIC")
        if variable is None:
            await zed.edit("**❈╎فـار زخرفـة الصـورة الوقتيـة غيـر موجـود ❌**\n**❈╎لـ اضـافته فقـط استخـدم الامـر : ↶**\n `.وقتي 1` الـى `.وقتي 17` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "الوقت" or input_str == "الساعه" or input_str == "المنطقه الزمنيه":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "TZ"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار المنطقـة الزمنيـة غيـر موجـود ❌**\n**❈╎لـ اضـافته فقـط استخـدم الامـر : ↶**\n `.وقت` واسـم الدولـة \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "ايموجي الايدي" or input_str == "ايموجي ايدي" or input_str == "رمز الايدي" or input_str == "رمز ايدي" or input_str == "الرمز ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_EMOJI")
        if variable is None:
            await zed.edit("**❈╎فـار ايموجي/رمز الايدي غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف رمز الايدي` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))
            
    elif input_str == "عنوان الايدي" or input_str == "عنوان ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_TEXT")
        if variable is None:
            await zed.edit("**❈╎فـار نص عنـوان كليشـة الايـدي غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف عنوان الايدي` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "خط الايدي" or input_str == "خط ايدي" or input_str == "خطوط الايدي" or input_str == "خط ايدي":
        variable = gvarstatus("CUSTOM_ALIVE_FONT")
        if variable is None:
            await zed.edit("**❈╎فـار خطـوط كليشـة الايـدي غيـر موجـود ❌**\n**❈╎لـ اضـافته بالـرد ع الرمـز استخـدم الامـر : ↶**\n `.اضف خطوط الايدي` \n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "لاعب 1":
        variable = gvarstatus("Z_AK")
        if gvarstatus("Z_AK") is None:
            await zed.edit("**❈╎المتغيـر غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎المتغيـر {} موجـود ☑️**\n**❈╎قيمـة المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "لاعب 2":
        variable = gvarstatus("Z_A2K")
        if gvarstatus("Z_A2K") is None:
            await zed.edit("**❈╎المتغيـر غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎المتغيـر {} موجـود ☑️**\n**❈╎قيمـة المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "لاعب 3":
        variable = gvarstatus("Z_A3K")
        if gvarstatus("Z_A3K") is None:
            await zed.edit("**❈╎المتغيـر غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎المتغيـر {} موجـود ☑️**\n**❈╎قيمـة المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "لاعب 4":
        variable = gvarstatus("Z_A4K")
        if gvarstatus("Z_A4K") is None:
            await zed.edit("**❈╎المتغيـر غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎المتغيـر {} موجـود ☑️**\n**❈╎قيمـة المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "لاعب 5":
        variable = gvarstatus("Z_A5K")
        if gvarstatus("Z_A5K") is None:
            await zed.edit("**❈╎المتغيـر غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎المتغيـر {} موجـود ☑️**\n**❈╎قيمـة المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "توكن المكافح" or input_str == "كود المكافح" or input_str == "مكافح التخريب" or input_str == "مكافح التفليش":
        if Config.HEROKU_API_KEY is None:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ")
        if Config.HEROKU_APP_NAME is not None:
            app = Heroku.app(Config.HEROKU_APP_NAME)
        else:
            return await ed(event, "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.")
        heroku_var = app.config()
        variable = "SPAMWATCH_API"
        if variable not in heroku_var:
            await zed.edit("**❈╎فـار توكـن المكـافح غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎الفـار {} موجـود ☑️**\n**❈╎قيمـة الفـار : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "اشتراك خاص" or input_str == "اشتراك الخاص" or input_str == "قناة الاشتراك" or input_str == "الاشتراك":
        variable = gvarstatus("Custom_Pm_Channel")
        if gvarstatus("Custom_Pm_Channel") is None:
            await zed.edit("**❈╎المتغيـر غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎المتغيـر {} موجـود ☑️**\n**❈╎قيمـة المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "اشتراك كروب" or input_str == "اشتراك الكروب" or input_str == "قناة الاشتراك" or input_str == "الاشتراك":
        variable = gvarstatus("Custom_G_Channel")
        if gvarstatus("Custom_G_Channel") is None:
            await zed.edit("**❈╎المتغيـر غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎المتغيـر {} موجـود ☑️**\n**❈╎قيمـة المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    elif input_str == "االهمسه":
        variable = gvarstatus("hmsa_id")
        if gvarstatus("hmsa_id") is None:
            await zed.edit("**❈╎المتغيـر غيـر موجـود ❌**\n\n**❈╎قنـاة السـورس : @Power_Thon**")
        else:
            await zed.edit("**❈╎المتغيـر {} موجـود ☑️**\n**❈╎قيمـة المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, variable))

    else:
        if input_str:
            return await zed.edit("**❈╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))
        return await edit_or_reply(event, "**❈╎عـذࢪاً .. لايوجـد هنالك فـار بإسـم {} ؟!.. ارسـل (.اوامر الفارات) لـعرض قائمـة الفـارات**".format(input_str))


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern=r"وقت(?:\s|$)([\s\S]*)")
async def variable(event):
    if Config.HEROKU_API_KEY is None:
        return await ed(
            event,
            "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_API_KEY` اذا كنت لاتعلم اين يوجد فقط اذهب الى حسابك في هيروكو ثم إلى الإعـدادات ستجده بالاسفل انسخه ودخله في الفار. ",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await ed(
            event,
            "❈╎اضبط Var المطلوب في Heroku على وظيفة هذا بشكل طبيعي `HEROKU_APP_NAME` اسم التطبيق اذا كنت لاتعلم.",
        )
    input_str = event.text[5:]
    viraq = "Asia/Baghdad"
    vmsr = "Africa/Cairo"
    vdubai = "Asia/Dubai"
    vturk = "Europe/Istanbul"
    valgiers = "Africa/Algiers"
    vmoroco = "Africa/Casablanca"
    viran = "Asia/Tehran"
    heroku_var = app.config()
    zed = await edit_or_reply(event, "**❈╎جـاري إعـداد المنطقـة الزمنيـة لـ كايـدو 🌐...**")
    # All Rights Reserved for "Zed-Thon" "زلـزال الهيبـه"
    if input_str == "العراق" or input_str == "اليمن" or input_str == "سوريا" or input_str == "السعودية" or input_str == "لبنان" or input_str == "الاردن":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المتغير : ↶**\n دولـة `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**❈╎تم إضـافـة المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المضـاف اليـه : ↶**\n دولـة `{}` \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        heroku_var[variable] = viraq
    elif input_str == "مصر" or input_str == "ليبيا" or input_str == "القاهرة":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المتغير : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**❈╎تم إضـافـة المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المضـاف اليـه : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        heroku_var[variable] = vmsr
    elif input_str == "دبي" or input_str == "الامارات" or input_str == "عمان" or input_str == "مسقط":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المتغير : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**❈╎تم إضـافـة المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المضـاف اليـه : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        heroku_var[variable] = vdubai
    elif input_str == "تركيا" or input_str == "اسطنبول" or input_str == "انقرة":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المتغير : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**❈╎تم إضـافـة المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المضـاف اليـه : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        heroku_var[variable] = vturk
    elif input_str == "تونس" or input_str == "الجزائر":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المتغير : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**❈╎تم إضـافـة المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المضـاف اليـه : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        heroku_var[variable] = valgiers
    elif input_str == "المغرب" or input_str == "موريتانيا" or input_str == "الدار البيضاء":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المتغير : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**❈╎تم إضـافـة المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المضـاف اليـه : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        heroku_var[variable] = vmoroco        
    elif input_str == "ايران" or input_str == "طهران":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await zed.edit("**❈╎تم تغييـر المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المتغير : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        else:
            await zed.edit("**❈╎تم إضـافـة المنطقـة الزمنيـة .. بنجـاح ☑️**\n**❈╎المضـاف اليـه : ↶**\n دولـة `{}`  \n**❈╎يتم الآن إعـادة تشغيـل بـوت الحارس الذكي يستغـرق الامر 2-1 دقيـقة ▬▭ ...**".format(input_str))
        heroku_var[variable] = viran


# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="اضف صورة (الحماية|الحمايه|الفحص|الوقتي|البوت|الكتم) ?(.*)")
async def _(malatha):
    if malatha.fwd_from:
        return
    zed = await edit_or_reply(malatha, "**❈╎جـاري اضـافة فـار الصـورة الـى بـوتك ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
        #     if BOTLOG:
        await malatha.client.send_message(
            BOTLOG_CHATID,
            "**❈╎تم إنشاء حساب Telegraph جديد {} للدورة الحالية‌‌** \n**❈╎لا تعطي عنوان url هذا لأي شخص**".format(
                auth_url
            ),
        )
    optional_title = malatha.pattern_match.group(2)
    if malatha.reply_to_msg_id:
        start = datetime.now()
        r_message = await malatha.get_reply_message()
        input_str = malatha.pattern_match.group(1)
        if input_str in ["الحماية", "الحمايه"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**❈╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("pmpermit_pic", vinfo)
                await zed.edit("**❈╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, vinfo))
        elif input_str in ["الفحص", "السورس"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**❈╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("ALIVE_PIC", vinfo)
                await zed.edit("**❈╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, vinfo))
        elif input_str in ["البوت", "الستارت"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**❈╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("BOT_START_PIC", vinfo)
                await zed.edit("**❈╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, vinfo))
        elif input_str in ["الاوامر", "اللوحه"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**❈╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("CMD_PIC", vinfo)
                await zed.edit("**❈╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, vinfo))
        elif input_str in ["السورس", "سورس"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**❈╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("ALIVE_PIC", vinfo)
                await zed.edit("**❈╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, vinfo))
        elif input_str in ["الكتم", "كتم"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**❈╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("KTM_PIC", vinfo)
                await zed.edit("**❈╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, vinfo))
        elif input_str in ["الوقتي", "البروفايل"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            await zed.edit(f"** ⪼ تم تحميل** {downloaded_file_name} **.. بنجـاح ✓**")
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**❈╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("DIGITAL_PIC", vinfo)
                await zed.edit("**❈╎تم تغييـر صـورة {} .. بنجـاح ☑️**\n**❈╎المتغيـر : ↶**\n `{}` \n\n**❈╎قنـاة السـورس : @Power_Thon**".format(input_str, vinfo))


    else:
        await zed.edit(
            "**❈╎بالـرد ع صـورة لتعييـن الفـار ...**",
        )


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")



# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="اوامر الفارات")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalVP_cmd)

@zedub.zed_cmd(pattern="التخصيص")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalVP_cmd)