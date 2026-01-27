
import os

def kruti_to_unicode(text):
    # Mapping for Kruti Dev 010 to Unicode
    # Note: Kruti Dev is highly positional, but for simple .txt files
    # a character-to-character mapping covers the majority of cases.
    kd_map = {
        "k": "ा", "i": "य", "h": "ी", "A": "अ", "B": "इ", "C": "ई", "D": "उ", "E": "ऊ", "F": "ए", "G": "ऐ", "H": "ओ", "I": "औ",
        "J": "क", "K": "ख", "L": "ग", "M": "घ", "N": "ङ", "O": "च", "P": "छ", "Q": "ज", "R": "झ", "S": "ञ", "T": "ट", "U": "ठ", "V": "ड", "W": "ढ", "X": "ण", "Y": "त", "Z": "थ",
        "a": "द", "b": "ध", "c": "न", "d": "प", "e": "फ", "f": "ि", "g": "भ", "h": "म", "j": "र", "l": "व", "m": "श", "n": "ष", "o": "स", "p": "ह",
        "q": "ा", "r": "ि", "s": "ी", "t": "ु", "u": "ू", "v": "ृ", "w": "े", "x": "ै", "y": "ो", "z": "ौ",
        ";": "य", "fn": "दि", "ia": "पं", "fDr": "क्ति", "esa": "में", "vksj": "ओर", "LFkku": "स्थान", "O;fDr": "व्यक्ति", "iafDr": "पंक्ति",
        "ls": "से", "gS": "है", "Kkr": "ज्ञात", "dhft": "कीजिए", "fy;k": "लिया", "x;s": "गए", "D;k": "क्या", "Fks": "थे", "vkneh": "आदमी",
        "ds": "के", "chp": "बीच", "rc": "तब", "U;wure": "न्यूनतम", "Nk=": "छात्र", "rqyuk": "तुलना", "NksVk": "छोटा", "yack": "लंबा",
        "fd": "कि", "foijhr": "विपरीत", "eq[k": "मुख", "est": "मेज", "iM+kslh": "पड़ोसी", "pkSFks": "चौथे", "e/;": "मध्य", "dsoy": "केवल",
        "rhu": "तीन", "rhljs": "तीसरे", "vlR;": "असत्य", "pkfg,": "चाहिए", "nwljs": "दूसरे", "mÙkj": "उत्तर", "lh/kh": "सीधी", "js[kk": "रेखा",
        "Bhd": "ठीक", "lanHkZ": "संदर्भ", "pkjksa": "चारों", "lwpukvksa": "सूचनाओं", "vk/kkj": "आधार", "lgh": "सही", "fodYi": "विकल्प",
        "p;u": "चयन", "v{kj": "अक्षर", "o.kZekyk": "वर्णमाला", "izR;sd": "प्रत्येक", "fuekZ.k": "निर्माण", "lk/kkj.k": "साधारण", "C;kt": "ब्याज",
        "o" : "और"
    }
    
    # Sort keys by length descending to handle multi-char replacements first
    sorted_keys = sorted(kd_map.keys(), key=len, reverse=True)
    
    for k in sorted_keys:
        text = text.replace(k, kd_map[k])
    
    return text
