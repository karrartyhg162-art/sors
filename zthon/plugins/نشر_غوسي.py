import asyncio
import random
from telethon.tl.types import Channel, Chat
from zthon import zedub
from zthon.core.managers import edit_delete, edit_or_reply
from zthon.sql_helper.globals import addgvar, gvarstatus

BROADCAST_RUNNING = False

def get_gaussian_index(list_length):
    if list_length <= 1:
        return 0
    mu = (list_length - 1) / 2
    sigma = list_length / 6
    while True:
        idx = int(random.gauss(mu, sigma))
        if 0 <= idx < list_length:
            return idx

@zedub.zed_cmd(pattern=r"اضف نشر(?: |$)(.*)")
async def add_custom_group(event):
    input_str = event.pattern_match.group(1).strip()
    
    current_groups = gvarstatus("GAUSS_GROUPS") or ""
    group_list = current_groups.split(",") if current_groups else []
    added = 0
    
    if input_str:
        for g in input_str.split():
            try:
                entity = await event.client.get_entity(g)
                chat_id = str(entity.id)
                if chat_id not in group_list:
                    group_list.append(chat_id)
                    added += 1
            except Exception:
                pass
        if added > 0:
            addgvar("GAUSS_GROUPS", ",".join(group_list))
            await edit_or_reply(event, f"**⎉╎تم حفظ ({added}) مجموعات في القائمة المخصصة بنجاح ✓**\n**⎉╎يمكنك الآن النشر فيها باستخدام الأمر:** `.نشر مخصص 120-300`")
        else:
            await edit_or_reply(event, "**⎉╎لم يتم إضافة شيء! إما أن المعرفات خاطئة أو أنها مضافة مسبقاً.**")
        return

    zed = await edit_or_reply(event, "**⎉╎قم الآن بإرسال معرفات أو أيديات المجموعات (مجموعة واحدة أو عدة مجموعات).**\n**⎉╎وعندما تنتهي من إرسال كل المجموعات المطلوبة، اكتب الأمر:** `.تم`")
    from telethon import events
    
    try:
        async with event.client.conversation(event.chat_id, timeout=300) as conv:
            while True:
                response = await conv.wait_event(events.NewMessage(chats=event.chat_id, from_users=event.sender_id))
                text = response.text.strip()
                
                if text == ".تم":
                    break
                    
                added_in_step = 0
                for g in text.split():
                    try:
                        entity = await event.client.get_entity(g)
                        chat_id = str(entity.id)
                        if chat_id not in group_list:
                            group_list.append(chat_id)
                            added += 1
                            added_in_step += 1
                    except Exception:
                        pass
                
                if added_in_step > 0:
                    await conv.send_message(f"**⎉╎تم التعرف على المجموعات الجديدة!**\n**⎉╎إجمالي المجموعات المضافة في هذه الجلسة حتى الآن:** `{added}` مجموعة.\n**⎉╎أرسل المزيد من المجموعات، أو اكتب `.تم` للحفظ النهائي.**")
                else:
                    await conv.send_message("**⎉╎لم يتم التعرف على أية مجموعات جديدة من رسالتك الأخيرة، تأكد من المعرف وأرسله مجدداً، أو اكتب `.تم`.**")

    except asyncio.TimeoutError:
        return await zed.edit("**⎉╎انتهى وقت الانتظار! تم إغلاق وضع الإضافة.**")
        
    if added > 0:
        addgvar("GAUSS_GROUPS", ",".join(group_list))
        await event.respond(f"**⎉╎اكتملت الإضافة! تم حفظ إجمالي ({added}) مجموعات في القائمة بنجاح ✓**\n**⎉╎يمكنك الآن النشر فيها متى شئت باستخدام الأمر:** `.نشر مخصص 120-300`")
    else:
        await event.respond("**⎉╎تم إنهاء الوضع دون إضافة أي مجموعات جديدة.**")


@zedub.zed_cmd(pattern=r"حذف نشر(?: |$)(.*)")
async def remove_custom_group(event):
    input_str = event.pattern_match.group(1).strip()
    
    current_groups = gvarstatus("GAUSS_GROUPS") or ""
    group_list = current_groups.split(",") if current_groups else []
    removed = 0
    
    if input_str:
        for g in input_str.split():
            try:
                entity = await event.client.get_entity(g)
                chat_id = str(entity.id)
                if chat_id in group_list:
                    group_list.remove(chat_id)
                    removed += 1
            except Exception:
                if g in group_list:
                    group_list.remove(g)
                    removed += 1
        if removed > 0:
            addgvar("GAUSS_GROUPS", ",".join(group_list))
            await edit_or_reply(event, f"**⎉╎تم إزالة ({removed}) مجموعات من القائمة بنجاح ✓**")
        else:
            await edit_or_reply(event, "**⎉╎لم يتم حذف شيء! المجموعات غير موجودة في القائمة أصلاً.**")
        return

    zed = await edit_or_reply(event, "**⎉╎قم الآن بإرسال معرفات أو أيديات المجموعات التي تريد استبعادها من القائمة.**\n**⎉╎وعندما تنتهي، اكتب الأمر:** `.تم`")
    from telethon import events
    
    try:
        async with event.client.conversation(event.chat_id, timeout=300) as conv:
            while True:
                response = await conv.wait_event(events.NewMessage(chats=event.chat_id, from_users=event.sender_id))
                text = response.text.strip()
                
                if text == ".تم":
                    break
                    
                removed_in_step = 0
                for g in text.split():
                    try:
                        entity = await event.client.get_entity(g)
                        chat_id = str(entity.id)
                        if chat_id in group_list:
                            group_list.remove(chat_id)
                            removed += 1
                            removed_in_step += 1
                    except Exception:
                        if g in group_list:
                            group_list.remove(g)
                            removed += 1
                            removed_in_step += 1
                            
                if removed_in_step > 0:
                    await conv.send_message(f"**⎉╎تم الاستبعاد!**\n**⎉╎إجمالي المجموعات المستبعدة في هذه الجلسة حتى الآن:** `{removed}` مجموعة.\n**⎉╎أرسل المزيد، أو اكتب `.تم` للإنهاء.**")
                else:
                    await conv.send_message("**⎉╎هذه المجموعات غير موجودة في القائمة أصلاً! أرسل المزيد أو اكتب `.تم`.**")

    except asyncio.TimeoutError:
        return await zed.edit("**⎉╎انتهى وقت الانتظار! تم إغلاق وضع الحذف.**")
        
    if removed > 0:
        addgvar("GAUSS_GROUPS", ",".join(group_list))
        await event.respond(f"**⎉╎اكتمل الحذف! تم إزالة إجمالي ({removed}) مجموعات من القائمة بنجاح ✓**")
    else:
        await event.respond("**⎉╎تم إنهاء الوضع دون حذف أي مجموعات.**")


