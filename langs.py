from enum import Enum

class Languages(Enum):
    Developer = ""
    Afrikaans = "af"
    Arabic = "ar"
    Basque = "eu"
    Belarusian = "be"
    Bulgarian = "bg"
    Catalan = "ca"
    Chinese = "zh-CN"
    Czech = "cs"
    Danish = "da"
    Dutch = "nl"
    English = "en"
    Estonian = "et"
    Finnish = "fi"
    French = "fr"
    German = "de"
    Greek = "el"
    Hebrew = "iw"
    Hungarian = "hu"
    Icelandic = "is"
    Indonesian = "id"
    Italian = "it"
    Japanese = "ja"
    Korean = "ko"
    Latvian = "lv"
    Lithuanian = "lt"
    Norwegian = "no"
    Polish = "pl"
    Portuguese = "pt"
    Romanian = "ro"
    Russian = "ru"
    Slovak = "sk"
    Slovenian = "sl"
    Spanish = "es"
    Swedish = "sv"
    Thai = "th"
    Turkish = "tr"
    Ukrainian = "uk"
    Vietnamese = "vi"
    ChineseSimplified = "zh-CN"
    ChineseTraditional = "zh-TW"

    @property
    def short_name(self):
        return self.value

    @classmethod
    def from_short_name(cls, short_name):
        for lang in cls:
            if lang.short_name == short_name:
                return lang
        raise ValueError(f"No matching language for short name: {short_name}")

if __name__ == '__main__':
    # Example usage:
    print(Languages.English.short_name)  # "en"

    # Iterate all values
    for lang in Languages:
        print(lang.name, "->", lang.short_name)