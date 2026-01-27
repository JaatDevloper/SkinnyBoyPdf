import re

def krutidev_to_unicode(text):
    if not text:
        return ""

    # 1. SPECIAL REPLACEMENTS (Specific to your text patterns)
    # Kruti Dev में 'f' (ि) अक्षर से पहले आता है, इसे बाद में ले जाना (e.g., fdy -> dyf)
    text = re.sub(r'f([a-zA-Z0-9])', r'\1f', text)
    # आधे अक्षरों को संभालना (e.g., dh -> hd)
    text = re.sub(r'([a-zA-Z])h', r'h\1', text)

    # 2. MAPPING TABLE
    mapping = {
        'k': 'ा', 'i': 'ी', 'f': 'ि', 'u': 'ु', 'Q': 'ू', 's': 'ए', 'S': 'ै', 'a': 'अ', 'v': 'अ',
        'd': 'क', 'E': 'क', 'D': 'क', 'e': 'म', 'r': 'त', 't': 'ज', 'y': 'ब', 'n': 'न', 'L': 'न',
        'G': 'ह', 'g': 'ह', 'J': 'र', 'j': 'र', 'O': 'प', 'I': 'प', 'P': 'च', 'p': 'च', 'c': 'स',
        'z': 'भ', 'Z': 'भ', 'x': 'य', 'X': 'य', 'V': 'ट', 'B': 'ब', 'N': 'न', 'M': 'ा', 'H': 'ी',
        'U': 'ु', 'Y': 'ब', 'R': 'त', 'F': 'त', 'K': 'ा', 'w': 'ाँ', 'W': 'ाँ', 'q': 'ु',
        '1': '१', '2': '२', '3': '३', '4': '४', '5': '५', '6': '६', '7': '७', '8': '८', '9': '९', '0': '०',
        '[': 'ृ', ']': '।', 'Ù': 'ू', 'Ø': '्र', '¡': 'ी', 'ä': 'ि', 'ाे': 'ो', 'ाै': 'ौ',
        '¼': '(', '½': ')', '†': 'ु', 'ˆ': 'ृ', 'ा': 'ा', 'ं': 'ं', 'ः': 'ः', '़': '़', 'ण्': '.'
    }

    # 3. TRANSFORMATION LOOP
    res = ""
    i = 0
    while i < len(text):
        char = text[i]
        # 'h' indicates half letter in Kruti Dev logic
        if char == 'h' and i + 1 < len(text):
            next_char = mapping.get(text[i+1], text[i+1])
            res += next_char + '्'
            i += 2
        else:
            res += mapping.get(char, char)
            i += 1

    # 4. FINAL CLEANUP (Merging common Hindi mistakes)
    res = res.replace('अा', 'आ').replace('ाे', 'ो').replace('ाै', 'ौ')
    res = res.replace('ि्', 'ि').replace('्ि', 'ि')
    # Fixing common formatting like 'प्र' (ीभ)
    res = res.replace('ीभ', 'प्र')
    
    return res

def fix_file_content(content):
    lines = content.split('\n')
    fixed_lines = [krutidev_to_unicode(line) for line in lines]
    return '\n'.join(fixed_lines)
    
