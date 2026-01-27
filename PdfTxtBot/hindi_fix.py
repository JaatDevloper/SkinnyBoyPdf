# -*- coding: utf-8 -*-
import unicodedata
from aksharamukha import transliterate

def kruti_to_unicode(text: str) -> str:
    """
    Convert legacy Hindi (KrutiDev / Chanakya / broken legacy)
    into proper Unicode Devanagari for Telegram.
    """
    if not text:
        return text

    try:
        # Step 1: Convert legacy Hindi → Unicode Devanagari
        # Aksharamukha does NOT support 'Krutidev' as input.
        # Use source='Hindi' and target='Devanagari'.
        converted = transliterate.process(
            "Hindi",        # IMPORTANT: not "Krutidev"
            "Devanagari",
            text
        )

        # Step 2: Unicode normalization (mandatory)
        converted = unicodedata.normalize("NFC", converted)

        # Step 3: Minimal safe cleanup (ONLY universal fixes)
        converted = (
            converted
            .replace("ाे", "ो")
            .replace("ाै", "ौ")
        )

        return converted.strip()

    except Exception as e:
        print("Hindi conversion error:", e)
        return text
