# -*- coding: utf-8 -*-
import re
import unicodedata

# -------------------------------------------------
# KrutiDev 010 → Unicode mapping (cleaned & ordered)
# -------------------------------------------------

ARRAY_ONE = [
    "Q+Z","sas","aa",")Z","ZZ",
    "‘","’","“","”",
    "å","ƒ","„","…","†","‡","ˆ","‰","Š","‹",
    "¶+","d+","[+k","[+","x+","T+","t+","M+","<+","Q+",";+","j+","u+",
    "Ùk","Ù","Dr","–","—","é","™",
    "Nî","Vî","Bî","Mî","<î","|","K","}",
    "J","Vª","Mª","<ªª","Nª","Ø","Ý","nzZ","æ","ç","Á","xz",
    "v‚","vks","vkS","vk","v",
    "b±","Ã","bZ","b","m","Å",
    ",s",",","_",
    "pkS","p","Pk","P","N",
    "t","Tk","T",
    "V","B","M","<",
    ".k",".",
    "r","Rk","R","Fk","F",
    "n","/k","èk","/","Ë","è",
    "u","Uk","U",
    "i","Ik","I",
    "Q","¶",
    "c","Ck","C",
    "Hk","H",
    "e","Ek","E",
    ";","j",
    "y","Yk","Y",
    "G","o","Ok","O",
    "'k","'",
    "\"k","\"",
    "l","Lk","L",
    "g",
    "z",
    "‚","ks","kS","k","h",
    "q","w","`","s","S",
    "a","¡","%","W","~","-","A"
]

ARRAY_TWO = [
    "QZ+","sa","a","र्द्ध","Z",
    "“","”","‘","’",
    "०","१","२","३","४","५","६","७","८","९",
    "फ़्","क़","ख़","ख़्","ग़","ज़्","ज़","ड़","ढ़","फ़","य़","ऱ","ऩ",
    "त्त","त्त्","क्त","दृ","कृ","न्न","न्न्",
    "छ्य","ट्य","ठ्य","ड्य","ढ्य","द्य","ज्ञ","द्व",
    "श्र","ट्र","ड्र","ढ्र","छ्र","क्र","फ्र","र्द्र","द्र","प्र","प्र","ग्र",
    "ऑ","ओ","औ","आ","अ",
    "ईं","ई","ई","इ","उ","ऊ",
    "ऐ","ए","ऋ",
    "चै","च","च","च्","छ",
    "ज","ज","ज्",
    "ट","ठ","ड","ढ",
    "ण","ण्",
    "त","त","त्","थ","थ्",
    "द","ध","ध","ध","ध्","ध्",
    "न","न","न्",
    "प","प","प्",
    "फ","फ्",
    "ब","ब","ब्",
    "भ","भ्",
    "म","म","म्",
    "य","र",
    "ल","ल","ल्",
    "ळ","व","व","व्",
    "श","श्",
    "ष","ष्",
    "स","स","स्",
    "ह",
    "्र",
    "ॉ","ो","ौ","ा","ी",
    "ु","ू","ृ","े","ै",
    "ं","ँ","ः","ॅ","्","-","।"
]

# Pre-sort replacements (LONGEST FIRST — CRITICAL)
REPLACEMENTS = sorted(
    zip(ARRAY_ONE, ARRAY_TWO),
    key=lambda x: -len(x[0])
)

# -------------------------------------------------
# Main converter
# -------------------------------------------------

def krutidev_to_unicode(text: str) -> str:
    if not text:
        return ""

    # STEP 1: Glyph replacement (visual → logical)
    for src, tgt in REPLACEMENTS:
        text = text.replace(src, tgt)

    # STEP 2: Fix Reph (Z → र् before consonant cluster)
    # Example: kZ → र्क
    text = re.sub(r'Z([क-ह])', r'र्\1', text)

    # STEP 3: Fix pre-base matra "ि"
    # Visual order: िक  → Logical: कि
    text = re.sub(r'ि([क-ह])', r'\1ि', text)

    # STEP 4: Unicode normalization
    return unicodedata.normalize("NFC", text)


# -------------------------------------------------
# Test (your exact example)
# -------------------------------------------------
if __name__ == "__main__":
    sample = ";fn ,d iafDr esa ,d O;fDr nk;ha vksj ls 6osa vkSj ck;ha vksj ls 8osa LFkku ij cSBk gS]"
    print(krutidev_to_unicode(sample))
