import argparse
import os

from ai_handler import get_translated_for
from backups import rotate_backups
from dev_parser import parse_local_definitions, load_local_definitions_from_json, save_local_definitions_to_json, \
    write_language
from langs import Languages


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def translate(developer_file, json_file, output_folder):
    # Use a breakpoint in the code line below to debug your script.
    # print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    developer_rows = parse_local_definitions(developer_file)

    print(f'Found {len(developer_rows)} Developer Rows')

    definitions = {}

    for lang in Languages:
        definitions[lang.name] = {}

    lang_data = load_local_definitions_from_json(json_file)

    for lang in definitions.keys():
        items = definitions[lang]
        if lang == Languages.Developer.name:
            lang_items = developer_rows
        else:
            lang_items = lang_data[lang]
        for lang_item in lang_items:
            items[lang_item.term] = lang_item

    # Get the English Definitions
    english_definitions = definitions[Languages.English.name]
    developer_definitions = definitions[Languages.Developer.name]

    # Extract sets of terms (keys) from each language
    english_terms = {ld.term for ld in english_definitions.values()}
    developer_terms = {ld.term for ld in developer_definitions.values()}
    updated_keys = []

    # Keys in both
    common_terms = english_terms.intersection(developer_terms)

    # Keys only in developer
    only_in_developer = developer_terms - english_terms

    # Keys only in english
    keys_to_remove = english_terms - developer_terms

    for common_term in common_terms:
        developer_item = developer_definitions[common_term]
        english_item = english_definitions[common_term]
        if developer_item.display != english_item.display:
            updated_keys.append(developer_item.term)

    print("New Keys:", only_in_developer)
    print("Changed Keys:", updated_keys)
    print("Removed Keys:", keys_to_remove)

    # remove dead keys
    if len(keys_to_remove) > 0:
        for lang in Languages:
            definition = definitions[lang.name]
            for key in keys_to_remove:
                if key in definition:
                    del definition[key]

    # Start translating values

    # New values
    for new_term in only_in_developer:
        print(f'New Term: {new_term}')
        developer_item = developer_definitions[new_term]
        for lang in Languages:
            if lang == Languages.Developer:
                continue
            if lang == Languages.English:
                # Overwrite the english item
                english_definitions = definitions[Languages.English.name]
                english_definitions[new_term] = developer_item
                continue

            current_definitions = definitions[lang.name]

            translated_text = get_translated_for(developer_item.display, lang.name, new_term)

            if translated_text is not None and translated_text != '':
                print(f'Found: "{translated_text}" for {lang.name}')
                new_item = developer_item.cloneAs(translated_text)
                current_definitions[new_term] = new_item
            else:
                print(f'Missing: "{new_term}" for {lang.name}')

    # Updated values
    for updated_keys in updated_keys:
        print(f'Changed Term: {updated_keys}')
        developer_item = developer_definitions[updated_keys]
        for lang in Languages:
            if lang == Languages.Developer:
                continue
            if lang == Languages.English:
                # Overwrite the english item
                english_definitions = definitions[Languages.English.name]
                english_definitions[updated_keys] = developer_item
                continue

            current_definitions = definitions[lang.name]

            translated_text = get_translated_for(developer_item.display, lang.name, updated_keys)

            if translated_text is not None and translated_text != '':
                print(f'Found: "{translated_text}" for {lang.name}')
                new_item = developer_item.cloneAs(translated_text)
                current_definitions[current_definitions] = new_item
            else:
                print(f'Missing: "{current_definitions}" for {lang.name}')
                current_definitions[current_definitions].synced = False

    for lang in Languages:
        if lang == Languages.Developer:
            continue

        write_language(
            os.path.join(output_folder, lang.name + ".txt"),
            lang,
            definitions[lang.name],
            definitions[Languages.English.name],
            definitions[Languages.Developer.name]
        )

    rotate_backups(json_file, 5)

    save_local_definitions_to_json(json_file, definitions)

    print('Program Complete')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process dev, json, and output paths.")

    parser.add_argument("dev", type=str, help="Path to the developer file")
    parser.add_argument("json", type=str, help="Path to the JSON file")
    parser.add_argument("output", type=str, help="Path to the output file")

    args = parser.parse_args()

    print(f"Dev file: {args.dev}")
    print(f"JSON file: {args.json}")
    print(f"Output file: {args.output}")

    translate(args.dev, args.json, args.output)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
