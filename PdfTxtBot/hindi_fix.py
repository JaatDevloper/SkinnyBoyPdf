# -*- coding: utf-8 -*-
import unicodedata
from aksharamukha import transliterate

def kruti_to_unicode(text):
    """
    Convert legacy Hindi (Kruti Dev 010) to proper Unicode Devanagari
    using aksharamukha and Unicode normalization (NFC).
    """
    try:
        # Aksharamukha Mapping from legacy KrutiDev to Unicode Devanagari
        # Note: 'Krutidev' is the standard name in Aksharamukha
        converted = transliterate.process('Krutidev', 'Devanagari', text)
        
        # Unicode Normalization Form Canonical Composition (NFC)
        # This is critical for Telegram to render matras and ligatures correctly
        normalized = unicodedata.normalize('NFC', converted)
        
        # Final cleanup for common artifacts that transliteration might miss
        replacements = {
            "ाे": "ो", "ाै": "ौ", "िा": "ा", "अो": "ओ", "नषो": "कुल", "ऐो": "एक",
            "१ण": "१.", "२ण": "२.", "३ण": "३.", "४ण": "४.", "५ण": "५.", 
            "६ण": "६.", "७ण": "७.", "८ण": "८.", "९ण": "९.", "१०ण": "१०."
        }
        for k, v in replacements.items():
            normalized = normalized.replace(k, v)
            
        return normalized
    except Exception as e:
        print(f"Error in Hindi conversion: {e}")
        return text
