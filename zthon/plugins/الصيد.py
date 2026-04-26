# Code by: t.me/dar4k  ~ t.me/r0r77

# Update by t.me/zzzzl1l

import random

import requests

import time

from asyncio import sleep

import telethon

from telethon.sync import functions

from user_agent import generate_user_agent



from zthon import zedub



a = "qwertyuiopassdfghjklzxcvbnm"

b = "1234567890"

e = "qwertyuiopassdfghjklzxcvbnm1234567890"



trys, trys2 = [0], [0]

isclaim = ["off"]

isauto = ["off"]





def check_user(username):

    url = "https://t.me/" + str(username)

    headers = {

        "User-Agent": generate_user_agent(),

        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",

        "Accept-Encoding": "gzip, deflate, br",

        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",

    }



    response = requests.get(url, headers=headers)

    if (

        response.text.find(

            'If you have <strong>Telegram</strong>, you can contact <a class="tgme_username_link"'

        )

        >= 0

    ):

        return True

    else:

        return False





def gen_user(choice):

    if choice == "ثلاثيات":

        c = random.choices(a)

        d = random.choices(b)

        s = random.choices(e)

        f = [c[0], "_", d[0], "_", s[0]]

        username = "".join(f)



    elif choice == "خماسيات":

        c = d = random.choices(a)

        d = random.choices(b)

        f = [c[0], c[0], c[0], c[0], d[0]]

        random.shuffle(f)

        username = "".join(f)



    elif choice == "خماسي حرفين":

        c = d = random.choices(a)

        d = random.choices(e)

        f = [c[0], d[0], c[0], c[0], d[0]]

        random.shuffle(f)

        username = "".join(f)



    elif choice == "سداسيات":

        c = d = random.choices(a)

        d = random.choices(e)

        f = [c[0], c[0], c[0], c[0], c[0], d[0]]

        random.shuffle(f)

        username = "".join(f)



    elif choice == "سداسي حرفين":

        c = d = random.choices(a)

        d = random.choices(b)

        f = [c[0], d[0], c[0], c[0], c[0], d[0]]

        random.shuffle(f)

        username = "".join(f)



    elif choice == "سباعيات":

        c = d = random.choices(a)

        d = random.choices(b)

        f = [c[0], c[0], c[0], c[0], d[0], c[0], c[0]]

        random.shuffle(f)

        username = "".join(f)



    elif choice == "بوتات":

        c = random.choices(a)

        d = random.choices(e)

        s = random.choices(e)

        f = [c[0], s[0], d[0]]

        username = "".join(f)

        username = username + "bot"



    elif choice == "تيست":

        c = d = random.choices(a)

        d = random.choices(b)

        f = [c[0], d[0], c[0], d[0], d[0], c[0], c[0], d[0], c[0], d[0]]

        random.shuffle(f)

        username = "".join(f)

    else:

        raise ValueError("Invalid choice for username generation.")

    return username





ZelzalChecler_cmd = (

    "𓆩 [Smart Guard - أوامـر الصيد والتشيكـر](t.me/SI0lZ) 𓆪\n\n"

    "**✾╎قـائمـة أوامـر تشيكـر صيـد معـرفات تيليجـرام :** \n\n"

    "`.النوع`\n"

    "**⪼ لـ عـرض الانـوع التي يمكـن صيدهـا مع الامثـله**\n"

    "`.صيد` + النـوع\n"

    "**⪼ لـ صيـد يـوزرات عشوائيـة على حسب النـوع**\n"

    "`.تثبيت` + اليوزر\n"

    "**⪼ لـ تثبيت اليـوزر بقنـاة معينـه إذا اصبح متـاحًا يتم اخـذه**\n"

    "`.ثبت` + اليوزر\n"

    "**⪼ لـ تثبيت اليـوزر بحسـابك مباشـرة إذا اصبح متـاحًا يتم اخـذه**\n"

    "`.حالة الصيد`\n"

    "**⪼ لـ معرفـة حالـة تقـدم عمليـة الصيد**\n"

    "`.حالة التثبيت`\n"

    "**⪼ لـ معرفـة حالـة تقـدم التثبيت التلقـائـي**\n"

    "`.ايقاف الصيد`\n"

    "**⪼ لـ إيقـاف عمليـة الصيد الجاريـة**\n"

    "`.ايقاف التثبيت`\n"

    "**⪼ لـ إيقـاف عمليـة التثبيت التلقـائـي**\n\n"

    "**- ملاحظـات مهـمة قبـل استخـدام أوامـر الصيد والتثبيت :**\n"

    "**⪼** تأكد من ان حسابك يوجد فيه مساحـة لإنشاء قناة عامة (قناة بمعرف)\n"

    "**⪼** إذا كان لا يوجد مساحـة لإنشاء قناة عامة قم بارسال يوزر اي قناة من قنوات حسابك وبالرد عـلى مـعرفهـا ارسل احد اوامر الصيد\n"

    "**⪼** لا تـقـم بإيقـاف الصيد حـتى لـو استـمر الصيد أيـام\n"

    "**⪼** تحلى بالصبر وكرر محاولات الصيد لتصـيد مـعرف يوزر\n"

    "**⪼** كل نوع من اليوزرات يختلف عن الاخر من حيث نسبة الصيد\n"

    "**⪼ التثبيت هو تثبيت يوزر محدد حتى ماينسرق منك عندما يصير متاح**\n\n"

    "**- انضـم للقنـاة ~ @hh9hh9**\n"

    "**⪼ لـ رؤيـة بعـض اليـوزرات التي قام بصيدهـا منصبيـن كايـدو**\n\n"

)



