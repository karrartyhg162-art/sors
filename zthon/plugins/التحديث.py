import asyncio
import contextlib
import os
import sys
from asyncio.exceptions import CancelledError
from time import sleep

import heroku3
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from zthon import HEROKU_APP, UPSTREAM_REPO_URL, zedub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _zedutils
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)

plugin_category = "الادوات"
cmdhd = Config.COMMAND_HAND_LER
ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger(__name__)
# -- Constants -- #

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
OLDZED = Config.OLDZED
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = "master"

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku application"
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)


# -- Constants End -- #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update_bot(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    sandy = await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**•⎆┊تم التحـديث ⎌ بنجـاح**\n**•⎆┊جـارِ إعـادة تشغيـل بـوت زدثــون ⎋ **\n**•⎆┊انتظـࢪ مـن 2 - 1 دقيقـه . . .📟**")
    await event.client.reload(sandy)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        return await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n **•─────────────────•**\n** ⪼ لم تقـم بوضـع مربـع فـار HEROKU_API_KEY اثنـاء التنصيب وهـذا خطـأ .. قم بضبـط المتغيـر أولاً لتحديث بوت زدثــون ..؟!**", link_preview=False)
    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_applications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n **•─────────────────•**\n** ⪼ لم تقـم بوضـع مربـع فـار HEROKU_APP_NAME اثنـاء التنصيب وهـذا خطـأ .. قم بضبـط المتغيـر أولاً لتحديث بوت زدثــون ..؟!**", link_preview=False)
        repo.__del__()
        return
    heroku_app = next(
        (app for app in heroku_applications if app.name == HEROKU_APP_NAME),
        None,
    )

    if heroku_app is None:
        await event.edit(
            f"{txt}\n" "**- بيانات اعتماد هيروكو غير صالحة لتنصيب تحديث زدثــون**"
        )
        return repo.__del__()
    sandy = await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**✾╎جـارِ . . تنصـيب التحـديث الجـذري ⎌**\n**✾╎يـرجى الانتظـار حتى تنتـهي العمليـة ⎋**\n**✾╎عادة ما يستغرق هـذا التحديث من 5 - 4 دقائـق 📟**")
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS.error(e)
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace(
        "https://", f"https://api:{HEROKU_API_KEY}@"
    )

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**Error log:**\n`{error}`")
        return repo.__del__()
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await edit_delete(
            event, "`Build failed!\n" "Cancelled or there were some errors...`"
        )
    try:
        remote.push("master:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**Here is the error log:**\n`{error}`")
        return repo.__del__()
    await event.edit("`Deploy was failed. So restarting to update`")
    with contextlib.suppress(CancelledError):
        await event.client.disconnect()
        if HEROKU_APP is not None:
            HEROKU_APP.restart()


@zedub.zed_cmd(
    pattern="تحديث(| الان)?$",
    command=("update", plugin_category),
    info={
        "header": "لـ تحـديث بــوت زدثـــون",
        "الاستـخـدام": [
            "{tr}تحديث",
            "{tr}تحديث الان",
            "{tr}تحديث البوت",
        ],
    },
)
async def upstream(event):
    "To check if the bot is up to date and update if specified"
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n**⪼ جاري البحث عن التحديثات  🌐.. ،**")
    off_repo = UPSTREAM_REPO_URL
    force_update = False
    if ENV and (HEROKU_API_KEY is None or HEROKU_APP_NAME is None):
        return await edit_or_reply(
            event, f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n** ⪼ اضبط الفـارات المطلوبة أولاً لتحديث بوت زدثــون ،**"
        )
    try:
        txt = (
            "**- عـذراً .. لا يمكن لبرنامج التحديث المتابعة بسبب** "
            + "**حـدوث بعض المشـاكل**\n\n**تتبع السجل:**\n"
        )

        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\nالدليل {error} غير موجود")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`فشل مبكر! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Unfortunately, the directory {error} does not seem to be a git repository.\nBut we can fix that by force updating the userbot using .update now.`"
            )

        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        return repo.__del__()
    with contextlib.suppress(BaseException):
        repo.create_remote("upstream", off_repo)
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    # Special case for deploy
    if changelog == "" and not force_update:
        await event.edit(
            f"\nᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⪼ سـورس زدثــون محـدث لـ آخـر إصـدار 🛂**"
        )
        return repo.__del__()
    if conf == "" and not force_update:
        return await edit_or_reply(event, f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**•⎆┊يوجـد تحـديث جديـد لسـورس زدثــون ༗...**\n\n**•⎆┊للتحديث السريع اضغـط هنـا ⇜** ⦉ `{cmdhd}تحديث الان` ⦊ \n**•⎆┊للتحديث الجـذري اضغـط هنـا ⇜** ⦉ `{cmdhd}تحديث البوت` ⦊ \n\n𓆩 [𝙎𝙊𝙐𝙍𝘾𝞝 𝙕𝞝𝘿](t.me/Smart Guard) 𓆪")
    if force_update:
        await event.edit(
            "`Force-Syncing to latest stable userbot code, please wait...`"
        )
    if conf == "الان":
        await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**")
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟷𝟶 ▬▭▭▭▭▭▭▭▭▭")
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟸𝟶 ▬▬▭▭▭▭▭▭▭▭")
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟹𝟶 ▬▬▬▭▭▭▭▭▭▭")
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟺𝟶 ▬▬▬▬▭▭▭▭▭▭")
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟻𝟶 ▬▬▬▬▬▭▭▭▭▭")
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟼𝟶 ▬▬▬▬▬▬▭▭▭▭")
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟽𝟶 ▬▬▬▬▬▬▬▭▭▭")
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟾𝟶 ▬▬▬▬▬▬▬▬▭▭") 
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟿𝟶 ▬▬▬▬▬▬▬▬▬▭") 
        await asyncio.sleep(1)
        await event.edit("ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⇜ يتـم تحـديث بـوت زدثــون .. انتظـر . . .🌐**\n\n%𝟷𝟶𝟶 ▬▬▬▬▬▬▬▬▬▬💯") 
        await update_bot(event, repo, ups_rem, ac_br)
    return


@zedub.zed_cmd(
    pattern="تحديث البوت$",
)
async def upstream(event):
    if ENV:
        if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
            return await edit_or_reply(
                event, "`Set the required vars first to update the bot`"
            )
    elif os.path.exists("config.py"):
        return await edit_delete(
            event,
            f"I guess you are on selfhost. For self host you need to use `{cmdhd}update now`",
        )
    event = await edit_or_reply(event, f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**⪼ يتم تنصيب التحديث  انتظر 🌐 ،**")
    off_repo = "https://github.com/Zed-Thon/nekopack"
    os.chdir("/app")
    try:
        txt = (
            "`Oops.. Updater cannot continue due to "
            + "some problems occured`\n\n**LOGTRACE:**\n"
        )

        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`directory {error} is not found`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Early failure! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    with contextlib.suppress(BaseException):
        repo.create_remote("upstream", off_repo)
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit(f"ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - تحـديثـات السـورس\n**•─────────────────•**\n\n**✾╎جـارِ . . تنصـيب التحـديث الجـذري ⎌**\n**✾╎يـرجى الانتظـار حتى تنتـهي العمليـة ⎋**\n**✾╎عادة ما يستغرق هـذا التحديث من 5 - 4 دقائـق 📟**")
    await deploy(event, repo, ups_rem, ac_br, txt)
