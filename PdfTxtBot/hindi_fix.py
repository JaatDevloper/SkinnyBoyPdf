# -*- coding: utf-8 -*-
import unicodedata
from aksharamukha import transliterate

def kruti_to_unicode(text: str) -> str:
    """
    Convert legacy Hindi (KrutiDev) into proper Unicode Devanagari.
    Using 'Krutidev' which is the correct internal script name for Aksharamukha.
    """
    if not text:
        return text

    try:
        # Step 1: Convert legacy Hindi (KrutiDev) → Unicode Devanagari
        # Aksharamukha uses 'Krutidev' (case sensitive) for the legacy font
        converted = transliterate.process(
            "Krutidev",
            "Devanagari",
            text
        )

        # Step 2: Unicode normalization (mandatory for matra rendering)
        converted = unicodedata.normalize("NFC", converted)

        # Step 3: Specific fixes for common KrutiDev conversion artifacts
        # Matra fixes and character corrections
        replacements = {
            "ाे": "ो", 
            "ाै": "ौ",
            "िा": "ा",
            "अो": "ओ",
            "नषो": "कुल",
            "ऐो": "एक"
        }
        for k, v in replacements.items():
            converted = converted.replace(k, v)

        return converted.strip()

    except Exception as e:
        print("Hindi conversion error:", e)
        return text
