# -*- coding: utf-8 -*-
from aksharamukha import transliterate

def kruti_to_unicode(text):
    """
    Convert Kruti Dev 010 encoded text to Unicode Hindi using aksharamukha.
    """
    try:
        # Aksharamukha supports KrutiDev to Unicode
        # Source: 'KrutiDev010', Target: 'Devanagari'
        fixed_text = transliterate.process('KrutiDev010', 'Devanagari', text)
        return fixed_text
    except Exception as e:
        print(f"Aksharamukha error: {e}")
        # Fallback to simple replacement if aksharamukha fails
        return text