@zedub.zed_cmd(pattern=r"ايقاف النشر$")
async def stop_broadcast(event):
    global BROADCAST_RUNNING
    if not BROADCAST_RUNNING:
        return await edit_or_reply(event, "**⎉╎لا يوجد عملية نشر قيد التشغيل حالياً!**")
    
    BROADCAST_RUNNING = False
    await edit_or_reply(event, "**⎉╎تم إيقاف عملية النشر التلقائي بنجاح ✓**")


@zedub.zed_cmd(pattern=r"نشر (مخصص )?(\d+)-(\d+)$")
async def start_gaussian_broadcast(event):
    global BROADCAST_RUNNING
    
    reply = await event.get_reply_message()
    if not reply:
        return await edit_or_reply(event, "**⎉╎عـذراً .. يجب عليك الرد على الرسالة التي تريد نشرها أولاً!**")
    
    if BROADCAST_RUNNING:
        return await edit_or_reply(event, "**⎉╎هناك عملية نشر تعمل حالياً، قم بإيقافها أولاً باستخدام `.ايقاف النشر`**")
    
    is_custom = bool(event.pattern_match.group(1))
    min_time = int(event.pattern_match.group(2))
    max_time = int(event.pattern_match.group(3))
    
    if min_time >= max_time:
        return await edit_or_reply(event, "**⎉╎عـذراً .. يجب أن يكون الوقت الأصغر أولاً، مثلاً: `.نشر 120-300`**")
    
    await edit_or_reply(event, "**⎉╎جـارِ جلب المجموعات وتحضير النشر بالتوزيع الغوسي .. الرجاء الانتظار**")
    
    groups_to_post = []
    
    if is_custom:
        current_groups = gvarstatus("GAUSS_GROUPS") or ""
        if not current_groups:
            return await edit_or_reply(event, "**⎉╎قائمة النشر المخصص فارغة! قم بإضافة مجموعات باستخدام `.تفعيل مخصص`**")
        groups_to_post = [int(x) for x in current_groups.split(",") if x.strip()]
    else:
        dialogs = await event.client.get_dialogs()
        for dialog in dialogs:
            if dialog.is_group:
                groups_to_post.append(dialog.id)
                
    if not groups_to_post:
        return await edit_or_reply(event, "**⎉╎لم يتم العثور على أي مجموعات للنشر!**")
    
    total_groups = len(groups_to_post)
    await edit_or_reply(event, f"**⎉╎تم البدء بعملية النشر التلقائي!**\n**⎉╎العدد الإجمالي:** `{total_groups}` مجموعة\n**⎉╎النطاق الزمني:** من `{min_time}` إلى `{max_time}` ثانية\n**⎉╎لإيقاف النشر أرسل:** `.ايقاف النشر`")
    
    BROADCAST_RUNNING = True
    successful_posts = 0
    
    mu_time = (min_time + max_time) / 2
    sigma_time = (max_time - min_time) / 6
    
    while groups_to_post and BROADCAST_RUNNING:
        # Choose group using Gaussian Distribution
        idx = get_gaussian_index(len(groups_to_post))
        target_group = groups_to_post.pop(idx)
        
        try:
            await event.client.send_message(target_group, reply)
            successful_posts += 1
        except Exception as e:
            # Group might be restricted or bot was kicked
            pass
            
        if not groups_to_post or not BROADCAST_RUNNING:
            break
            
        # Calculate random sleep time using Gaussian Distribution
        while True:
            sleep_time = random.gauss(mu_time, sigma_time)
            if min_time <= sleep_time <= max_time:
                break
                
        await asyncio.sleep(sleep_time)
        
    BROADCAST_RUNNING = False
    
    if len(groups_to_post) == 0:
        await event.respond(f"**⎉╎اكتملت عملية النشر التلقائي!**\n**⎉╎تم النشر بنجاح في:** `{successful_posts}` مجموعة ✓")
    else:
        await event.respond(f"**⎉╎تم إيقاف عملية النشر!**\n**⎉╎الجروبات التي تم النشر فيها:** `{successful_posts}` مجموعة.")
