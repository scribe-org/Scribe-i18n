import os
import json
import requests

url = ('https://github.com/scribe-org/Scribe-iOS/raw/606a67a0fa3f665349f2402ef265e743c015b588/Scribe/Resources'
       '/Localizable.xcstrings')
response = requests.get(url)

if response.status_code == 200:
    file = response.content
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = os.listdir(directory)
    langlist = [file.replace('.json', '') for file in files if file.endswith('.json')]

    for lang in langlist:
        dest = open(f'{directory}/{lang}.json', 'w')
        if lang == "en-US":
            lang = "en"

        data = '{\n'
        json_file = json.loads(file)
        strings = json_file["strings"]
        pos = 0
        for key in strings:
            pos += 1
            translation = ''
            if lang in json_file["strings"][key]["localizations"]:
                translation = (json_file["strings"][key]["localizations"][lang]["stringUnit"]["value"]
                               .replace('"', '\\"')
                               .replace('\n', '\\n'))
            comment = ''
            if "comment" in json_file["strings"][key]:
                comment = (json_file["strings"][key]["comment"]
                           .replace('"', '\\"')
                           .replace('\n', '\\n'))
            data += (f'  "{key}" : {{\n'
                     f'    "translation" : "{translation}",\n'
                     f'    "comment" : "{comment}"\n'
                     f'  }}')
            if pos < len(json_file["strings"]):
                data += ',\n'
            else:
                data += '\n'
        data += '}\n'

        dest.write(data)

else:
    print("Failed to fetch the file. Status code:", response.status_code)