ZelzalType_cmd = (

"𓆩 [Smart Guard - أنـواع اليـوزرات](t.me/SI0lZ) 𓆪\n\n"

"**✾╎قـائمـة أنـواع اليـوزرات التي يمكـن صيدهـا مـع الأمثـلة :** \n\n"

"⪼  `.صيد ثلاثيات`  **مثـال ~** A_R_D\n"

"⪼  `.صيد خماسيات`  **مثـال ~** AAARA\n"

"⪼  `.صيد خماسي حرفين`  **مثـال ~** AAARD\n"

"⪼  `.صيد سداسيات`  **مثـال ~** AAARAA\n"

"⪼  `.صيد سداسي حرفين`  **مثـال ~** AAARDA\n"

"⪼  `.صيد سباعيات`  **مثـال ~** AAAARAA\n"

"⪼  `.صيد بوتات`  **مثـال ~** ARDBot\n"

"**⪼ لـ استخـدام الانـواع أرسـل .صيد + النـوع**\n"

"**⪼ مثــال :**\n"

"⪼  `.صيد سداسي حرفين`\n\n\n"

"**- انضـم للقنـاة ~ @hh9hh9**\n"

"**⪼ لـ رؤيـة بعـض اليـوزرات التي قام بصيدهـا منصبيـن كايـدو**"

)





@zedub.zed_cmd(pattern="الصيد")

async def cmd(zelzallll):

    await edit_or_reply(zelzallll, ZelzalChecler_cmd)



@zedub.zed_cmd(pattern="النوع")

async def cmd(zelzallll):

    await edit_or_reply(zelzallll, ZelzalType_cmd)



@zedub.zed_cmd(pattern="صيد (.*)")

