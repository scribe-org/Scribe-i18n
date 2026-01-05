# SPDX-License-Identifier: GPL-3.0-or-later
"""
Converts from Scribe-i18n localization JSON files to the Localizable.xcstrings file.


Usage:
    python3 i18n/scripts/ios/convert_jsons_to_xcstrings.py
"""

import json
import os
import re
import glob

directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the path to the "locales" folder.
locales_folder = os.path.join(directory, "locales")

if not os.path.exists(locales_folder):
    print(f"Error: The folder '{locales_folder}' does not exist. Please ensure the path is correct.")
    exit(1)

# Define the path to Scribe-iOS root (go up from i18n/i18n/scripts/ios to reach Scribe-iOS)
scribe_ios_root = os.path.abspath(os.path.join(directory, "..", "..", ".."))

def find_used_keys(root_path):
    """Scan Swift files for localization key usage."""
    used_keys = set()
    
    swift_files = glob.glob(os.path.join(root_path, "**/*.swift"), recursive=True)
    
    for filepath in swift_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Find all strings that look like i18n keys
                matches = re.findall(r'["\'](i18n\.[^"\']+)["\']', content)
                used_keys.update(matches)
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
    
    return used_keys


# Find all keys actually used in the codebase
used_keys = find_used_keys(scribe_ios_root)

json_dir_list = os.listdir(locales_folder)
languages = sorted(
    [file.replace(".json", "") for file in json_dir_list if file.endswith(".json")]
)

# Load the base language file safely.
try:
    with open(os.path.join(locales_folder, "en-US.json"), "r") as json_file:
        base_language_data = json.load(json_file)

except FileNotFoundError:
    print("Error: The base language file 'en-US.json' does not exist.")
    exit(1)


data = {"sourceLanguage": "en"}
strings = {}

# Pre-load all JSON files into a dictionary.
lang_data = {}
for lang in languages:
    with open(os.path.join(locales_folder, f"{lang}.json"), "r") as lang_file:
        lang_data[lang] = json.load(lang_file)

for key in base_language_data:
    if not key.startswith(("i18n.app", "i18n._global")):
        continue

    language = {}
    for lang, lang_json in lang_data.items():  # use already loaded language data
        translation = lang_json.get(key, "")
        if lang == "en-US":
            lang = "en"

        if translation:
            language[lang] = {"stringUnit": {"state": "", "value": translation}}
    
    # Mark as active if found in the codebase
    if key in used_keys:
        strings[key] = {"comment": "", "localizations": language}
    else:
        strings[key] = {"comment": "", "extractionState": "stale", "localizations": language}


# Sort using a custom key to match iOS/Xcode localized sorting
sorted_strings = {
    k: strings[k] for k in sorted(strings.keys(), key=lambda x: x.replace(".", "|"))
}

data |= {"strings": sorted_strings, "version": "1.0"}

with open(os.path.join(directory, "Localizable.xcstrings"), "w") as xcstrings_file:
    json.dump(data, xcstrings_file, indent=2, ensure_ascii=False, separators=(",", " : "))
    xcstrings_file.write("\n")

print(
    "Scribe-i18n localization JSON files successfully converted to the Localizable.xcstrings file."
)
