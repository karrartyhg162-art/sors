import os
import re
import urllib.request
from collections import defaultdict

import ujson
import yt_dlp
from telethon import Button
from yt_dlp.utils import DownloadError, ExtractorError, GeoRestrictedError

from ...Config import Config
from ...core import pool
from ...core.logger import logging
from ..aiohttp_helper import AioHttp
from ..progress import humanbytes
from .functions import sublists

LOGS = logging.getLogger(__name__)
BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./zthon/cache/ytsearch.json"

song_dl = "yt-dlp --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o './temp/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --audio-quality {QUALITY} {video_link}"

thumb_dl = "yt-dlp --force-ipv4 -o './temp/%(title)s.%(ext)s' --write-thumbnail --skip-download {video_link}"
video_dl = "yt-dlp --force-ipv4 --write-thumbnail --add-metadata --embed-thumbnail -o './temp/%(title)s.%(ext)s' -f 'best[height<=480]' {video_link}"
name_dl = (
    "yt-dlp --force-ipv4 --get-filename -o './temp/%(title)s.%(ext)s' {video_link}"
)


async def yt_search(zed):
    try:
        zed = urllib.parse.quote(zed)
        html = urllib.request.urlopen(
            f"https://www.youtube.com/results?search_query={zed}"
        )

        user_data = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_link = []
        k = 0
        for i in user_data:
            if user_data:
                video_link.append(f"https://www.youtube.com/watch?v={user_data[k]}")
            k += 1
            if k > 3:
                break
        if video_link:
            return video_link[0]
        return "Couldnt fetch results"
    except Exception:
        return "Couldnt fetch results"


