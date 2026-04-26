from . import fonts
from . import memeshelper as catmemes
from .aiohttp_helper import AioHttp
from .utils import *

flag = True
_retry_count = 0
while flag:
    try:
        from .chatbot import *
        from .functions import *
        from .memeifyhelpers import *
        from .progress import *
        from .qhelper import process
        from .tools import *
        from .utils import _zedtools, _zedutils, _format

        break
    except ModuleNotFoundError as e:
        install_pip(e.name)
        _retry_count += 1
        if _retry_count > 0:
            break
