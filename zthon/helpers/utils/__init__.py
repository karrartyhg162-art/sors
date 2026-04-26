from .extdl import *
from .paste import *

flag = True
_retry_count = 0
while flag:
    try:
        from . import format as _format
        from . import tools as _zedtools
        from . import utils as _zedutils
        from .events import *
        from .format import *
        from .tools import *
        from .utils import *

        break
    except ModuleNotFoundError as e:
        install_pip(e.name)
        _retry_count += 1
        if _retry_count > 0:
            break
