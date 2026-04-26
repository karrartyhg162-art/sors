#!/usr/bin/env python3
"""
Rebrand script: Kaido → [Smart Guard](https://t.me/SI0lZ) | الحارس الذكي
Developer: @Sl0IZ (ID: 6726762505)
Channel: @SI0lZ

Only replaces in string literals and comments.
Does NOT touch variable names, function names, or file paths on disk.
"""
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r"c:\Users\LOQ\Desktop\Source-main"

# Order matters: longest/most-specific patterns FIRST
REPLACEMENTS = [
    # ── 1. URLs (most specific first) ──
    ("https://t.me/Tws_kaido_q/59", "https://t.me/SI0lZ"),
    ("https://t.me/Tws_kaido_q/63", "https://t.me/SI0lZ"),
    ("https://t.me/Tws_kaido_q",    "https://t.me/SI0lZ"),
    ("https://t.me/kaido_qklaesh",  "https://t.me/SI0lZ"),
    ("https://t.me/kaido_qe1",      "https://t.me/SI0lZ"),
    ("https://t.me/kaido_q",        "https://t.me/SI0lZ"),
    ("https://t.me/kaido_c",        "https://t.me/SI0lZ"),
    ("https://t.me/HAIDAR_MY",      "https://t.me/Sl0IZ"),
    ("https://t.me/HAIDAR_TM0",     "https://t.me/Sl0IZ"),

    # t.me without https://
    ("t.me/Tws_kaido_q",    "t.me/SI0lZ"),
    ("t.me/kaido_qklaesh",  "t.me/SI0lZ"),
    ("t.me/kaido_qe1",      "t.me/SI0lZ"),
    ("t.me/kaido_q",        "t.me/SI0lZ"),
    ("t.me/kaido_c",        "t.me/SI0lZ"),
    ("t.me/HAIDAR_MY",      "t.me/Sl0IZ"),
    ("t.me/HAIDAR_TM0",     "t.me/Sl0IZ"),

    # ── 2. @usernames ──
    ("@HAIDAR_TM0", "@Sl0IZ"),
    ("@HAIDAR_MY",  "@Sl0IZ"),
    ("@kaido_q",    "@SI0lZ"),
    ("@kaido_c",    "@SI0lZ"),

    # ── 3. Bare usernames in lists/sets (quoted) ──
    ('"HAIDAR_TM0"', '"Sl0IZ"'),
    ('"kaido_q"',    '"SI0lZ"'),
    ('"kaido_c"',    '"SI0lZ"'),

    # ── 4. Styled-text brand names (longest first) ──
    ("سورس كايدو العربي - KAIDO USERBOT", "[Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("𝗞𝗮𝗶𝗱𝗼 𝗨𝘀𝗲𝗿𝗯𝗼𝘁",                    "[Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("KAIDO USERBOT",                       "[Smart Guard](https://t.me/SI0lZ)"),
    ("ڪٱيدّو 𝐾𝐴𝐼𝐷𝑂🜢",                     "[Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("ڪٱيدّو 𝐾𝐴𝐼𝐷𝑂",                       "[Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("𝙎𝙊𝙐𝙍𝘾𝞝 𝗞𝗔𝗜𝗗𝗢",                      "[Smart Guard](https://t.me/SI0lZ)"),
    ("𝗦𝗼𝘂𝗿𝗰𝗲 𝗞𝗮𝗶𝗱𝗼",                      "[Smart Guard](https://t.me/SI0lZ)"),
    ("𝗞𝗮𝗶𝗱𝗼",                               "[Smart Guard](https://t.me/SI0lZ)"),
    ("𝗞𝗔𝗜𝗗𝗢",                               "[Smart Guard](https://t.me/SI0lZ)"),
    ("𝐾𝐴𝐼𝐷𝑂",                               "[Smart Guard](https://t.me/SI0lZ)"),
    ("ڪٱيدّو",                              "الحارس الذكي"),

    # ── 5. Arabic brand names (longest first) ──
    ("سورس كايدو العربي",   "[Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("سـورس كايدو",         "[Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("سورس كايدو",          "[Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("لســورس كايدو",       "لـ [Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("بسـورس كايدو",        "بـ [Smart Guard](https://t.me/SI0lZ) | الحارس الذكي"),
    ("بـوت كايدو",          "بـوت الحارس الذكي"),
    ("كــلايــش كايدو",     "قنـاة الحارس الذكي"),
    ("كـاتب كايدو",         "كـاتب الحارس الذكي"),
    ("قنـوات كايدو",        "قنـوات الحارس الذكي"),
    ("قنـوات كـايـدو",      "قنـوات الحارس الذكي"),
    ("كـايـدو",             "الحارس الذكي"),
    ("كايدو",               "الحارس الذكي"),

    # ── 6. English brand in strings (handled line-by-line to skip file paths) ──
    # Will be handled specially below

    # ── 7. Developer name replacements in strings ──
    ("𝙈𝙊𝙃𝘼𝙈𝙈𝘼𝘿",    "Sl0IZ"),
    ("مطوري حيدر",    "المطور @Sl0IZ"),
    ("عزيزي باقر",    "عزيزي @Sl0IZ"),
    ("[حيدر]",        "[@Sl0IZ]"),
    ("[HAIDAR]",      "[@Sl0IZ]"),
    ("𝗱𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿",   "𝗱𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿"),  # keep as-is (this is just the word "developer")
    
    # ── 8. Old developer ID (if present) ──
    # Add any old developer IDs here if needed
]

# "Kaido" / "kaido" must skip file path lines (kaido.jpg, kaido1.jpg)
ENGLISH_REPLACEMENTS = [
    ("Kaido", "[Smart Guard](https://t.me/SI0lZ)"),
]

PROTECTED_SUBSTRINGS = ["kaido.jpg", "kaido1.jpg", "kaido2.jpg"]


def process_file(filepath):
    """Process a single .py file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"  [X] Read error: {filepath} -> {e}")
        return False

    original = content

    # Phase 1: bulk replacements (safe – patterns only appear in strings/comments)
    for old, new in REPLACEMENTS:
        if old != new and old in content:
            content = content.replace(old, new)

    # Phase 2: English "Kaido" – line-by-line to protect file paths
    for old, new in ENGLISH_REPLACEMENTS:
        if old in content:
            lines = content.split("\n")
            new_lines = []
            for line in lines:
                if any(p in line for p in PROTECTED_SUBSTRINGS):
                    new_lines.append(line)          # keep file-path lines intact
                else:
                    new_lines.append(line.replace(old, new))
            content = "\n".join(new_lines)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    modified = 0
    scanned = 0
    for dirpath, _, filenames in os.walk(ROOT):
        # Skip hidden/venv dirs
        if any(skip in dirpath for skip in [".git", "__pycache__", "venv", ".env"]):
            continue
        for fn in filenames:
            if fn.endswith(".py") and fn != "rebrand.py":
                fp = os.path.join(dirpath, fn)
                scanned += 1
                if process_file(fp):
                    modified += 1
                    print(f"  [OK] {fp}")

    print(f"\n{'='*50}")
    print(f"  Scanned : {scanned} files")
    print(f"  Modified: {modified} files")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
