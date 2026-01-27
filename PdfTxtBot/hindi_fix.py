# -*- coding: utf-8 -*-
import unicodedata
import re

# Comprehensive mapping for Kruti Dev to Unicode
MAPPING = {
    "ñ": "॰", "Q+Z": "फ़", "sas": "sa", "aa": "a", ")Z": "र्द्ध", "ZZ": "Z",
    "‘": "\"", "’": "\"", "“": "'", "”": "'", "å": "०", "ƒ": "१", "„": "२",
    "…": "३", "†": "४", "‡": "५", "ˆ": "६", "‰": "७", "Š": "८", "‹": "९",
    "¶+": "फ़्", "d+": "क़", "[+k": "ख़", "[+": "ख़्", "x+": "ग़", "T+": "ज़्",
    "t+": "ज़", "M+": "ड़", "<+": "ढ़", "Q+": "फ़", ";+": "य़", "j+": "ऱ",
    "u+": "ऩ", "Ùk": "त्त", "Ù": "त्त्", "Dr": "क्त", "–": "दृ", "—": "कृ",
    "é": "न्न", "™": "न्न्", "=kk": "त्रा", "f=k": "त्रि", "à": "ह्न", "á": "ह्य",
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
    "~": "्", "A": "।", "झ": ">", "¼": "(", "½": ")", "्ा": "", "ाे": "ो", "ाै": "ौ"
}

def krutidev_to_unicode(text: str) -> str:
    if not text:
        return ""

    modified_text = text

    # 1. Handle the 'f' (Chhoti ee) shift before other replacements
    # It looks for 'f' and moves it after the next consonant/half-consonant cluster
    modified_text = re.sub(r'f((?:[a-zA-Z0-9\[\]{}|;:,.<>?/!@#$%^&*()_=+~-]|(?:[क-ह]्))*)', r'\1f', modified_text)

    # 2. General Mapping using sorted keys for priority
    sorted_keys = sorted(MAPPING.keys(), key=len, reverse=True)
    for k in sorted_keys:
        modified_text = modified_text.replace(k, MAPPING[k])

    # 3. Handle 'f' which is now 'ि' but needs to be placed after the consonant
    # This regex moves 'ि' after the base consonant and its halant if applicable
    modified_text = re.sub(r'ि([क-ह]्?[क-ह]?)', r'\1ि', modified_text)

    # 4. Handle Reph (Z) - In Kruti Dev 'Z' is typed at the end, but Unicode 'र्' is at the start
    # Matches a consonant cluster + matra followed by Z and moves 'र्' to the front
    modified_text = re.sub(r'([क-ह]्?[क-ह]?[ािीुूेैोौ]?)Z', r'र्\1', modified_text)

    # 5. Clean up conversion artifacts
    replacements = {
        "िा": "ी",
        "ज़्ा": "ज़ा",
        "्ा": "",
        "ाे": "ो",
        "ाै": "ौ"
    }
    for old, new in replacements.items():
        modified_text = modified_text.replace(old, new)

    return unicodedata.normalize("NFC", modified_text).strip()

def fix_file_content(content: str) -> str:
    # Handle the specific case from your input: Dr -> क्त, f=k -> त्रि, etc.
    lines = content.split('\n')
    fixed_lines = [krutidev_to_unicode(line) for line in lines]
    return '\n'.join(fixed_lines)
    
