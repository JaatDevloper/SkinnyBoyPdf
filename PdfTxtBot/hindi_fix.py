# -*- coding: utf-8 -*-
import unicodedata
import re

# Optimized mapping including punctuation fixes
MAPPING = {
    "ñ": "॰", "Q+Z": "QZ+", "sas": "sa", "aa": "a", ")Z": "र्द्ध", "ZZ": "Z",
    "‘": "\"", "’": "\"", "“": "'", "”": "'", "å": "०", "ƒ": "१", "„": "२",
    "…": "३", "†": "४", "‡": "५", "ˆ": "६", "‰": "७", "Š": "८", "‹": "९",
    "¶+": "फ़्", "d+": "क़", "[+k": "ख़", "[+": "ख़्", "x+": "ग़", "T+": "ज़्",
    "t+": "ज़", "M+": "ड़", "<+": "ढ़", "Q+": "फ़", ";+": "य़", "j+": "ऱ",
    "u+": "ऩ", "Ùk": "त्त", "Ù": "त्त्", "Dr": "क्त", "–": "दृ", "—": "कृ",
    "é": "न्न", "™": "न्न्", "=kk": "=k", "f=k": "f=", "à": "ह्न", "á": "ह्य",
    "â": "हृ", "ã": "ह्म", "ºz": "ह्र", "º": "ह्", "í": "द्द", "{k": "क्ष",
    "{": "क्ष्", "=": "त्र", "«": "त्र्", "Nî": "छ्य", "Vî": "ट्य", "Bî": "ठ्य",
    "Mî": "ड्य", "<î": "ढ्य", "|": "द्य", "K": "ज्ञ", "}": "द्व", "J": "श्र",
    "Vª": "ट्र", "Mª": "ड्र", "<ªª": "ढ्र", "Nª": "छ्र", "Ø": "क्र", "Ý": "फ्र",
    "nzZ": "र्द्र", "æ": "द्र", "ç": "प्र", "Á": "प्र", "xz": "ग्र", "#": "रु",
    ":": "रू", "v‚": "ऑ", "vks": "ओ", "vkS": "औ", "vk": "आ", "v": "अ",
    "b±": "ईं", "Ã": "ई", "bZ": "ई", "b": "इ", "m": "उ", "Å": "ऊ", ",s": "ऐ",
    ",": "ए", "_": "ऋ", "ô": "क्क", "d": "क", "Dk": "क", "D": "क्", "[k": "ख",
    "[": "ख्", "x": "ग", "Xk": "ग", "X": "ग्", "Ä": "घ", "?k": "घ", "?": "घ्",
    "³": "ङ", "pkS": "चै", "p": "च", "Pk": "च", "P": "च्", "N": "छ", "t": "ज",
    "Tk": "ज", "T": "ज्", ">": "झ", "÷": "झ्", "¥": "ञ", "ê": "ट्ट", "ë": "ट्ठ",
    "V": "ट", "B": "ठ", "ì": "ड्ड", "ï": "ड्ढ", "M": "ड", "<": "ढ", ".k": "ण",
    ".": "ण्", "r": "त", "Rk": "त", "R": "त्", "Fk": "थ", "F": "थ्", ")": "द्ध",
    "n": "द", "/k": "ध", "èk": "ध", "/": "ध्", "Ë": "ध्", "è": "ध्", "u": "न",
    "Uk": "न", "U": "न्", "i": "प", "Ik": "प", "I": "प्", "Q": "फ", "¶": "फ्",
    "c": "ब", "Ck": "ब", "C": "ब्", "Hk": "भ", "H": "भ्", "e": "म", "Ek": "म",
    "E": "म्", ";": "य", "¸": "य्", "j": "र", "y": "ल", "Yk": "ल", "Y": "ल्",
    "G": "ळ", "o": "व", "Ok": "व", "O": "व्", "'k": "श", "'": "श्", "\"k": "ष",
    "\"": "ष्", "l": "स", "Lk": "स", "L": "स्", "g": "ह", "È": "ीं", "z": "्र",
    "‚": "ॉ", "ks": "ो", "kS": "ौ", "k": "ा", "h": "ी", "q": "ु", "w": "ू",
    "`": "ृ", "s": "े", "S": "ै", "a": "ं", "¡": "ँ", "%": "ः", "W": "ॅ",
    "~": "्", "-": "-", "A": "।", "1": "1", "2": "2", "3": "3", "4": "4", 
    "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "0": "0", 
    "(": "(", ")": ")", "\\": " "
}

def krutidev_to_unicode(text: str) -> str:
    if not text:
        return ""

    # Sort keys by length to prevent partial matches
    sorted_keys = sorted(MAPPING.keys(), key=len, reverse=True)
    
    # 1. Standard character replacement
    for k in sorted_keys:
        text = text.replace(k, MAPPING[k])

    # 2. Fix the "Chhoti ee" (f) vowel position
    # In Kruti Dev, 'f' comes before the letter. In Unicode, 'ि' comes after.
    # We look for 'ि' followed by any character (including half-letters with virama)
    # and swap them.
    text = re.sub(r'ि([क-ह](्[क-ह])?)', r'\1ि', text)

    # 3. Fix Reph (Z / र्) position
    # In Kruti Dev, 'Z' is often at the end, but in Unicode it should be at the start of the cluster
    text = re.sub(r'([क-ह](्[क-ह])?)([ािीुूेैोौ]?)्र', r'र्\1\3', text)

    return unicodedata.normalize("NFC", text)

def save_unicode_txt(path: str, text: str):
    with open(path, "w", encoding="utf-8-sig", newline="\n") as f:
        f.write(text)

# --- Test Example ---
input_text = """1. ;fn ,d iafDr esa ,d O;fDr nk;ha vksj ls 6osa vkSj ck;ha vksj ls 8osa LFkku ij cSBk gS] rks ml iafDr esa cSBs O;fDr;ksa dh dqy la[;k Kkr dhft,\\
(a) 13 ✅
(b) 12"""

print(krutidev_to_unicode(input_text))
