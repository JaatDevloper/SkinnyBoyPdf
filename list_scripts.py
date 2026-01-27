# -*- coding: utf-8 -*-
from aksharamukha import transliterate

def list_scripts():
    scripts = transliterate.scripts()
    print("Available Scripts in Aksharamukha:")
    for script in sorted(scripts):
        print(f"- {script}")

if __name__ == "__main__":
    list_scripts()
