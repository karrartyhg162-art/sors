# Minimal imghdr implementation for python 3.13 where it was removed.
def what(file, h=None):
    f = None
    try:
        if h is None:
            if isinstance(file, str):
                f = open(file, 'rb')
                h = f.read(32)
            else:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
        for tf in tests:
            res = tf(h, f)
            if res:
                return res
    finally:
        if f: f.close()
    return None

def test_jpeg(h, f):
    if h[6:10] in (b'JFIF', b'Exif'):
        return 'jpeg'
    elif h[:4] in (b'\xff\xd8\xff\xdb', b'\xff\xd8\xff\xee', b'\xff\xd8\xff\xe1', b'\xff\xd8\xff\xe0'):
        return 'jpeg'
    elif h[:2] == b'\xff\xd8':
        return 'jpeg'

def test_png(h, f):
    if h.startswith(b'\211PNG\r\n\032\n'):
        return 'png'

def test_gif(h, f):
    if h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
        return 'gif'

def test_webp(h, f):
    if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return 'webp'

tests = [test_jpeg, test_png, test_gif, test_webp]
