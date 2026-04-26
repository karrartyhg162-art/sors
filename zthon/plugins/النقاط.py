import requests
import asyncio
from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from zthon import zedub
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id



ZelzalCoins_cmd = (
    "[ᯓ 𝘀𝗼𝘂𝗿𝗰𝗲 Smart Guard - اوامـر تجميـع النقـاط](t.me/SI0lZ) 𓆪\n\n"
    "**𓆰 قـائمـة اوامـر تجميـع نقـاط بوتـات تمـويـل الخاص بسـورس كايـدو🦾 :** \n\n"
    "`.المليار`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت المليـار ( @EEOBot ) .. تلقائـيـًا ✓**\n\n"
    "`.الجوكر`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت الجوكـر ( @A_MAN9300BOT ) .. تلقائـيـًا ✓**\n\n"
    "`.الجنرال`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت الجنــرال ( @MARKTEBOT ) .. تلقائـيـًا ✓**\n\n"
    "`.المليون`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت العـــرب ( @xnsex21bot ) .. تلقائـيـًا ✓**\n\n"
    "`.العرب`\n"
    "**⪼ لـ تجميـع النقـاط مـن بـوت المليــون ( @qweqwe1919bot ) .. تلقائـيـًا ✓**\n\n\n"
    "`.المليار ايقاف`\n"
    "**⪼ لـ إيقـاف عمليـة تجميـع النقـاط من بوت المليـار ..**\n\n"
    "`.الجوكر ايقاف`\n"
    "**⪼ لـ إيقـاف عمليـة تجميـع النقـاط من بوت الجوكـر ..**\n\n"
    "`.الجنرال ايقاف`\n"
    "**⪼ لـ إيقـاف عمليـة تجميـع النقـاط من بوت الجنـرال ..**\n\n"
    "`.المليون ايقاف`\n"
    "**⪼ لـ إيقـاف عمليـة تجميـع النقـاط من بوت المليـون ..**\n\n\n"
    "**𓆰 قـائمـة اوامـر تجميـع نقـاط العـاب بـوت وعـد🦾 :** \n\n"
    "`.بخشيش وعد`\n"
    "`.راتب وعد`\n"
    "`.استثمار وعد`\n"
    "`.كلمات وعد`\n"
    "**⪼ لـ تجميـع نقـاط العـاب في بوت وعـد تــلــقـائيًا ✓ ..قم بـ اضافة البوت في مجموعة جديدة ثم ارسل**\n"
    "**الامـر + عـدد الاعـادة للامـر**\n"
    "**⪼ مثــال :**\n"
    "`.راتب وعد 50`\n\n\n"
    "**- مـلاحظــه :**\n"
    "**⪼ سيتم اضـافـه المزيـد من البوتـات بالتحديثـات الجايـه .. إذا تريـد اضافـة بـوت محـدد راسـل مطـور السـورس @A_D_P**"
)


