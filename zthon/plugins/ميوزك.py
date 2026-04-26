# Code For T.me/IQThon
# Edit By T.me/ZedThon
from zthon.core.logger import logging
from telethon import TelegramClient, client, events

from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

import os
try:
    import pytgcalls
    from pytgcalls import idle
    from pytgcalls import PyTgCalls
    from pytgcalls import StreamType
    from pytgcalls.types.input_stream import AudioVideoPiped, AudioPiped
    from pytgcalls.types.input_stream.quality import HighQualityAudio
    from pytgcalls.types.input_stream.quality import HighQualityVideo
    PYTGCALLS_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    PYTGCALLS_AVAILABLE = False
from zthon import zedub

from ..Config import Config
from telethon.sessions import StringSession

import asyncio
LOGS = logging.getLogger(__name__)

new_zedub = TelegramClient(StringSession(Config.STRING_SESSION), Config.APP_ID, Config.API_HASH)

async def PyStart():
    global zedub_py
    try:
        await new_zedub.start()
        zedub_py = PyTgCalls(new_zedub)
        await zedub_py.start()
    except Exception as error:
        print (error)

async def JoinThenStreamVideo(chat_id, StreamFile):
    global zedub_py
    await PyStart()
    await zedub_py.join_group_call(
        int(chat_id),
        AudioVideoPiped(
            StreamFile,
            HighQualityAudio(),
            HighQualityVideo(),
        ),
        stream_type=StreamType().local_stream,
    )
    await idle()
    
async def JoinThenStreamAudio(chat_id, StreamFile):
    global zedub_py
    await PyStart()
    await zedub_py.join_group_call(
        int(chat_id),
        AudioPiped(
            StreamFile,
            HighQualityAudio(),
        ),
        stream_type=StreamType().local_stream,
    )
    await idle()
    
async def LeaveStream(chat_id):
    global zedub_py
    await zedub_py.leave_group_call(
        chat_id,
    )


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@zedub.zed_cmd(pattern="دعوه للمكالمه(?: |$)(.*)")
async def _(e):
    ok = await edit_or_reply(e, "**- جـارِ دعـوة الاشخـاص الى المكالمـه ...**")
    users = []
    z = 0
    async for x in e.client.iter_participants(e.chat_id):
        if not x.bot:
            users.append(x.id)
    hmm = list(user_list(users, 6))
    for p in hmm:
        try:
            await e.client(invitetovc(call=await get_call(e), users=p))
            z += 6
        except BaseException:
            pass
    await ok.edit(f"**- تم انضمـام {z} مستخـدم الى المكالمـه .. بنجـاح ✓**")
@zedub.zed_cmd(pattern="بدء مكالمه(?: |$)(.*)")
async def _(e):
    try:
        await e.client(startvc(e.chat_id))
        await edit_or_reply(e, "**- جـارِ بـدء محـادثـه صـوتيـه ...**")
    except Exception as ex:
        await edit_or_reply(e, f"`{str(ex)}`")



# DOWNLOAD THEN STREAM AUDIO
@zedub.on(events.NewMessage(outgoing=True, pattern=r'.شغل صوت'))
async def AudioFileToVoiceChat(event):
    if event.reply_to != None:
        try:
            from telethon.tl.functions.channels import GetMessagesRequest
            message_media = await event.client(GetMessagesRequest(channel=event.chat_id, id=[event.reply_to.reply_to_msg_id]))
        except:
            from telethon.tl.functions.messages import GetMessagesRequest
            message_media = await event.client(GetMessagesRequest(id=[event.reply_to.reply_to_msg_id]))
            
        try:
            if message_media.messages[0].media != None and str(message_media.messages[0].media.document.mime_type).startswith('audio'):
                edit = await event.edit('**- جـارِ تشغيـل المقطـٓـع الصـٓـوتي ... 🎧♥️**')
                filename = await event.client.download_media(message_media.messages[0], 'audio')
                
                edit = await event.edit("**- تم التشغيل .. بنجـاح 🎧♥️\n\n- قناة السورس : @ZedThon**")
                try:
                    stream = await JoinThenStreamAudio(f'{event.chat_id}', filename)
                    edit = await event.edit('**⎉╎تم .. بنجـاح☑️**')
                except Exception as error:
                    print (error)
                    edit = await event.edit('**⎉╎البث جاري, اذا لم يبدأ اوقف البث و حاول مرة اخرى**')
            else:
                edit = await event.edit('**⎉╎يجب الرد على صوتية**')
                
        except Exception as error:
            edit = await event.edit('**⎉╎يجب الرد على صوتية**')
    else:
        edit = await event.edit('**⎉╎يجب الرد على صوتية**')
    

# DOWNLOAD THEN STREAM VIDEO
@zedub.on(events.NewMessage(outgoing=True, pattern=r'.شغل فيديو'))
async def VideoFileToVoiceChat(event):
    if event.reply_to != None:
        try:
            from telethon.tl.functions.channels import GetMessagesRequest
            message_media = await event.client(GetMessagesRequest(channel=event.chat_id, id=[event.reply_to.reply_to_msg_id]))
        except:
            from telethon.tl.functions.messages import GetMessagesRequest
            message_media = await event.client(GetMessagesRequest(id=[event.reply_to.reply_to_msg_id]))
            
        try:
            if message_media.messages[0].media != None and str(message_media.messages[0].media.document.mime_type).startswith('video'):
                edit = await event.edit('**- جـارِ تشغيـل مقطـٓـع الفيـٓـديو ... 🎧♥️**')
                filename = await event.client.download_media(message_media.messages[0], 'video')
                
                edit = await event.edit("**- تم التشغيل .. بنجـاح 🎧♥️\n\n- قناة السورس : @ZedThon**")
                try:
                    stream = await JoinThenStreamVideo(f'{event.chat_id}', filename)
                    edit = await event.edit('**⎉╎تم .. بنجـاح☑️**')
                except Exception as error:
                    print (error)
                    edit = await event.edit('**⎉╎البث جاري, اذا لم يبدأ اوقف البث و حاول مرة اخرى**')
            else:
                edit = await event.edit('**⎉╎يجب الرد على الفيديو**')
                
        except Exception as error:
            edit = await event.edit('**⎉╎يجب الرد على الفيديو**')
    else:
        edit = await event.edit('**⎉╎يجب الرد على الفيديو**')
