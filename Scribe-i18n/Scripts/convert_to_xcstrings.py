import os
import json

directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = os.listdir(directory)
langlist = sorted([file.replace('.json', '') for file in files if file.endswith('.json')])
path = os.path.join(directory, 'en-US.json')
file = open(path, 'r').read()
file = json.loads(file)

data = ('{\n'
        '  "sourceLanguage" : "en",\n'
        '  "strings" : {\n')
pos = 0
for key in file:
    pos += 1
    data += (f'    "{key}" : {{\n'
             f'      "comment" : "",\n'
             f'      "localizations" : {{\n')
    for lang in langlist:
        if lang != 'en-US':
            langfile = json.loads(open(os.path.join(directory, f'{lang}.json'), 'r').read())
            translation = (langfile[key]
                           .replace('"', '\\"')
                           .replace('\n', '\\n'))
            if translation != '':
                data += (f'        "{lang}" : {{\n'
                         f'          "stringUnit" : {{\n'
                         f'            "state" : "",\n'
                         f'            "value" : "{translation}"\n'
                         f'          }}\n'
                         f'        }},\n')

    langfile = json.loads(open(os.path.join(directory, f'en-US.json'), 'r').read())
    translation = (langfile[key]
                   .replace('"', '\\"')
                   .replace('\n', '\\n'))
    data += (f'        "en" : {{\n'
             f'          "stringUnit" : {{\n'
             f'            "state" : "",\n'
             f'            "value" : "{translation}"\n'
             f'          }}\n'
             f'        }}\n')

    if pos < len(file):
        data += ('      }\n'
                 '    },\n')
    else:
        data += ('      }\n'
                 '    }\n')

data += (f'  }},\n'
         f'  "version" : "1.0"\n'
         f'}}')
open(os.path.join(directory, "Localizable.xcstrings"), 'w').write(data)