@zedub.zed_cmd(pattern="بوت المليار$")
async def _(event):
    await event.edit('@EEOBot')

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="المليار ?(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    await event.edit("**𓆰 حـسنـًا .. تأكـد من انك مشتـرك بـ قنـوات الاشتـراك الإجبـاري لتجنب الأخطـاء @EEOBot**")
    channel_entity = await zedub.get_entity('@EEOBot')
    await zedub.send_message('@EEOBot', '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages('@EEOBot', limit=1)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages('@EEOBot', limit=1)
    await msg1[0].click(0)

    chs = 1
    for i in range(100):
        await asyncio.sleep(4)

        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1,
                                               offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('**𓆰 لا يوجد قنوات في الوقت الحالي .. قم يتجميع النقاط بطريقه مـخـتـلفة**') != -1:
            await zedub.send_message(event.chat_id, f"**𓆰 لا يـوجـد قنـوات بالبـوت حـاليًا ...**")
            break
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, f"**𓆰 تم إيقـاف تجميـع النقـاط ☑️ ...**")
            break
        url = msgs.reply_markup.rows[0].buttons[0].url
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages('@EEOBot', limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await event.edit(f"**𓆰 تم بنجـاح الاشتـراك في {chs} قنـاة .❗**")
        except:
            msg2 = await zedub.get_messages('@EEOBot', limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await event.edit(f"**𓆰 القنـاة رقـم {chs} خطـأ .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**𓆰 تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")



@zedub.zed_cmd(pattern="تجميع المليار ?(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    await event.edit("**𓆰 حـسنـًا .. تأكـد من انك مشتـرك بـ قنـوات الاشتـراك الإجبـاري لتجنب الأخطـاء @EEOBot**")
    channel_entity = await zedub.get_entity('@EEOBot')
    await zedub.send_message('@EEOBot', '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages('@EEOBot', limit=1)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages('@EEOBot', limit=1)
    await msg1[0].click(0)

    chs = 1
    for i in range(100):
        await asyncio.sleep(4)

        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1,
                                               offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('**𓆰 لا يوجد قنوات في الوقت الحالي .. قم يتجميع النقاط بطريقه مـخـتـلفة**') != -1:
            await zedub.send_message(event.chat_id, f"**𓆰 لا يـوجـد قنـوات بالبـوت حـاليًا ...**")
            break
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, f"**𓆰 تم إيقـاف تجميـع النقـاط ☑️ ...**")
            break
        url = msgs.reply_markup.rows[0].buttons[0].url
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages('@EEOBot', limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await event.edit(f"**𓆰 تم بنجـاح الاشتـراك في {chs} قنـاة .❗**")
        except:
            msg2 = await zedub.get_messages('@EEOBot', limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await event.edit(f"**𓆰 القنـاة رقـم {chs} خطـأ .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**𓆰 تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")



@zedub.zed_cmd(pattern="بوت العرب$")
async def _(event):
    await event.edit('@xnsex21bot')

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="العرب ?(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    await event.edit("**𓆰 حـسنـًا .. تأكـد من انك مشتـرك بـ قنـوات الاشتـراك الإجبـاري لتجنب الأخطـاء @xnsex21bot**")
    channel_entity = await zedub.get_entity('@xnsex21bot')
    await zedub.send_message('@xnsex21bot', '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages('@xnsex21bot', limit=1)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages('@xnsex21bot', limit=1)
    await msg1[0].click(0)

    chs = 1
    for i in range(100):
        await asyncio.sleep(4)

        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1,
                                               offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('**𓆰 لا يوجد قنوات في الوقت الحالي .. قم يتجميع النقاط بطريقه مـخـتـلفة**') != -1:
            await zedub.send_message(event.chat_id, f"**𓆰 لا يـوجـد قنـوات بالبـوت حـاليًا ...**")
            break
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, f"**𓆰 تم إيقـاف تجميـع النقـاط ☑️ ...**")
            break
        url = msgs.reply_markup.rows[0].buttons[0].url
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages('@xnsex21bot', limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await event.edit(f"**𓆰 تم بنجـاح الاشتـراك في {chs} قنـاة .❗**")
        except:
            msg2 = await zedub.get_messages('@xnsex21bot', limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await event.edit(f"**𓆰 القنـاة رقـم {chs} خطـأ .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**𓆰 تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")



@zedub.zed_cmd(pattern="تجميع العرب ?(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    await event.edit("**𓆰 حـسنـًا .. تأكـد من انك مشتـرك بـ قنـوات الاشتـراك الإجبـاري لتجنب الأخطـاء @xnsex21bot**")
    channel_entity = await zedub.get_entity('@xnsex21bot')
    await zedub.send_message('@xnsex21bot', '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages('@xnsex21bot', limit=1)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages('@xnsex21bot', limit=1)
    await msg1[0].click(0)

    chs = 1
    for i in range(100):
        await asyncio.sleep(4)

        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1,
                                               offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('**𓆰 لا يوجد قنوات في الوقت الحالي .. قم يتجميع النقاط بطريقه مـخـتـلفة**') != -1:
            await zedub.send_message(event.chat_id, f"**𓆰 لا يـوجـد قنـوات بالبـوت حـاليًا ...**")
            break
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, f"**𓆰 تم إيقـاف تجميـع النقـاط ☑️ ...**")
            break
        url = msgs.reply_markup.rows[0].buttons[0].url
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages('@xnsex21bot', limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await event.edit(f"**𓆰 تم بنجـاح الاشتـراك في {chs} قنـاة .❗**")
        except:
            msg2 = await zedub.get_messages('@xnsex21bot', limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await event.edit(f"**𓆰 القنـاة رقـم {chs} خطـأ .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**𓆰 تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    
    
    
@zedub.zed_cmd(pattern="بوت الجوكر$")
async def _(event):
    await event.edit('@A_MAN9300BOT')

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="الجوكر ?(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    await event.edit("**𓆰 حـسنـًا .. تأكـد من انك مشتـرك بـ قنـوات الاشتـراك الإجبـاري لتجنب الأخطـاء @A_MAN9300BOT**")
    channel_entity = await zedub.get_entity('@A_MAN9300BOT')
    await zedub.send_message('@A_MAN9300BOT', '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages('@A_MAN9300BOT', limit=1)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages('@A_MAN9300BOT', limit=1)
    await msg1[0].click(0)

    chs = 1
    for i in range(100):
        await asyncio.sleep(4)

        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1,
                                               offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('**𓆰 لا يوجد قنوات في الوقت الحالي .. قم يتجميع النقاط بطريقه مـخـتـلفة**') != -1:
            await zedub.send_message(event.chat_id, f"**𓆰 لا يـوجـد قنـوات بالبـوت حـاليًا ...**")
            break
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, f"**𓆰 تم إيقـاف تجميـع النقـاط ☑️ ...**")
            break
        url = msgs.reply_markup.rows[0].buttons[0].url
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages('@A_MAN9300BOT', limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await event.edit(f"**𓆰 تم بنجـاح الاشتـراك في {chs} قنـاة .❗**")
        except:
            msg2 = await zedub.get_messages('@A_MAN9300BOT', limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await event.edit(f"**𓆰 القنـاة رقـم {chs} خطـأ .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**𓆰 تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")



@zedub.zed_cmd(pattern="بوت الجنرال$")
async def _(event):
    await event.edit('@MARKTEBOT')

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="الجنرال ?(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    await event.edit("**𓆰 حـسنـًا .. تأكـد من انك مشتـرك بـ قنـوات الاشتـراك الإجبـاري لتجنب الأخطـاء @MARKTEBOT**")
    channel_entity = await zedub.get_entity('@MARKTEBOT')
    await zedub.send_message('@MARKTEBOT', '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages('@MARKTEBOT', limit=1)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages('@MARKTEBOT', limit=1)
    await msg1[0].click(0)

    chs = 1
    for i in range(100):
        await asyncio.sleep(4)

        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1,
                                               offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('**𓆰 لا يوجد قنوات في الوقت الحالي .. قم يتجميع النقاط بطريقه مـخـتـلفة**') != -1:
            await zedub.send_message(event.chat_id, f"**𓆰 لا يـوجـد قنـوات بالبـوت حـاليًا ...**")
            break
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, f"**𓆰 تم إيقـاف تجميـع النقـاط ☑️ ...**")
            break
        url = msgs.reply_markup.rows[0].buttons[0].url
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages('@MARKTEBOT', limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await event.edit(f"**𓆰 تم بنجـاح الاشتـراك في {chs} قنـاة .❗**")
        except:
            msg2 = await zedub.get_messages('@MARKTEBOT', limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await event.edit(f"**𓆰 القنـاة رقـم {chs} خطـأ .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**𓆰 تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")



@zedub.zed_cmd(pattern="بوت المليون$")
async def _(event):
    await event.edit('@qweqwe1919bot')

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="المليون ?(.*)")
async def _(event):
    con = event.pattern_match.group(1).lower()
    await event.edit("**𓆰 حـسنـًا .. تأكـد من انك مشتـرك بـ قنـوات الاشتـراك الإجبـاري لتجنب الأخطـاء @qweqwe1919bot**")
    channel_entity = await zedub.get_entity('@qweqwe1919bot')
    await zedub.send_message('@qweqwe1919bot', '/start')
    await asyncio.sleep(4)
    msg0 = await zedub.get_messages('@qweqwe1919bot', limit=1)
    await msg0[0].click(2)
    await asyncio.sleep(4)
    msg1 = await zedub.get_messages('@qweqwe1919bot', limit=1)
    await msg1[0].click(0)

    chs = 1
    for i in range(100):
        await asyncio.sleep(4)

        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1,
                                               offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        if msgs.message.find('**𓆰 لا يوجد قنوات في الوقت الحالي .. قم يتجميع النقاط بطريقه مـخـتـلفة**') != -1:
            await zedub.send_message(event.chat_id, f"**𓆰 لا يـوجـد قنـوات بالبـوت حـاليًا ...**")
            break
        if con == "ايقاف":
            await zedub.send_message(event.chat_id, f"**𓆰 تم إيقـاف تجميـع النقـاط ☑️ ...**")
            break
        url = msgs.reply_markup.rows[0].buttons[0].url
        try:
            try:
                await zedub(JoinChannelRequest(url))
            except:
                bott = url.split('/')[-1]
                await zedub(ImportChatInviteRequest(bott))
            msg2 = await zedub.get_messages('@qweqwe1919bot', limit=1)
            await msg2[0].click(text='تحقق')
            chs += 1
            await event.edit(f"**𓆰 تم بنجـاح الاشتـراك في {chs} قنـاة .❗**")
        except:
            msg2 = await zedub.get_messages('@qweqwe1919bot', limit=1)
            await msg2[0].click(text='التالي')
            chs += 1
            await event.edit(f"**𓆰 القنـاة رقـم {chs} خطـأ .. يمكـن تبنـدت**")
    await zedub.send_message(event.chat_id, "**𓆰 تم الانتهـاء مـن تجميـع النقـاط .. حاول من جديد في وقت آخر ✓**")
    
    
 
# code by @r0r77 & @Dar4k
@zedub.zed_cmd(pattern="بخشيش وعد (.*)")
async def baqshis(event):
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await zedub.send_message(chat, "بخشيش")
        await asyncio.sleep(605)


@zedub.zed_cmd(pattern="راتب وعد (.*)")
async def ratb(event):
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await zedub.send_message(chat, "راتب")
        await asyncio.sleep(605)


@zedub.zed_cmd(pattern="كلمات وعد (.*)")
async def waorwaad(event):
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await zedub.send_message(chat, "كلمات")
        await asyncio.sleep(0.5)
        masg = await jmub.get_messages(chat, limit=1)
        masg = masg[0].message
        masg = ("".join(masg.split(maxsplit=3)[3:])).split(" ", 2)
        if len(masg) == 2:
            msg = masg[0]
            await zedub.send_message(chat, msg)
        else:
            msg = masg[0] + " " + masg[1]
            await zedub.send_message(chat, msg)


@zedub.zed_cmd(pattern="استثمار وعد (.*)")
async def _(event):
    await event.edit(
        "**𓆰 تم تفعيل الاستثمـار لـ بوت وعد بنجـاح ✅**\n**𓆰 لـ إيقافـه ارسـل** \n`.استثمار وعد 1`"
    )
    for i in range(int("".join(event.text.split(maxsplit=2)[2:]).split(" ", 2)[0])):
        chat = event.chat_id
        await zedub.send_message(chat, "فلوسي")
        await asyncio.sleep(0.5)
        masg = await jmub.get_messages(chat, limit=1)
        masg = masg[0].message
        masg = ("".join(masg.split(maxsplit=2)[2:])).split(" ", 2)
        msg = masg[0]
        if int(msg) > 500000000:
            await zedub.send_message(chat, f"استثمار {msg}")
            await asyncio.sleep(10)
            mssag2 = await jmub.get_messages(chat, limit=1)
            await mssag2[0].click(text="اي ✅")
        else:
            await zedub.send_message(chat, f"استثمار {msg}")
        await asyncio.sleep(1210)



@zedub.zed_cmd(pattern="اوامر النقاط")
async def cmd(zelzallll):
    await edit_or_reply(zelzallll, ZelzalCoins_cmd)

