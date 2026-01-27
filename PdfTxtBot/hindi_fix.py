# -*- coding: utf-8 -*-
import re
import unicodedata

# -------------------------------------------------
# KrutiDev / legacy Hindi → Unicode converter
# -------------------------------------------------

KRUTI_MAP = {
    "Ø": "।",
    "Ù": "‘",
    "Ú": "’",
    "Û": "“",
    "Ü": "”",
    "æ": "ं",
    "ç": "ः",
    "é": "अ",
    "ê": "आ",
    "ë": "इ",
    "ì": "ई",
    "í": "उ",
    "î": "ऊ",
    "ï": "ऋ",
    "ð": "ए",
    "ñ": "ऐ",
    "ò": "ओ",
    "ó": "औ",
    "ô": "क",
    "õ": "ख",
    "ö": "ग",
    "÷": "घ",
    "ø": "च",
    "ù": "छ",
    "ú": "ज",
    "û": "झ",
    "ü": "ट",
    "ý": "ठ",
    "þ": "ड",
    "ÿ": "ढ",
    "À": "ण",
    "Á": "त",
    "Â": "थ",
    "Ã": "द",
    "Ä": "ध",
    "Å": "न",
    "Æ": "प",
    "Ç": "फ",
    "È": "ब",
    "É": "भ",
    "Ê": "म",
    "Ë": "य",
    "Ì": "र",
    "Í": "ल",
    "Î": "व",
    "Ï": "श",
    "Ð": "ष",
    "Ñ": "स",
    "Ò": "ह",
    "Ó": "ा",
    "Ô": "ि",
    "Õ": "ी",
    "Ö": "ु",
    "×": "ू",
    "Ø": "ृ",
    "Ù": "े",
    "Ú": "ै",
    "Û": "ो",
    "Ü": "ौ",
    "Ý": "्",
}

# -------------------------------------------------
# Post processing cleanup (VERY IMPORTANT)
# -------------------------------------------------

def clean_hindi_text(text: str) -> str:
    if not text:
        return ""

    # remove duplicate halants
    while "््" in text:
        text = text.replace("््", "्")

    # fix reph duplication
    text = text.replace("्र्र", "्र")

    # fix misplaced chhoti ee
    text = text.replace("ि्", "्ि")

    # punctuation fixes
    text = text.replace("।।", "।")
    text = text.replace("..", "।")

    # normalize spaces
    while "  " in text:
        text = text.replace("  ", " ")

    # clean lines (questions stay clean)
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            lines.append(line)

    return "\n".join(lines)


# -------------------------------------------------
# MAIN FUNCTION (this is what bot imports)
# -------------------------------------------------

def krutidev_to_unicode(text: str) -> str:
    if not text:
        return ""

    # Step 1: map characters
    output = []
    for ch in text:
        output.append(KRUTI_MAP.get(ch, ch))
    text = "".join(output)

    # Step 2: normalize unicode
    text = unicodedata.normalize("NFC", text)

    # Step 3: final cleanup
    return clean_hindi_text(text)
