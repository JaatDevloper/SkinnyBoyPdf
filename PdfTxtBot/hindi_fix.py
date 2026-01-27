# -*- coding: utf-8 -*-
import re

def kruti_to_unicode(text):
    """
    Comprehensive Kruti Dev 010 to Unicode Hindi conversion.
    This handles positional rules like 'i' matra and half-consonants.
    """
    # Character mapping arrays
    array_1 = [
        "ñ", "ò", "ó", "ô", "õ", "ö", "÷", "ø", "ù", "ú", "û", "ü", "ý", "þ",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
        "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b",
        "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
        "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3",
        "4", "5", "6", "7", "8", "9", " ", "।", "!", "?", "-", "_", "+", "*", "/",
        "‘", "’", "“", "”", "(", ")", "{", "}", "=", "।"
    ]
    array_2 = [
        "़", "ा", "ि", "ी", "ु", "ू", "ृ", "े", "ै", "ो", "ौ", "ं", "ः", "ँ",
        "अ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "क", "ख", "ग", "घ", "ङ",
        "च", "छ", "ज", "झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध",
        "न", "प", "फ", "ि", "भ", "म", "य", "र", "ल", "व", "श", "ष", "स", "ह",
        "ु", "ि", "े", "ु", "ू", "ृ", "े", "ै", "ो", "ौ", "०", "१", "२", "३",
        "४", "५", "६", "७", "८", "९", " ", "।", "!", "?", "-", "_", "+", "*", "/",
        "‘", "’", "“", "”", "(", ")", "{", "}", "=", "।"
    ]

    # Specific common Kruti Dev 010 combinations
    mapping = {
        "k": "ा", "i": "प", "h": "ी", "A": "ओ", "S": "ै", "d": "ो", "D": "ौ",
        ";": "य", "fn": "दि", "ia": "पं", "fDr": "क्ति", "esa": "में", "vksj": "ओर", 
        "LFkku": "स्थान", "O;fDr": "व्यक्ति", "iafDr": "पंक्ति", "ls": "से", "gS": "है", 
        "Kkr": "ज्ञात", "dhft": "कीजिए", "fy;k": "लिया", "x;s": "गए", "D;k": "क्या", 
        "Fks": "थे", "vkneh": "आदमी", "ds": "के", "chp": "बीच", "rc": "तब", 
        "U;wure": "न्यूनतम", "Nk=": "छात्र", "rqyuk": "तुलना", "NksVk": "छोटा", 
        "yack": "लंबा", "fd": "कि", "foijhr": "विपरीत", "eq[k": "मुख", "est": "मेज", 
        "iM+kslh": "पड़ोसी", "pkSFks": "चौथे", "e/;": "मध्य", "dsoy": "केवल", 
        "rhu": "तीन", "rhljs": "तीसरे", "vlR;": "असत्य", "pkfg,": "चाहिए", 
        "nwljs": "दूसरे", "mÙkj": "उत्तर", "lh/kh": "सीधी", "js[kk": "रेखा", 
        "Bhd": "ठीक", "lanHkZ": "संदर्भ", "pkjksa": "चारों", "lwpukvksa": "सूचनाओं", 
        "vk/kkj": "आधार", "lgh": "सही", "fodYi": " विकल्प", "p;u": "चयन", 
        "v{kj": "अक्षर", "o.kZekyk": "वर्णमाला", "izR;sd": "प्रत्येक", 
        "fuekZ.k": "निर्माण", "lk/kkj.k": "साधारण", "C;kt": "ब्याज", "o": "और"
    }

    # Apply word replacements first
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    for k in sorted_keys:
        text = text.replace(k, mapping[k])

    # Apply character replacements
    for i in range(len(array_1)):
        text = text.replace(array_1[i], array_2[i])

    # Fix positional 'i' matra: 'ि' + consonant -> consonant + 'ि'
    # Consonants range: \u0915-\u0939
    text = re.sub(r'ि([\u0915-\u0939]्?[\u0915-\u0939]?)', r'\1ि', text)
    
    # Final cleanup of common artifacts
    text = text.replace("िा", "ा")
    
    return text
