# -*- coding: utf-8 -*-
import unicodedata


def krutidev_to_unicode(text: str) -> str:
    if not text:
        return ""

    s = " " + text + " "

    # -----------------------------
    # STEP 1: Fix "f" (ि) positioning
    # -----------------------------
    result = []
    i = 0
    while i < len(s):
        if s[i] == 'f':
            if i + 1 < len(s):
                result.append(s[i + 1])
                result.append('ि')
                i += 2
            else:
                result.append('ि')
                i += 1
        else:
            result.append(s[i])
            i += 1
    s = ''.join(result)

    # -----------------------------
    # STEP 2: Fix reph (Z → ्र)
    # -----------------------------
    matras = "ािीुूृेैोौंःँ"
    while "Z" in s:
        i = s.find("Z")
        s = s.replace("Z", "", 1)
        if i > 1 and (i - 1) < len(s) and s[i-1] in matras:
            s = s[:i-2] + "्र" + s[i-2:]
        elif i > 0:
            s = s[:i-1] + "्र" + s[i-1:]
        else:
            s = "्र" + s

    # -----------------------------
    # STEP 3: KrutiDev → Unicode map
    # (sorted by length DESC to avoid partial replace bugs)
    # -----------------------------
    mapping = {
        ";कद्ध": "(घ)",
        ";बद्ध": "(ग)",
        ";इद्ध": "(ख)",
        ";ंद्ध": "(क)",

        "Q+Z": "QZ+",
        "ZZ": "Z",

        "v‚": "ऑ",
        "vks": "ओ",
        "vkS": "औ",
        "vk": "आ",
        "v": "अ",

        "b±": "ईं",
        "Ã": "ई",
        "bZ": "ई",
        "b": "इ",

        "m": "उ",
        "Å": "ऊ",

        ",s": "ऐ",
        ",": "ए",

        "d": "क",
        "Dk": "क",
        "D": "क्",

        "[k": "ख",
        "[": "ख्",

        "x": "ग",
        "Xk": "ग",
        "X": "ग्",

        "?k": "घ",
        "?": "घ्",

        "p": "च",
        "Pk": "च",
        "P": "च्",

        "N": "छ",

        "t": "ज",
        "Tk": "ज",
        "T": "ज्",

        ">": "झ",

        "V": "ट",
        "B": "ठ",
        "M": "ड",
        "<": "ढ",
        ".k": "ण",

        "r": "त",
        "Rk": "त",
        "R": "त्",

        "Fk": "थ",
        "F": "थ्",

        "n": "द",
        "/k": "ध",
        "/": "ध्",

        "u": "न",
        "Uk": "न",
        "U": "न्",

        "i": "प",
        "Ik": "प",
        "I": "प्",

        "Q": "फ",
        "c": "ब",
        "Ck": "ब",
        "C": "ब्",

        "Hk": "भ",
        "H": "भ्",

        "e": "म",
        "Ek": "म",
        "E": "म्",

        ";": "य",
        "j": "र",
        "y": "ल",
        "Yk": "ल",
        "Y": "ल्",

        "G": "ळ",

        "o": "व",
        "Ok": "व",
        "O": "व्",

        "'k": "श",
        "'": "श्",

        "\"k": "ष",
        "\"": "ष्",

        "l": "स",
        "Lk": "स",
        "L": "स्",

        "g": "ह",

        "k": "ा",
        "h": "ी",
        "q": "ु",
        "w": "ू",
        "`": "ृ",
        "s": "े",
        "S": "ै",

        "a": "ं",
        "¡": "ँ",
        "%": "ः",

        "~": "्",
        "-": "-",
        "=": "=",
        "A": "।"
    }

    for k in sorted(mapping, key=len, reverse=True):
        s = s.replace(k, mapping[k])

    # -----------------------------
    # STEP 4: Normalize Unicode
    # -----------------------------
    s = unicodedata.normalize("NFC", s)

    return s.strip()


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    sample = ";ंद्ध ₹ 6150\n;इद्ध ₹ 7687.5\n;बद्ध ₹ 4612.5\n;कद्ध ₹ 3075"
    print(krutidev_to_unicode(sample))
