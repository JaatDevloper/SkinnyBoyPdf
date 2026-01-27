
import os
import re

def kruti_to_unicode(text):
    """
    Convert Kruti Dev 010 encoded text to Unicode Hindi.
    This implementation handles character mapping and positional rules (like 'i' matra).
    """
    
    # Kruti Dev to Unicode mapping
    # Using a list of tuples to maintain order if needed, but dict is fine for replacements
    mapping = {
        "ñ": "़", "ò": "ा", "ó": "ि", "ô": "ी", "õ": "ु", "ö": "ू", "÷": "ृ", "ø": "े", "ù": "ै", "ú": "ो", "û": "ौ", "ü": "ं", "ý": "ः", "þ": "ँ",
        "A": "अ", "B": "इ", "C": "ई", "D": "उ", "E": "ऊ", "F": "ए", "G": "ऐ", "H": "ओ", "I": "औ",
        "J": "क", "K": "ख", "L": "ग", "M": "घ", "N": "ङ", "O": "च", "P": "छ", "Q": "ज", "R": "झ", "S": "ञ",
        "T": "ट", "U": "ठ", "V": "ड", "W": "ढ", "X": "ण", "Y": "त", "Z": "थ", "a": "द", "b": "ध",
        "c": "न", "d": "प", "e": "फ", "f": "ि", "g": "भ", "h": "म", "i": "य", "j": "र", "k": "ल", "l": "व",
        "m": "श", "n": "ष", "o": "स", "p": "ह",
        "q": "ु", "r": "ि", "s": "े", "t": "ु", "u": "ू", "v": "ृ", "w": "े", "x": "ै", "y": "ो", "z": "ौ",
        "0": "०", "1": "१", "2": "२", "3": "३", "4": "४", "5": "५", "6": "६", "7": "७", "8": "८", "9": "९",
        "k": "ा", "i": "प", "f": "ि", "h": "ी", "A": "ओ", "S": "ै", "d": "ो", "D": "ौ",
        ";": "य", "fn": "दि", "ia": "पं", "fDr": "क्ति", "esa": "में", "vksj": "ओर", "LFkku": "स्थान", "O;fDr": "व्यक्ति", "iafDr": "पंक्ति",
        "ls": "से", "gS": "है", "Kkr": "ज्ञात", "dhft": "कीजिए", "fy;k": "लिया", "x;s": "गए", "D;k": "क्या", "Fks": "थे", "vkneh": "आदमी",
        "ds": "के", "chp": "बीच", "rc": "तब", "U;wure": "न्यूनतम", "Nk=": "छात्र", "rqyuk": "तुलना", "NksVk": "छोटा", "yack": "लंबा",
        "fd": "कि", "foijhr": "विपरीत", "eq[k": "मुख", "est": "मेज", "iM+kslh": "पड़ोसी", "pkSFks": "चौथे", "e/;": "मध्य", "dsoy": "केवल",
        "rhu": "तीन", "rhljs": "तीसरे", "vlR;": "असत्य", "pkfg,": "चाहिए", "nwljs": "दूसरे", "mÙkj": "उत्तर", "lh/kh": "सीधी", "js[kk": "रेखा",
        "Bhd": "ठीक", "lanHkZ": "संदर्भ", "pkjksa": "चारों", "lwpukvksa": "सूचनाओं", "vk/kkj": "आधार", "lgh": "सही", "fodYi": "विकल्प",
        "p;u": "चयन", "v{kj": "अक्षर", "o.kZekyk": "वर्णमाला", "izR;sd": "प्रत्येक", "fuekZ.k": "निर्माण", "lk/kkj.k": "साधारण", "C;kt": "ब्याज",
        "o" : "और"
    }

    # Standard Kruti Dev 010 to Unicode replacements (Extended)
    array_1 = [
        "‘", "’", "“", "”", "(", ")", "{", "}", "=", "।", "!", "?", "-", "_", "+", "*", "/", " ",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "v", "V", "b", "B", "m", "M", "_", "~", ",", "a", "A",
        "k", "i", "h", "q", "Q", "v", "s", "S", "d", "D", "!", "K", "]",
        "f", "x", "X", "g", "G", "?", "p", "P", "N", "t", "T", ">", "V", "B", "M", "<", ".", "r", "R", "Fk", "F", "n", "N", "/", "u", "U", "i", "I", "c", "C", "H", "e", "E", ";", "j", "y", "Y", "o", "O", "ó", "Ó", "ष", "l", "L", "g", "G"
    ]
    array_2 = [
        "‘", "’", "“", "”", "(", ")", "{", "}", "=", "।", "!", "?", "-", "_", "+", "*", "/", " ",
        "०", "१", "२", "३", "४", "५", "६", "७", "८", "९",
        "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ",
        "ा", "ि", "ी", "ु", "ू", "ृ", "े", "ै", "ो", "ौ", "ं", "्", "़",
        "ि", "ख", "ख्", "ग", "ग्", "घ", "च", "च्", "छ", "ज", "ज्", "झ", "ट", "ठ", "ड", "ढ", "ण", "त", "त्", "थ", "थ्", "द", "द्ध", "ध", "न", "न्", "प", "प्", "ब", "ब्", "भ", "म", "म्", "य", "र", "ल", "ल्", "व", "व्", "श", "श्", "ष", "स", "स्", "ह", "ह"
    ]

    # Special positional rules (like short 'i' matra which appears before the consonant)
    # This is a complex logic that usually involves regex.
    
    # First, handle the known dictionary for common words to improve accuracy
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    for k in sorted_keys:
        text = text.replace(k, mapping[k])

    # Then apply character by character for anything remaining
    for i in range(len(array_1)):
        text = text.replace(array_1[i], array_2[i])

    # Positional 'i' matra fix: 'ि' + consonant -> consonant + 'ि'
    # In Kruti Dev, 'f' (converted to 'ि') is typed BEFORE the consonant. 
    # Unicode needs it AFTER.
    # We find 'ि' followed by any Hindi consonant and swap them.
    # Devanagari consonants: क-ह (U+0915 to U+0939) plus others
    text = re.sub(r'ि([क-ह])', r'\1ि', text)
    # Handle half consonants as well
    text = re.sub(r'ि([क-ह]्)', r'\1ि', text)
    
    return text
