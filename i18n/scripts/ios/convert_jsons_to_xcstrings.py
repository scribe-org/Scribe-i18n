# SPDX-License-Identifier: GPL-3.0-or-later
"""
Converts from Scribe-i18n localization JSON files to the Localizable.xcstrings file.


Usage:
    python3 i18n/scripts/ios/convert_jsons_to_xcstrings.py
"""

import json
import os

directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the path to the "locales" folder.
locales_folder = os.path.join(directory, "locales")

if not os.path.exists(locales_folder):
    print(f"Error: The folder '{locales_folder}' does not exist. Please ensure the path is correct.")
    exit(1)


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
    if not key.startswith("i18n.app"):
        continue

    language = {}
    for lang, lang_json in lang_data.items():  # use already loaded language data
        translation = lang_json.get(key, "")
        if lang == "en-US":
            lang = "en"

        if translation:
            language[lang] = {"stringUnit": {"state": "", "value": translation}}

    strings[key] = {"comment": "", "localizations": language}

data |= {"strings": strings, "version": "1.0"}

with open(os.path.join(directory, "Localizable.xcstrings"), "w") as xcstrings_file:
    json.dump(data, xcstrings_file, indent=2, ensure_ascii=False, separators=(",", " : "))
    xcstrings_file.write("\n")

print(
    "Scribe-i18n localization JSON files successfully converted to the Localizable.xcstrings file."
)