async def hunterusername(event):

    choice = str(event.pattern_match.group(1))

    replly = await event.get_reply_message()

    if choice not in ("ثلاثيات", "خماسيات", "خماسي حرفين", "سداسيات", "سداسي حرفين", "سباعي", "بوتات"): #code by t.me/zzzzl1l

        return await event.edit(f"**- عـذرًا عـزيـزي\n- لايوجـد نوع** {choice} \n**- لـ عرض الانواع أرسـل (**`.النوع`**)**")



    try:

        if replly and replly.text.startswith('@'): #Code Update by @zzzzl1l

            ch = replly.text

            await event.edit(f"**𓆰 تم بـدء الصيد .. بنجـاح ☑️**\n**𓆰 النـوع** {choice} \n**𓆰 على القنـاة** {ch} \n**𓆰 لمعرفـة تقـدم عمليـة الصيد (** `.حالة الصيد` **)**\n**𓆰 لـ ايقـاف عمليـة الصيد (** `.ايقاف الصيد` **)**")

        else:

            ch = await zedub(

                functions.channels.CreateChannelRequest(

                    title="⎉ صيـد كايـدو [Smart Guard](https://t.me/SI0lZ) ⎉",

                    about="This channel to hunt username by - @SI0lZ ",

                )

            )

            ch = ch.updates[1].channel_id

            await event.edit(f"**𓆰 تم بـدء الصيد .. بنجـاح ☑️**\n**𓆰 علـى النـوع** {choice} \n**𓆰 لمعرفـة تقـدم عمليـة الصيد (** `.حالة الصيد` **)**\n**𓆰 لـ ايقـاف عمليـة الصيد (** `.ايقاف الصيد` **)**")

    except Exception as e:

        await zedub.send_message(event.chat_id, f"خطأ في انشاء القناة , الخطأ**-  : {str(e)}**")

        zedmod = False



    isclaim.clear()

    isclaim.append("on")

    zedmod = True

    while zedmod: #code by t.me/zzzzl1l

        username = gen_user(choice)

        isav = check_user(username)

        if isav == True:

            try:

                await zedub(

                    functions.channels.UpdateUsernameRequest(

                        channel=ch, username=username

                    )

                )

                await event.client.send_message(

                    event.chat_id,

                    f"- Done : @{username} ✅\n- By : @SI0lZ \n- Hunting Log {trys[0]}",

                )

                await event.client.send_message(

                    "@Sl0IZ", f"- Done : @{username} ✅\n- By : @SI0lZ \n- Hunting Log {trys[0]}",

                )

                zedmod = False

                break

            except telethon.errors.FloodWaitError as e: #code by t.me/zzzzl1l

                await sleep(e.seconds)

                pass

            except telethon.errors.rpcerrorlist.UsernameInvalidError:

                pass

            except Exception as baned:

                if "(caused by UpdateUsernameRequest)" in str(baned):

                    pass

            except telethon.errors.FloodError as e:

                await zedub.send_message(

                    event.chat_id,

                    f"للاسف تبندت , مدة الباند**-  ({e.seconds}) ثانية .**",

                )

                zedmod = False

                break

            except Exception as eee:

                if "the username is already" in str(eee):

                    pass

                if "USERNAME_PURCHASE_AVAILABLE" in str(eee):

                    pass

                else:

                    await zedub.send_message(

                        event.chat_id,

                        f"""- خطأ مع @{username} , الخطأ :{str(eee)}""",

                    )

                    zedmod = False

                    break

        else:

            pass

        trys[0] += 1



    isclaim.clear()

    isclaim.append("off")

    trys[0] = 0

    return await event.client.send_message(event.chat_id, "**- تم الانتهاء من الصيد .. بنجـاح ✅**")





@zedub.zed_cmd(pattern="تثبيت (.*)")

async def _(event):

    zelzal = str(event.pattern_match.group(1))

    if not zelzal.startswith('@'): # Code Update by @zzzzl1l

        return await event.edit("**𓆰 عـذرًا عـزيـزي المدخـل خطـأ ❌**\n**𓆰 استخـدم الامـر كالتالـي**\n**𓆰 أرسـل (**`.تثبيت`** + اليـوزر)**")

    try:

        ch = await zedub(

            functions.channels.CreateChannelRequest(

                title="⎉ تثبيت كايـدو [Smart Guard](https://t.me/SI0lZ) ⎉",

                about="تم تثبيت اليـوزر بواسطـة سـورس كايـدو - @SI0lZ ",

            )

        )

        ch = ch.updates[1].channel_id

        await event.edit(f"**𓆰 تم بـدء التثبيت .. بنجـاح ☑️**\n**𓆰 اليـوزر المثبت ( {zelzal} )**\n**𓆰 لمعرفـة تقـدم عمليـة التثبيت أرسـل (**`.حالة التثبيت`**)**")

    except Exception as e:

        await zedub.send_message(

            event.chat_id, f"خطأ في انشاء القناة , الخطأ**-  : {str(e)}**"

        )

        swapmod = False



    isauto.clear()

    isauto.append("on")

    username = zelzal.replace("@", "")  # Code Update by @zzzzl1l

    swapmod = True

    while swapmod:

        isav = check_user(username)

        if isav == True:

            try:

                await zedub(

                    functions.channels.UpdateUsernameRequest(

                        channel=ch, username=username

                    )

                )

                await event.client.send_message(

                    event.chat_id,

                    f"- Done : @{username} \n- Save: ❲ Channel ❳\n- By : @SI0lZ \n- Hunting Log {trys2[0]}",

                )

                await event.client.send_message(

                    "@Sl0IZ",

                    f"- Done : @{username} \n- Save: ❲ Channel ❳\n- By : @SI0lZ \n- Hunting Log {trys2[0]}",

                )

                swapmod = False

                break

            except telethon.errors.rpcerrorlist.UsernameInvalidError:

                await event.client.send_message(

                    event.chat_id, f"**المعرف @{username} غير صالح ؟!**"

                )

                swapmod = False

                break

            except telethon.errors.FloodError as e:

                await zedub.send_message(

                    event.chat_id, f"للاسف تبندت , مدة الباند ({e.seconds}) ثانية ."

                )

                swapmod = False

                break

            except Exception as eee:

                await zedub.send_message(

                    event.chat_id,

                    f"""خطأ مع {username} , الخطأ :{str(eee)}""",

                )

                swapmod = False

                break

        else:

            pass

        trys2[0] += 1



    isclaim.clear()

    isclaim.append("off")

    trys2[0] = 0

    return await zedub.send_message(event.chat_id, "**- تم الانتهاء من التثبيت .. بنجـاح ✅**")





