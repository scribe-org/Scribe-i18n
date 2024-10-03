"""
Converts from the Scribe-i18n Localizable.xcstrings file to localization JSON files.

Usage:
    python3 Scribe-i18n/scripts/ios/convert_xcstrings_to_jsons.py
"""


import json
import os

# Determine the directory
directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Read the Localizable.xcstrings file
try:
    with open(os.path.join(directory, "Localizable.xcstrings"), "r") as f:
        file = f.read()
except FileNotFoundError:
    print("Error: Localizable.xcstrings file not found.")
    exit(1)

dir_list = os.listdir(directory)
languages = [file.replace(".json", "") for file in dir_list if file.endswith(".json")]

for lang in languages:
    dest = open(f"{directory}/{lang}.json", "w")
    if lang == "en-US":
        lang = "en"

    json_file = json.loads(file)
    strings = json_file["strings"]

    data = {}
    for pos, key in enumerate(strings, start=1):
        translation = ""
        if (
            lang in json_file["strings"][key]["localizations"]
            and json_file["strings"][key]["localizations"][lang]["stringUnit"]["value"]
            != ""
            and json_file["strings"][key]["localizations"][lang]["stringUnit"]["value"]
            != key
        ):
            translation = json_file["strings"][key]["localizations"][lang][
                "stringUnit"
            ]["value"]

        data[key] = translation

    json.dump(data, dest, indent=2, ensure_ascii=False)
    dest.write("\n")

print(
    "Scribe-i18n Localizable.xcstrings file successfully converted to the localization JSON files."
)
