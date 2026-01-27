# -*- coding: utf-8 -*-
import sys

# Original Kruti Dev 010 text from the user's sample
test_input = "10. lkr O;fä M] N] O] P] Q] R vkSj S mÙkj dh vksj eqag djds ,d lh/kh js[kk esa cSBs gSa ¼t:jh ugha fd blh Øe esa gksa½A R vkSj S ds chp esa dsoy nks O;fä cSBs gSaA S] N ds ck,a ls nwljs LFkku ij cSBk gSA P] O ds ck,a ls rhljs LFkku ij cSBk gSA S vkSj N ds chp esa dsoy Q cSBk gSA N iafä ds lcls nkfgus Nksj ij cSBk gSA rks fuEufyf[kr esa ls dkSu iafä ds Bhd chp esa cSBk gS\\"

def test_manual_mapping(text):
    print("Testing Manual Mapping...")
    # This is a simplified version of our current mapping
    # Just to see if it can handle the core characters
    kd_map = {
        "lkr": "सात", "O;fä": "व्यक्ति", "vkSj": "और", "mÙkj": "उत्तर", "eqag": "मुंह",
        "lh/kh": "सीधी", "js[kk": "रेखा", "cSBs": "बैठे", "gSa": "हैं", "fuf'pr": "निश्चित",
        "ck,a": "बाएं", "ls": "से", "nwljs": "दूसरे", "LFkku": "स्थान", "cSBk": "बैठा",
        "rhljs": "तीसरे", "chp": "बीच", "dsoy": "केवल", "iafä": "पंक्ति", "nkfgus": "दाहिने",
        "Nksj": "छोर", "fuEufyf[kr": "निम्नलिखित", "Bhd": "ठीक", "gS": "है"
    }
    temp = text
    for k, v in kd_map.items():
        temp = temp.replace(k, v)
    return temp

def test_aksharamukha(text):
    print("Testing Aksharamukha...")
    try:
        from aksharamukha import transliterate
        # Try different possible script names
        for script in ['KrutiDev010', 'KrutiDev', 'Krutidev']:
            try:
                result = transliterate.process(script, 'Devanagari', text)
                if result != text:
                    print(f"  Success with {script}!")
                    return result
            except:
                continue
        return "Failed to transliterate"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(f"Input: {test_input}\n")
    print(f"Manual Result: {test_manual_mapping(test_input)}\n")
    print(f"Aksharamukha Result: {test_aksharamukha(test_input)}\n")
