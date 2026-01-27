# -*- coding: utf-8 -*-
import unicodedata

def KrutiDev_to_Unicode(krutidev_substring):
    if not krutidev_substring:
        return ""

    modified_substring = krutidev_substring

    array_one = [
        "ñ","Q+Z","sas","aa",")Z","ZZ","‘","’","“","”",
        "å","ƒ","„","…","†","‡","ˆ","‰","Š","‹",
        "¶+","d+","[+k","[+","x+","T+","t+","M+","<+","Q+",";+","j+","u+",
        "Ùk","Ù","Dr","–","—","é","™","=kk","f=k",
        "à","á","â","ã","ºz","º","í","{k","{","=","«",
        "Nî","Vî","Bî","Mî","<î","|","K","}",
        "J","Vª","Mª","<ªª","Nª","Ø","Ý","nzZ","æ","ç","Á","xz","#",":",
        "v‚","vks","vkS","vk","v","b±","Ã","bZ","b","m","Å",",s",",","_",
        "ô","d","Dk","D","[k","[","x","Xk","X","Ä","?k","?","³",
        "pkS","p","Pk","P","N","t","Tk","T",">","÷","¥",
        "ê","ë","V","B","ì","ï","M+","<+","M","<",".k",".",
        "r","Rk","R","Fk","F",")","n","/k","èk","/","Ë","è","u","Uk","U",
        "i","Ik","I","Q","¶","c","Ck","C","Hk","H","e","Ek","E",
        ";","¸","j","y","Yk","Y","G","o","Ok","O",
        "'k","'","\"k","\"","l","Lk","L","g",
        "È","z",
        "‚","ks","kS","k","h","q","w","`","s","S",
        "a","¡","%","W","~","-","A"
    ]

    array_two = [
        "॰","QZ+","sa","a","र्द्ध","Z","\"","\"","'","'",
        "०","१","२","३","४","५","६","७","८","९",
        "फ़्","क़","ख़","ख़्","ग़","ज़्","ज़","ड़","ढ़","फ़","य़","ऱ","ऩ",
        "त्त","त्त्","क्त","दृ","कृ","न्न","न्न्","=k","f=",
        "ह्न","ह्य","हृ","ह्म","ह्र","ह्","द्द","क्ष","क्ष्","त्र","त्र्",
        "छ्य","ट्य","ठ्य","ड्य","ढ्य","द्य","ज्ञ","द्व",
        "श्र","ट्र","ड्र","ढ्र","छ्र","क्र","फ्र","र्द्र","द्र","प्र","प्र","ग्र","रु","रू",
        "ऑ","ओ","औ","आ","अ","ईं","ई","ई","इ","उ","ऊ","ऐ","ए","ऋ",
        "क्क","क","क","क्","ख","ख्","ग","ग","ग्","घ","घ","घ्","ङ",
        "चै","च","च","च्","छ","ज","ज","ज्","झ","झ्","ञ",
        "ट्ट","ट्ठ","ट","ठ","ड्ड","ड्ढ","ड़","ढ़","ड","ढ","ण","ण्",
        "त","त","त्","थ","थ्","द्ध","द","ध","ध","ध्","ध्","ध्","न","न","न्",
        "प","प","प्","फ","फ्","ब","ब","ब्","भ","भ्","म","म","म्",
        "य","य्","र","ल","ल","ल्","ळ","व","व","व्",
        "श","श्","ष","ष्","स","स","स्","ह",
        "ीं","्र",
        "ॉ","ो","ौ","ा","ी","ु","ू","ृ","े","ै",
        "ं","ँ","ः","ॅ","्","-","।"
    ]

    # ---- Fix 'f' matra (ि) ----
    modified_substring = " " + modified_substring + " "
    while "f" in modified_substring:
        pos = modified_substring.find("f")
        if pos > 0:
            modified_substring = (
                modified_substring[:pos]
                + modified_substring[pos+1]
                + "f"
                + modified_substring[pos+2:]
            )
        else:
            break
    modified_substring = modified_substring.replace("f", "ि").strip()

    # ---- Fix reph (Z) ----
    modified_substring = " " + modified_substring + " "
    while "Z" in modified_substring:
        pos = modified_substring.find("Z")
        modified_substring = modified_substring.replace("Z", "", 1)
        if pos > 1:
            modified_substring = (
                modified_substring[:pos-1]
                + "्र"
                + modified_substring[pos-1:]
            )
    modified_substring = modified_substring.strip()

    # ---- Replace KrutiDev glyphs ----
    for i in range(len(array_one)):
        modified_substring = modified_substring.replace(
            array_one[i], array_two[i]
        )

    return unicodedata.normalize("NFC", modified_substring)
