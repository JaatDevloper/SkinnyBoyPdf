import re

def krutidev_to_unicode(text):
    if not text:
        return ""

    # 1. CHARACTER MAPPING TABLE (KrutiDev 010 to Unicode)
    mapping = {
        'v': 'अ', 'k': 'ा', 'i': 'ी', 'f': 'ि', 'u': 'ु', 'Q': 'ू', 's': 'ए', 'S': 'ै',
        'd': 'क', 'E': 'ख्', 'D': 'क', 'e': 'म', 'r': 'त', 't': 'ज', 'y': 'ब', 'n': 'न',
        'G': 'ह', 'g': 'ह', 'J': 'र', 'j': 'र', 'O': 'व्', 'I': 'प्', 'P': 'च्', 'p': 'च',
        'c': 'स', 'z': 'भ', 'Z': 'भ', 'x': 'य', 'X': 'य', 'V': 'ट', 'B': 'ब', 'N': 'न',
        'M': 'ा', 'H': 'ी', 'U': 'ु', 'Y': 'ब', 'R': 'त', 'F': 'त', 'K': 'ा', 'w': 'ाँ',
        'q': 'ु', 'W': 'ाँ', 'h': '्', 'j': 'र', 'l': 'स', 'o': 'व', 'L': 'न',
        'm': 'इ', 'n': 'न', 'p': 'च', 'r': 'त', 's': 'ए', 't': 'ज', 'v': 'अ', 'y': 'ब',
        '[': 'ृ', ']': '।', 'Ù': 'ू', 'Ø': '्र', '¡': 'ी', 'ä': 'ि', 'ाे': 'ो', 'ाै': 'ौ',
        '¼': '(', '½': ')', '†': 'ु', 'ˆ': 'ृ', 'A': 'ा', 'ं': 'ं', 'ः': 'ः', '़': '़',
        '्ा': 'ा', 'ीं': 'ीं', 'ks': 'ो', 'kS': 'ौ', 'ीं': 'ीं', 'अा': 'आ'
    }

    # 2. SEPARATING ENGLISH AND HINDI
    # Hum sirf un words ko fix karenge jinme KrutiDev ke hindi characters hain
    words = text.split(' ')
    fixed_words = []

    for word in words:
        # Check if word contains KrutiDev patterns (like 'f' at start or specific Kruti symbols)
        # English words like "respect", "must", "the" etc. won't match common Kruti shifting
        
        # Fixing Matra Shifting (f+d -> df)
        temp_word = re.sub(r'f([a-zA-Z])', r'\1f', word)
        temp_word = re.sub(r'i([a-zA-Z])', r'\1i', temp_word)

        # Transliteration
        new_word = ""
        is_hindi = False
        for char in temp_word:
            if char in mapping:
                new_word += mapping[char]
                # Agar koi bhi mapped character mila, matlab ye hindi word hai
                if char not in ' ().-0123456789': 
                    is_hindi = True
            else:
                new_word += char
        
        # Cleanup
        cleanup = {'ाे': 'ो', 'ाै': 'ौ', 'ेा': 'ो', '्ा': 'ा', 'िा': 'ाि', 'T': 'ा'}
        for old, new in cleanup.items():
            new_word = new_word.replace(old, new)
        
        fixed_words.append(new_word)

    return ' '.join(fixed_words)

def fix_file_content(content):
    lines = content.split('\n')
    fixed_lines = [krutidev_to_unicode(line) for line in lines]
    return '\n'.join(fixed_lines)
    
