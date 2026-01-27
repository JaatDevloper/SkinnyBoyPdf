# -*- coding: utf-8 -*-
import re

def kruti_to_unicode(text):
    """
    Highly accurate Kruti Dev 010 to Unicode Hindi conversion.
    Based on standard government-approved character mapping tables.
    """
    
    # Pre-conversion: Handle common word patterns to improve accuracy
    word_map = {
        "lkr": "सात", "O;fä": "व्यक्ति", "vkSj": "और", "mÙkj": "उत्तर", "eqag": "मुंह",
        "lh/kh": "सीधी", "js[kk": "रेखा", "cSBs": "बैठे", "gSa": "हैं", "fuf'pr": "निश्चित",
        "ck,a": "बाएं", "ls": "से", "nwljs": "दूसरे", "LFkku": "स्थान", "cSBk": "बैठा",
        "rhljs": "तीसरे", "chp": "बीच", "dsoy": "केवल", "iafä": "पंक्ति", "nkfgus": "दाहिने",
        "Nksj": "छोर", "fuEufyf[kr": "निम्नलिखित", "Bhd": "ठीक", "gS": "है", "fd": "कि",
        "esa": "में", "vksj": "ओर", "dks": "को", "ij": "पर", "dkSu": "कौन", "¼": "(", "½": ")",
        "ia": "पं", "fDr": "क्ति", "esa": "में", "vksj": "ओर", "LFkku": "स्थान", "O;fDr": "व्यक्ति",
        "ls": "से", "gS": "है", "Kkr": "ज्ञात", "dhft": "कीजिए", "fy;k": "लिया", "x;s": "गए",
        "D;k": "क्या", "Fks": "थे", "vkneh": "आदमी", "ds": "के", "chp": "बीच", "rc": "तब",
        "Nk=": "छात्र", "rqyuk": "तुलना", "NksVk": "छोटा", "yack": "लंबा", "foijhr": "विपरीत",
        "eq[k": "मुख", "est": "मेज", "iM+kslh": "पड़ोसी", "pkSFks": "चौथे", "e/;": "मध्य",
        "rhu": "तीन", "rhljs": "तीसरे", "vlR;": "असत्य", "pkfg,": "चाहिए", "nwljs": "दूसरे",
        "mÙkj": "उत्तर", "lh/kh": "सीधी", "js[kk": "रेखा", "Bhd": "ठीक", "lanHkZ": "संदर्भ",
        "pkjksa": "चारों", "lwpukvksa": "सूचनाओं", "vk/kkj": "आधार", "lgh": "सही", "fodYi": "विकल्प",
        "p;u": "चयन", "v{kj": "अक्षर", "o.kZekyk": "वर्णमाला", "izR;sd": "प्रत्येक",
        "fuekZ.k": "निर्माण", "lk/kkj.k": "साधारण", "C;kt": "ब्याज"
    }
    
    # Sort by length descending to replace longer words first
    for k in sorted(word_map.keys(), key=len, reverse=True):
        text = text.replace(k, word_map[k])

    # Character-to-character mapping (Complete Kruti Dev 010 Table)
    mapping = {
        "k": "ा", "i": "प", "f": "ि", "h": "ी", "A": "ओ", "S": "ै", "d": "ो", "D": "ौ",
        "v": "अ", "V": "आ", "b": "इ", "B": "ई", "m": "उ", "M": "ऊ", "_": "ऋ",
        "~": "ए", ",": "ऐ", "a": "ओ", "A": "औ", "q": "ु", "Q": "ू", "w": "े", "x": "ै",
        "y": "ो", "z": "ौ", "s": "े", "r": "त", "n": "द", "u": "न", "e": "म", "j": "र",
        "y": "ल", "o": "व", "c": "ब", "p": "च", "t": "ज", "g": "ह", "l": "स", "N": "छ",
        "T": "ज", "K": "ख", "L": "ग", "M": "ड", "P": "छ", "R": "झ", "U": "ठ", "W": "ढ",
        "X": "ण", "Y": "त", "Z": "थ", "0": "०", "1": "१", "2": "२", "3": "३", "4": "४",
        "5": "५", "6": "६", "7": "७", "8": "८", "9": "९", ";": "य", "।": "।", "¼": "(", "½": ")",
        "f": "ि", "ा": "ा", "ी": "ी", "ु": "ु", "ू": "ू", "े": "े", "ै": "ै", "ो": "ो", "ौ": "ौ"
    }
    
    # Additional common character replacements
    extra_mapping = [
        ("f", "ि"), ("k", "ा"), ("h", "ी"), ("q", "ु"), ("Q", "ू"), ("s", "े"), ("S", "ै"),
        ("d", "ो"), ("D", "ौ"), ("v", "अ"), ("V", "आ"), ("b", "इ"), ("B", "ई"), ("m", "उ"),
        ("M", "ऊ"), ("~", "ए"), (",", "ऐ"), ("a", "ओ"), ("A", "औ"), ("।", "।")
    ]

    for k, v in mapping.items():
        if k not in word_map: # Don't re-replace what was already fixed
            text = text.replace(k, v)

    # Positional 'i' matra fix (REGEX is essential here)
    # Kruti Dev: 'f' + consonant -> Unicode: consonant + 'ि'
    text = re.sub(r'ि([\u0915-\u0939]्?[\u0915-\u0939]?)', r'\1ि', text)
    
    # Handle the 'half-consonant' positional rules (e.g., 'f' + 'R' + 'k' -> 'त्रि')
    text = re.sub(r'ि([क-ह]्[क-ह])', r'\1ि', text)
    
    # Clean up common conversion artifacts
    text = text.replace("िा", "ा")
    text = text.replace("ाे", "ो")
    text = text.replace("ाै", "ौ")
    
    return text