@zedub.zed_cmd(pattern="ثبت (.*)")

async def _(event): # Code Update by @zzzzl1l

    zelzal = str(event.pattern_match.group(1))

    if not zelzal.startswith('@'): # Code Update by @zzzzl1l

        return await event.edit("**𓆰 عـذرًا عـزيـزي المدخـل خطـأ ❌**\n**𓆰 استخـدم الامـر كالتالـي**\n**𓆰 أرسـل (**`.ثبت`** + اليـوزر)**")

    await event.edit(f"**𓆰 تم بـدء التثبيت .. بنجـاح ☑️**\n**𓆰 اليـوزر المثبت ( {zelzal} )**\n**𓆰 لمعرفـة تقـدم عمليـة التثبيت أرسـل (**`.حالة التثبيت`**)**")

    isouto.clear()

    isouto.append("on")

    username = zelzal.replace("@", "")  # Code Update by @zzzzl1l

    swapmod = True

    while swapmod:

        isav = checker_user(username)

        if isav == True:

            try: # Code Update by @zzzzl1l

                await zedub(functions.account.UpdateUsernameRequest(username=username))

                await event.client.send_message(

                    event.chat_id,

                    f"- Done : @{username} \n- Save: ❲ Account ❳\n- By : @SI0lZ \n- Hunting Log {trys2[0]}",

                )

                await event.client.send_message(

                    "@Sl0IZ",

                    f"- Done : @{username} \n- Save: ❲ Account ❳\n- By : @SI0lZ \n- Hunting Log {trys2[0]}",

                )

                swapmod = False

                break

            except telethon.errors.rpcerrorlist.UsernameInvalidError:

                pass

            except telethon.errors.FloodError as e:

                await zedub.send_message(

                    event.chat_id, f"للاسف تبندت , مدة الباند ({e.seconds}) ثانية ."

                )

                swapmod = False

                break

            except Exception as eee:

                await zedub.send_message(

                    event.chat_id,

                    f"""خطأ مع {username} , الخطأ :{str(eee)}""",

                )

                swapmod = False

                break

        else:

            pass

        trys2[0] += 1



    isclaim.clear()

    isclaim.append("off")

    trys2[0] = 0

    return await zedub.send_message(event.chat_id, "**- تم الانتهاء من التثبيت .. بنجـاح ✅**")







@zedub.zed_cmd(pattern="حالة الصيد")

async def _(event):

    if "on" in isclaim:

        await event.edit(f"**- الصيد وصل لـ({trys[0]}) من المحـاولات**")

    elif "off" in isclaim:

        await event.edit("**- لا توجد عمليـة صيد جاريـة حـالـيًا!**")

    else:

        await event.edit("**- لقد حدث خطأ ما وتوقف الامر لديك**")





@zedub.zed_cmd(pattern="حالة التثبيت")

async def _(event):

    if "on" in isauto:

        await event.edit(f"**- التثبيت وصل لـ({trys2[0]}) من المحاولات**")

    elif "off" in isauto:

        await event.edit("**- لا توجد عمليـة تثبيث جاريـة حـالـيًا!**")

    else:

        await event.edit("-لقد حدث خطأ ما وتوقف الامر لديك")





@zedub.zed_cmd(pattern="ايقاف الصيد")

async def _(event): #code by t.me/zzzzl1l

    if "on" in isclaim:

        isclaim.clear()

        isclaim.append("off")

        trys[0] = 0

        return await event.edit("**- تم إيقـاف عمليـة الصيد .. بنجـاح ✓**")

    elif "off" in isclaim:

        return await event.edit("**𓆰 لا تـوجـد عـملية صـيد جاريـة حـالـيًا .**")

    else:

        return await event.edit("**- لقد حدث خطأ ما وتوقف الامر لديك**")





@zedub.zed_cmd(pattern="ايقاف التثبيت")

async def _(event): #code by t.me/zzzzl1l

    if "on" in isauto:

        isauto.clear()

        isauto.append("off")

        trys2[0] = 0

        return await event.edit("**- تم إيقـاف عمليـة التثبيت .. بنجـاح ✓**")

    elif "off" in isauto:

        return await event.edit("**لا توجـد عمـليـة تثبيت جاريـة حـالـيًا .**")

    else:

        return await event.edit("**-لقد حدث خطأ ما وتوقف الامر لديك**")