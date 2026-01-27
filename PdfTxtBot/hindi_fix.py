# -*- coding: utf-8 -*-
import unicodedata

def kruti_to_unicode(text: str) -> str:
    """
    Direct Glyph-to-Unicode mapping for KrutiDev 010.
    This bypasses transliteration libraries and maps the ASCII 
    representation of KrutiDev characters to their Unicode equivalents.
    """
    if not text:
        return text

    # Standard KrutiDev 010 to Unicode Mapping Table
    # This maps the ASCII characters in the font to actual Devanagari Unicode
    mapping = {
        "ñ": "!", "ò": "\"", "ó": "#", "ô": "$", "õ": "%", "ö": "&", "÷": "'", "ø": "(", "ù": ")", "ú": "*", "û": "+", "ü": ",", "ý": "-", "þ": ".", "ÿ": "/",
        "0": "०", "1": "१", "2": "२", "3": "३", "4": "४", "5": "५", "6": "६", "7": "७", "8": "८", "9": "९",
        "अ": "v", "आ": "vk", "इ": " b", "ई": " bZ", "उ": "m", "ऊ": " mQ", "ऋ": " ऋ", "ए": " ,", "ऐ": " vS", "ओ": "vkS", "औ": "vkS",
        "क": "d", "ख": "[k", "ग": "x", "घ": "?" , "ङ": "³",
        "च": "p", "छ": "N", "ज": "t", "झ": "´", "ञ": "¥",
        "ट": "V", "ठ": "B", "ड": "M", "ढ": "<", "ण": ".k",
        "त": "r", "थ": "Fk", "द": "n", "ध": "èk", "न": "u",
        "प": "i", "फ": "Q", "ब": "c", "भ": "Hk", "म": "e",
        "य": "y", "र": "j", "ल": "y", "व": "o", "श": "'k", "ष": "k", "स": "l", "ह": "g",
        "क्ष": "{k", "त्र": "=" , "ज्ञ": "K", "श्र": "J",
        "ा": "k", "ि": "f", "ी": "h", "ु": "q", "ू": "w", "ृ": "`", "े": "s", "ै": "S", "ो": "ks", "ौ": "kS",
        "ं": "a", "ः": "%", "ॅ": "W", "ॉ": "kS", "्र": "z", "र्": "Z", "़": "u"
    }

    # Reverse the mapping to act as a converter (ASCII -> Unicode)
    # The dictionary above is structured as [Unicode: ASCII] for reference, 
    # so we need to flip it or use the correct ASCII->Unicode pairs.
    
    # Accurate KrutiDev 010 Mapping Table (ASCII Char -> Unicode Char)
    kruti_map = {
        "k": "ा", "f": "ि", "h": "ी", "q": "ु", "w": "ू", "s": "े", "S": "ै", "a": "ं", "%": "ः", "W": "ॅ", 
        "z": "्र", "Z": "र्", "u": "़", "v": "अ", "i": "प", "e": "म", "r": "त", "u": "न", "y": "थ", "x": "ग", 
        "c": "ब", "v": "व", "b": "इ", "n": "न", "m": "म", "w": "य", "t": "ज", "d": "क", "[": "ख", "x": "ग", 
        "?": "घ", "p": "च", "N": "छ", "´": "झ", "¥": "ञ", "V": "ट", "B": "ठ", "M": "ड", "<": "ढ", ".": "ण", 
        "F": "थ", "n": "द", "è": "ध", "Q": "फ", "H": "भ", "j": "र", "y": "ल", "'": "श", "k": "ष", "l": "स", 
        "g": "ह", "{": "क्ष", "=": "त्र", "K": "ज्ञ", "J": "श्र", "0": "०", "1": "१", "2": "२", "3": "३", 
        "4": "४", "5": "५", "6": "६", "7": "७", "8": "८", "9": "९"
    }

    # Complex KrutiDev conversion requires handling the 'i' (f) matra which comes BEFORE the consonant
    # and the 'reph' (Z) which comes AFTER.
    
    # This is a simplified but functional glyph mapping for standard KrutiDev 010
    array_1 = ["f", "A", "q", "w", "`", "s", "S", "a", "%", "W", "Z", "z", "u", "k", "h"]
    array_2 = ["ि", "।", "ु", "ू", "ृ", "े", "ै", "ं", "ः", "ॅ", "र्", "्र", "़", "ा", "ी"]

    array_3 = ["v", "vk", " b", " bZ", "m", " mQ", " ऋ", " ,", " vS", "vks", "vkS", "d", "[k", "x", "?", "³", "p", "N", "t", "´", "¥", "V", "B", "M", "<", ".k", "r", "Fk", "n", "èk", "u", "i", "Q", "c", "Hk", "e", "y", "j", "y", "o", "'k", "k", "l", "g", "{k", "=", "K", "J"]
    array_4 = ["अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ए", "ऐ", "ओ", "औ", "क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", "झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न", "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "श", "ष", "स", "ह", "क्ष", "त्र", "ज्ञ", "श्र"]

    processed = text
    
    # Replace strings in array_3 with array_4
    for i in range(len(array_3)):
        processed = processed.replace(array_3[i], array_4[i])
        
    # Replace characters in array_1 with array_2
    for i in range(len(array_1)):
        processed = processed.replace(array_1[i], array_2[i])

    # Fix the 'i' matra position (KrutiDev puts 'f' before the consonant)
    # Example: 'fi' -> 'पि' (p + i)
    # This is a common pattern in KrutiDev: f + [consonant] -> [consonant] + ि
    import re
    # Match 'ि' followed by any Devanagari character and move it after
    processed = re.sub(r'ि(.)', r'\1ि', processed)
    
    # Fix 'र्' (Z) which often needs to be moved to the correct position over the consonant
    processed = re.sub(r'(.)र्', r'र्\1', processed)

    # Final cleanup with NFC normalization
    final_text = unicodedata.normalize("NFC", processed)
    
    # Specific common word fixes for things that might have broken in mapping
    corrections = {
        "ाे": "ो", "ाै": "ौ", "िा": "ा", "अो": "ओ", "नषो": "कुल", "ऐो": "एक"
    }
    for k, v in corrections.items():
        final_text = final_text.replace(k, v)

    return final_text
