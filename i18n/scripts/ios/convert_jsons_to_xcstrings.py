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
        
shared_keys = {"i18n._global.legal", "i18n._global.privacy_policy", "i18n.app._global.download_data", "i18n.app._global.english", "i18n.app._global.french", "i18n.app._global.german", "i18n.app._global.indonesian", "i18n.app._global.italian", "i18n.app._global.norwegian", "i18n.app._global.portuguese", "i18n.app._global.russian", "i18n.app._global.spanish", "i18n.app._global.swedish"}

unused_keys = {"i18n.app.about.community.share_conjugate", "i18n.app.about.feedback.rate_conjugate", "i18n.app.conjugate.choose_conjugation.select_tense", "i18n.app.conjugate.choose_conjugation.title", "i18n.app.conjugate.recently_conjugated.title", "i18n.app.conjugate.title", "i18n.app.conjugate.verbs_search.placeholder", "i18n.app.conjugate.verbs_search.title", "i18n.app.download.menu_option.conjugate_description", "i18n.app.download.menu_option.conjugate_download_data", "i18n.app.download.menu_option.conjugate_download_data_start", "i18n.app.download.menu_option.conjugate_title", "i18n.app.download.menu_option.scribe_description", "i18n.app.download.menu_option.scribe_download_data", "i18n.app.download.menu_option.scribe_title", "i18n.app.download.menu_ui.download_data.all_languages", "i18n.app.download.menu_ui.download_data.downloading", "i18n.app.download.menu_ui.download_data.title", "i18n.app.download.menu_ui.download_data.up_to_date", "i18n.app.download.menu_ui.download_data.update", "i18n.app.download.menu_ui.no_keyboards_installed", "i18n.app.download.menu_ui.update_data", "i18n.app.download.menu_ui.update_data.check_new", "i18n.app.download.menu_ui.update_data.regular_update", "i18n.app.installation.button_quick_tutorial", "i18n.app.installation.keyboard.keyboard_settings", "i18n.app.settings.keyboard.functionality.annotate_suggestions",  "i18n.app.settings.keyboard.functionality.annotate_suggestions_description", "i18n.app.settings.keyboard.functionality.default_emoji_tone", "i18n.app.settings.keyboard.functionality.default_emoji_tone_description", "i18n.app.settings.keyboard.functionality.default_emoji_tone.caption", "i18n.app.settings.keyboard.functionality.hold_for_alt_chars", "i18n.app.settings.keyboard.functionality.hold_for_alt_chars_description", "i18n.app.settings.keyboard.functionality.popup_on_keypress", "i18n.app.settings.keyboard.functionality.popup_on_keypress_description", "i18n.app.settings.keyboard.functionality.punctuation_spacing", "i18n.app.settings.keyboard.functionality.punctuation_spacing_description", "i18n.app.settings.keyboard.keypress_sound", "i18n.app.settings.keyboard.keypress_sound_description", "i18n.app.settings.keyboard.keypress_vibration", "i18n.app.settings.keyboard.keypress_vibration_description",  "i18n.app.settings.keyboard.layout.default_currency", "i18n.app.settings.keyboard.layout.default_currency_description", "i18n.app.settings.keyboard.layout.default_currency.caption", "i18n.app.settings.keyboard.layout.default_layout", "i18n.app.settings.keyboard.layout.default_layout_description", "i18n.app.settings.keyboard.layout.default_layout.caption", "i18n.app.settings.keyboard.translation.select_source.title", "i18n.app.settings.menu.app_color_mode", "i18n.app.settings.menu.app_color_mode_description", "i18n.app.settings.menu.app_language_description", "i18n.app.settings.menu.app_language.caption", "i18n.app.settings.menu.high_color_contrast", "i18n.app.settings.menu.high_color_contrast_description", "i18n.app.settings.menu.increase_text_size", "i18n.app.settings.menu.increase_text_size_description"}

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
    
    is_shared = key in shared_keys
    is_valid_app_key = key.startswith("i18n.app") and key not in unused_keys

    if is_shared or is_valid_app_key:
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
