import json
from dataclasses import asdict
from dataclasses import dataclass

from langs import Languages


@dataclass
class LocalDefinition:
    translate: bool
    both: bool
    term: str
    section: str
    display: str
    modified: bool = False
    synced: bool = True

    def cloneAs(self, new_display: str):
        return LocalDefinition(self.translate, self.both, self.term, self.section, new_display, True, True)


def parse_local_definitions(path):
    results = []
    section = "General"

    try:
        with open(path, 'r', encoding='utf-8') as buffered_reader:
            for line in buffered_reader:
                line = line.rstrip("\n")  # Strip trailing newline

                if line.startswith("#=") and len(line) > 2:
                    section = line[2:]

                elif (line.startswith("@") or
                      line.startswith("^@") or
                      line.startswith("!@") or
                      line.startswith("!^@")):

                    first_equal = line.find('=')
                    if first_equal > 0:
                        front = line[:first_equal]
                        translate = True
                        both = False

                        if front.startswith("!"):
                            translate = False
                            front = front[1:]

                        if front.startswith("^"):
                            both = True
                            front = front[1:]

                        back = line[first_equal + 1:]
                        results.append(LocalDefinition(
                            translate=translate,
                            both=both,
                            term=front,
                            section=section,
                            display=back,
                            modified=False,
                            synced=True
                        ))

    except Exception as ex:
        print(f"Error reading {path}: {ex}")

    return results


def load_local_definitions_from_json(path):
    results = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        definitions_by_lang = data.get("definitions", {})

        for language, defs in definitions_by_lang.items():
            results[language] = [
                LocalDefinition(**{**d, "synced": d.get("synced", True)})
                for d in defs
            ]

    except Exception as ex:
        print(f"Error reading {path}: {ex}")

    return results


def save_local_definitions_to_json(path, results):
    try:
        data = {
            "definitions": {
                language: [
                    asdict(defn)
                    for term, defn in sorted(defs.items(), key=lambda x: x[0].lower())
                ]
                for language, defs in sorted(results.items(), key=lambda x: x[0].lower())
            }
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as ex:
        print(f"Error writing {path}: {ex}")


def write_language(path, language, definitions, english_definitions, developer_definitions):
    # Sort by section, then term
    items = sorted(
        definitions.values(),
        key=lambda d: (d.section.lower(), d.term.lower())
    )

    with open(path, "w", encoding="utf-8") as f:
        current_section = ""

        for local_def in items:
            if current_section != local_def.section:
                f.write(f"#={local_def.section}\n")
                current_section = local_def.section

            f.write(f"{local_def.term}={local_def.display}")

            if language != Languages.English:
                developer_lang = developer_definitions.get(local_def.term)
                if developer_lang and developer_lang.both:
                    english_lang = english_definitions.get(local_def.term)
                    if english_lang:
                        f.write(f" - {english_lang.display}")

            f.write("\n")
