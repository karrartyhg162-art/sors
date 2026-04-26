#حقـوق_مـحمد_مطور_تيبثون
#𝗧𝗘𝗣𝗧𝗛𝗢𝗡
#@PPF22 .
import os
import urllib

from telethon.tl import functions
from zthon import zedub
from zthon.core.managers import edit_delete, edit_or_reply
from zthon.sql_helper.globals import addgvar, gvarstatus

plugin_category = "utils"


OFFLINE_TAG = "- َِ𝘩َِ𝘮َِ𝘥 ."


@zedub.zed_cmd(
    pattern="اسمي حمد$",
    command=("اسمي حمد", plugin_category),
    info={
        "header": "To your status as offline",
        "description": " it change your pic as offline, and add offline tag in name.",
        "usage": "{tr}offline",
    },
)
async def pussy(event):
    "make yourself offline"
    user = await event.client.get_entity("me")
    if user.first_name.startswith(OFFLINE_TAG):
        return await edit_delete(event, "**𓆰 لقد قمت بوضع اسمك مسبقًا**")
    await edit_or_reply(event, "**جـاري وضع اسم حمد على حسابـك**")
    photo = "./temp/donottouch.jpg"
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    urllib.request.urlretrieve(
        "https://graph.org/file/79d163e309f6494c251f2.jpg", photo
    )
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:  # pylint:disable=C0103,W0703
            await edit_or_reply(event, str(e))
        else:
            await edit_or_reply(event, "**𓆰 تم ترتيب اسمك ووضع الصورة**")
    os.remove(photo)
    first_name = user.first_name
    addgvar("my_first_name", first_name)
    addgvar("my_last_name", "")
    if last_name := user.last_name:
        addgvar("my_last_name", last_name)
    tag_name = OFFLINE_TAG
    await event.client(
        functions.account.UpdateProfileRequest(
            last_name=first_name, first_name=tag_name
        )
    )
    await edit_delete(event, f"**`{tag_name} {first_name}`\nانا أنا اسمي حمد.**")


@zedub.zed_cmd(
    pattern="اعادة اسمي$",
    command=("اعادة اسمي", plugin_category),
    info={
        "header": "To your status as online",
        "description": " it change your pic back normal, and remove offline tag in name.",
        "usage": "{tr}online",
    },
)
async def cat(event):
    "make yourself online"
    user = await event.client.get_entity("me")
    if user.first_name.startswith(OFFLINE_TAG):
        await edit_or_reply(event, "**𓆰 تم إعـادة حسـابك إلـى وضعه الأصلي**")
    else:
        await edit_delete(event, "**𓆰 حسابك بالوضع الأصلي فعلًا**")
        return
    try:
        await event.client(
            functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await edit_or_reply(event, str(e))
    else:
        await edit_or_reply(event, "**𓆰 جـاري إعـادة الحـساب كما كـان عليـه سـابقًا..**")
    first_name = gvarstatus("my_first_name")
    last_name = gvarstatus("my_last_name") or ""
    await event.client(
        functions.account.UpdateProfileRequest(
            last_name=last_name, first_name=first_name
        )
    )
    await edit_delete(event, f"**`{first_name} {last_name}`\n𓆰 أنا اسمي حمد**")
    