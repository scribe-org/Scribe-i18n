# SPDX-License-Identifier: GPL-3.0-or-later
"""
Converts from string.xml files to Scribe-i18n localization JSON files.

Usage:
    python3 i18n/scripts/android/convert_strings_to_json.py
"""

import os
import json
import re


def unescape_special_characters(string):
    """
    Replaces escaped special characters with those needed for JSON file formatting.
    """
    string = string.replace("&gt;", ">")
    string = string.replace("&lt;", "<")
    string = string.replace("&amp;", "&")
    string = string.replace("\\'", "'")
    string = string.replace("\\n", "\n")

    return string


directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the path to the "locales" folder.
locales_folder = os.path.join(directory, "locales")
if not os.path.exists(locales_folder):
    os.makedirs(locales_folder)

dir_list = os.listdir(locales_folder)
languages = sorted(
    [file.replace(".json", "") for file in dir_list if file.endswith(".json")]
)
regex = re.compile(r'<string name="(.*?)">(.*?)</string>', re.DOTALL)

values_directory = os.path.join(directory, "values")
if not os.path.exists(values_directory):
    print(f"Error: The folder '{values_directory}' does not exist. Please ensure the path is correct.")
    exit(1)

for lang in languages:
    path = os.path.join(values_directory, lang)
    try:
        with open(f"{path}/string.xml", "r") as file:
            content = file.read()

    except FileNotFoundError:
        print(f"Error: {path}/string.xml file not found.")
        exit(1)

    except Exception as e:
        print(f"Error: An unexpected error occurred while writing to ' {path}/string.xml: {e}")
        exit(1)

    matches = regex.findall(content)
    result = dict(matches)
    result = {key: unescape_special_characters(value) for key, value in result.items()}
    try:
        with open(
            os.path.join(locales_folder, f"{lang}.json"),
            "w",
            encoding="utf-8",
        ) as json_file:
            json.dump(result, json_file, indent=2, ensure_ascii=False)
            json_file.write("\n")

    except FileNotFoundError:
        print(f"Error: The folder '{locales_folder}' does not exist or cannot be accessed for writing.")
        exit(1)

    except Exception as e:
        print(f"Error: An unexpected error occurred while writing to '{locales_folder}/{lang}.json: {e}")
        exit(1)

print(
    "Scribe-i18n localization strings files successfully converted to the JSON files."
)