def _format_duration_hms(seconds):
    if seconds is None:
        return "غير معروف"
    try:
        sec = int(float(seconds))
    except (TypeError, ValueError):
        return "غير معروف"
    if sec < 0:
        return "غير معروف"
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def _view_count_short(n):
    if n is None:
        return "N/A"
    try:
        n = int(n)
    except (TypeError, ValueError):
        return "N/A"
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def _ytdlp_search_legacy_entries(query: str, limit: int = 15) -> list:
    """YouTube text search via yt-dlp; shapes entries like youtube-search-python for result_formatter."""
    opts = {
        "quiet": True,
        "noplaylist": True,
        "extract_flat": "in_playlist",
        "socket_timeout": 30,
        "ignoreerrors": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(f"ytsearch{int(limit)}:{query}", download=False)
    except Exception as err:
        LOGS.warning("YouTube search (yt-dlp) failed: %s", err)
        return []
    entries = (info or {}).get("entries") or []
    out = []
    for ent in entries:
        if not ent or not ent.get("id"):
            continue
        vid = str(ent["id"])
        if len(vid) != 11:
            continue
        link = ent.get("url") or (BASE_YT_URL + vid)
        if isinstance(link, str) and link.startswith("/watch"):
            link = "https://www.youtube.com" + link
        title = ent.get("title") or ""
        desc = (ent.get("description") or "").strip()
        snippet = [{"text": desc[:600]}] if desc else [{"text": ""}]
        dur_str = _format_duration_hms(ent.get("duration"))
        vc_short = _view_count_short(ent.get("view_count"))
        ud = ent.get("upload_date")
        if ud and len(str(ud)) == 8:
            uds = str(ud)
            published = f"{uds[:4]}-{uds[4:6]}-{uds[6:8]}"
        else:
            published = "—"
        ch_name = ent.get("channel") or ent.get("uploader") or ""
        ch_url = ent.get("channel_url") or ent.get("uploader_url") or ""
        if ch_name and not ch_url:
            ch_url = "https://www.youtube.com"
        acc_title = title if len(title) <= 100 else (title[:97] + "...")
        out.append(
            {
                "id": vid,
                "link": link,
                "title": title,
                "descriptionSnippet": snippet,
                "accessibility": {"duration": dur_str, "title": acc_title},
                "viewCount": {"short": vc_short},
                "publishedTime": published,
                "channel": ({"name": ch_name, "link": ch_url} if ch_name else None),
            }
        )
    return out


@pool.run_in_thread
def ytdlp_search_legacy_entries(query: str, limit: int = 15) -> list:
    return _ytdlp_search_legacy_entries(query.strip(), limit)


async def youtube_inline_search_formatted(query: str, limit: int = 15):
    """Text search for inline ytdl; returns result_formatter dict or None."""
    resp = await ytdlp_search_legacy_entries(query, limit)
    if not resp:
        return None
    return await result_formatter(resp)


@pool.run_in_thread
def _ytsp_search(query: str, limit: int):
    try:
        from youtubesearchpython import VideosSearch
        return VideosSearch(query, limit=limit).result().get('result', [])
    except Exception as err:
        LOGS.warning("YouTube search (ytsp) failed: %s", err)
        return []

async def ytsearch(query, limit):
    result = ""
    try:
        results = await _ytsp_search(query.strip(), limit)
        for v in results:
            title = v.get('title', 'Unknown')
            link = v.get('link', '')
            textresult = f"[{title}]({link})\n"
            try:
                ds = v.get("descriptionSnippet") or []
                snippet_text = "".join(x.get("text", "") for x in ds) if ds else "None"
                textresult += f"**- الوصـف : **`{snippet_text}`\n"
            except Exception:
                textresult += "**- الوصـف : **`None`\n"
            
            duration = v.get("duration", "N/A")
            views = v.get("viewCount", {}).get("short", "N/A") if v.get("viewCount") else "N/A"
            textresult += f"**- المـده : **{duration}  **- المشـاهـدات : **{views}\n"
            result += f"☞ {textresult}\n"
        if not result:
            raise Exception("No results from ytsp")
        return result
    except Exception as e:
        LOGS.warning(f"Falling back to legacy search due to: {e}")
        legacy = await ytdlp_search_legacy_entries(query.strip(), limit)
        for v in legacy:
            textresult = f"[{v['title']}]({v['link']})\n"
            try:
                ds = v.get("descriptionSnippet") or []
                snippet_text = "".join(x.get("text", "") for x in ds)
                textresult += f"**- الوصـف : **`{snippet_text}`\n"
            except Exception:
                textresult += "**- الوصـف : **`None`\n"
            textresult += f"**- المـده : **{v['accessibility']['duration']}  **- المشـاهـدات : **{v['viewCount']['short']}\n"
            result += f"☞ {textresult}\n"
        return result


class YT_Search_X:
    def __init__(self):
        if not os.path.exists(PATH):
            with open(PATH, "w") as f_x:
                ujson.dump({}, f_x)
        with open(PATH) as yt_db:
            self.db = ujson.load(yt_db)

    def store_(self, rnd_id: str, results: dict):
        self.db[rnd_id] = results
        self.save()

    def save(self):
        with open(PATH, "w") as outfile:
            ujson.dump(self.db, outfile, indent=4)


ytsearch_data = YT_Search_X()

"""
async def yt_data(zed):
    params = {"format": "json", "url": zed}
    url = "https://www.youtube.com/oembed"  # https://stackoverflow.com/questions/29069444/returning-the-urls-as-a-list-from-a-youtube-search-query
    query_string = urllib.parse.urlencode(params)
    url = f"{url}?{query_string}"
    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = ujson.loads(response_text.decode())
    return data
"""


async def get_ytthumb(videoid: str):
    thumb_quality = [
        "maxresdefault.jpg",  # Best quality
        "hqdefault.jpg",
        "sddefault.jpg",
        "mqdefault.jpg",
        "default.jpg",  # Worst quality
    ]
    thumb_link = "https://i.imgur.com/4LwPLai.png"
    for qualiy in thumb_quality:
        link = f"https://i.ytimg.com/vi/{videoid}/{qualiy}"
        if await AioHttp().get_status(link) == 200:
            thumb_link = link
            break
    return thumb_link


def get_yt_video_id(url: str):
    if match := YOUTUBE_REGEX.search(url):
        return match.group(1)


# Based on https://gist.github.com/AgentOak/34d47c65b1d28829bb17c24c04a0096f
def get_choice_by_id(choice_id, media_type: str):
    if choice_id == "mkv":
        # default format selection
        choice_str = "bestvideo+bestaudio/best"
        disp_str = "best(video+audio)"
    elif choice_id == "mp3":
        choice_str = "320"
        disp_str = "320 Kbps"
    elif choice_id == "mp4":
        # Download best Webm / Mp4 format available or any other best if no mp4
        # available
        choice_str = "bestvideo[ext=webm]+251/bestvideo[ext=mp4]+(258/256/140/bestaudio[ext=m4a])/bestvideo[ext=webm]+(250/249)/best"
        disp_str = "best(video+audio)[webm/mp4]"
    else:
        disp_str = str(choice_id)
        choice_str = (
            f"{disp_str}+(258/256/140/bestaudio[ext=m4a])/best"
            if media_type == "v"
            else disp_str
        )

    return choice_str, disp_str


async def result_formatter(results: list):
    output = {}
    for index, r in enumerate(results, start=1):
        v_deo_id = r.get("id")
        thumb = await get_ytthumb(v_deo_id)
        upld = r.get("channel")
        title = f'<a href={r.get("link")}><b>{r.get("title")}</b></a>\n'
        out = title
        if r.get("descriptionSnippet"):
            out += "<code>{}</code>\n\n".format(
                "".join(x.get("text") for x in r.get("descriptionSnippet"))
            )
        out += f'<b>❯  المـده :</b> {r.get("accessibility").get("duration")}\n'
        views = f'<b>❯  المشـاهـدات :</b> {r.get("viewCount").get("short")}\n'
        out += views
        out += f'<b>❯  تاريـخ الرفـع :</b> {r.get("publishedTime")}\n'
        if upld:
            out += "<b>❯  القنـاة :</b> "
            out += f'<a href={upld.get("link")}>{upld.get("name")}</a>'

        output[index] = dict(
            message=out,
            thumb=thumb,
            video_id=v_deo_id,
            list_view=f'<img src={thumb}><b><a href={r.get("link")}>{index}. {r.get("accessibility").get("title")}</a></b><br>',
        )

    return output


def yt_search_btns(
    data_key: str, page: int, vid: str, total: int, del_back: bool = False
):
    buttons = [
        [
            Button.inline(
                text="رجـوع ⬅️",
                data=f"ytdl_back_{data_key}_{page}",
            ),
            Button.inline(
                text=f"{page} / {total}",
                data=f"ytdl_next_{data_key}_{page}",
            ),
        ],
        [
            Button.inline(
                text="عرض الكل 📜",
                data=f"ytdl_listall_{data_key}_{page}",
            ),
            Button.inline(
                text="⬇️ تحميـل",
                data=f"ytdl_download_{vid}_0",
            ),
        ],
    ]
    if del_back:
        buttons[0].pop(0)
    return buttons


@pool.run_in_thread
def download_button(vid: str, body: bool = False):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    try:
        vid_data = yt_dlp.YoutubeDL({"no-playlist": True}).extract_info(
            BASE_YT_URL + vid, download=False
        )
    except ExtractorError:
        vid_data = {"formats": []}
    buttons = [
        [
            Button.inline("⭐️ اعلى دقـه - 📹 MKV", data=f"ytdl_download_{vid}_mkv_v"),
            Button.inline(
                "⭐️ اعلى دقـه - 📹 WebM/MP4",
                data=f"ytdl_download_{vid}_mp4_v",
            ),
        ]
    ]
    # ------------------------------------------------ #
    qual_dict = defaultdict(lambda: defaultdict(int))
    qual_list = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p"]
    audio_dict = {}
    # ------------------------------------------------ #
    for video in vid_data["formats"]:
        if video.get("filesize"):
            fr_note = video.get("format_note")
            fr_id = int(video.get("format_id"))
            fr_size = video.get("filesize")
            if video.get("ext") == "mp4":
                for frmt_ in qual_list:
                    if fr_note in (frmt_, f"{frmt_}60"):
                        qual_dict[frmt_][fr_id] = fr_size
            if video.get("acodec") != "none":
                bitrrate = int(video.get("abr", 0))
                if bitrrate != 0:
                    audio_dict[
                        bitrrate
                    ] = f"🎵 {bitrrate}Kbps ({humanbytes(fr_size) or 'N/A'})"

    video_btns = []
    for frmt in qual_list:
        frmt_dict = qual_dict[frmt]
        if len(frmt_dict) != 0:
            frmt_id = sorted(list(frmt_dict))[-1]
            frmt_size = humanbytes(frmt_dict.get(frmt_id)) or "N/A"
            video_btns.append(
                Button.inline(
                    f"📹 {frmt} ({frmt_size})",
                    data=f"ytdl_download_{vid}_{frmt_id}_v",
                )
            )
    buttons += sublists(video_btns, width=2)
    buttons += [
        [Button.inline("⭐️ اعلى دقـه - 🎵 320Kbps - MP3", data=f"ytdl_download_{vid}_mp3_a")]
    ]
    buttons += sublists(
        [
            Button.inline(audio_dict.get(key_), data=f"ytdl_download_{vid}_{key_}_a")
            for key_ in sorted(audio_dict.keys())
        ],
        width=2,
    )
    if body:
        vid_body = f"<a href={vid_data.get('webpage_url')}><b>[{vid_data.get('title')}]</b></a>"
        return vid_body, buttons
    return buttons


@pool.run_in_thread
def _tubeDl(url: str, starttime, uid: str):
    ydl_opts = {
        "addmetadata": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "outtmpl": os.path.join(
            Config.TEMP_DIR, str(starttime), "%(title)s-%(format)s.%(ext)s"
        ),
        #         "logger": LOGS,
        "format": uid,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "postprocessors": [
            {"key": "FFmpegMetadata"}
            # ERROR R15: Memory quota vastly exceeded
            # {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        ],
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            x = ydl.download([url])
    except DownloadError as e:
        LOGS.error(e)
    except GeoRestrictedError:
        LOGS.error("هذا الفيديو غير متاح  في بلدك")
    else:
        return x


@pool.run_in_thread
def _mp3Dl(url: str, starttime, uid: str):
    _opts = {
        "outtmpl": os.path.join(Config.TEMP_DIR, str(starttime), "%(title)s.%(ext)s"),
        #         "logger": LOGS,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "format": "bestaudio/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": uid,
            },
            {"key": "EmbedThumbnail"},  # ERROR: Conversion failed!
            {"key": "FFmpegMetadata"},
        ],
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(_opts) as ytdl:
            dloader = ytdl.download([url])
    except Exception as y_e:
        LOGS.exception(y_e)
        return y_e
    else:
        return dloader
